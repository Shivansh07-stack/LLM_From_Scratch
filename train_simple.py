import torch
import numpy as np
from llm.args import get_parser
from llm.transformer import Transformer, AdamW, CrossEntropyLoss, gradient_clip, cos_lr_scheduler
from llm.bpe_tokenizer import BpeTokenizer
import os
import time

def get_batch(x: np.ndarray, batch_size: int, context_length: int, device: str):
    ix = torch.randint(0, len(x) - context_length, (batch_size,))
    input_seqs = torch.stack([torch.from_numpy(x[i : i + context_length].astype(np.int64)) for i in ix])
    target_seqs = torch.stack([torch.from_numpy(x[i + 1 : i + 1 + context_length].astype(np.int64)) for i in ix])
    return input_seqs.to(device), target_seqs.to(device)

def main():
    parser = get_parser()
    args = parser.parse_args()
    # Override for quick test
    args.device = "cpu"
    args.world_size = 1
    args.backend = "gloo"
    args.iterations = 50
    args.batch_size = 16
    args.max_seq_len = 64
    args.log_interval = 5
    args.val_interval = 25
    args.warmup_iters = 10
    args.cos_cycle_iters = args.iterations
    args.lr = 5e-4
    args.lr_min = 1e-5
    args.lr_max = 5e-4
    args.train_source_file = "data/TinyStoriesV2-GPT4-train.txt"
    args.valid_source_file = "data/TinyStoriesV2-GPT4-valid.txt"
    args.train_data = "data/training_data.npy"
    args.val_data = "data/validation_data.npy"
    args.tokenizer_checkpoint = "data/tokenizer_small"
    args.checkpoint_path = "checkpoints"
    args.log_dir = "logs"
    
    os.makedirs(args.checkpoint_path, exist_ok=True)
    os.makedirs(args.log_dir, exist_ok=True)
    
    # Load tokenizer
    tokenizer = BpeTokenizer(special_tokens=["<|endoftext|>"])
    tokenizer.load(args.tokenizer_checkpoint)
    args.vocab_size = len(tokenizer.vcab2id)
    print(f"Vocab size: {args.vocab_size}")
    
    # Load data
    train_data = np.load(args.train_data, mmap_mode='r')
    val_data = np.load(args.val_data, mmap_mode='r')
    print(f"Train data shape: {train_data.shape}, Val data shape: {val_data.shape}")
    
    # Model
    model = Transformer(
        d_model=args.d_model,
        num_heads=args.num_heads,
        d_ff=args.d_ff,
        vocab_size=args.vocab_size,
        num_layers=args.num_layers,
        max_seq_len=args.max_seq_len,
        device=args.device,
    ).to(args.device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters())/1e6:.2f} M")
    
    optimizer = AdamW(model.parameters(), lr=args.lr, betas=(args.beta1, args.beta2), weight_decay=args.weight_decay)
    criterion = CrossEntropyLoss()
    
    # Training loop
    model.train()
    start_time = time.time()
    for i in range(args.iterations + 1):
        # Validation
        if i % args.val_interval == 0:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for _ in range(20):  # fewer batches for speed
                    val_inputs, val_targets = get_batch(val_data, args.batch_size, args.max_seq_len, args.device)
                    val_logits = model(val_inputs)
                    val_loss += criterion(val_logits, val_targets).item()
            val_loss /= 20
            model.train()
            print(f"Iter {i:4d} | Val Loss: {val_loss:.4f}")
        
        # Training step
        inputs, targets = get_batch(train_data, args.batch_size, args.max_seq_len, args.device)
        logits = model(inputs)
        loss = criterion(logits, targets)
        
        optimizer.zero_grad()
        loss.backward()
        gradient_clip(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        # LR scheduling
        lr = cos_lr_scheduler(
            it=i,
            warmup_iters=args.warmup_iters,
            cos_cycle_iters=args.cos_cycle_iters,
            lr_min=args.lr_min,
            lr_max=args.lr_max,
        )
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
        
        if i % args.log_interval == 0:
            print(f"Iter {i:4d} | Train Loss: {loss.item():.4f} | LR: {lr:.6f}")
        
        # Checkpoint
        if i % 200 == 0 and i > 0:
            torch.save({
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'iteration': i,
                'loss': loss.item(),
            }, os.path.join(args.checkpoint_path, f'model_{i}.pt'))
            print(f"Saved checkpoint at iteration {i}")
    
    end_time = time.time()
    print(f"Training completed in {end_time - start_time:.2f} seconds")
    
    # Generate a sample
    model.eval()
    prompt = "tell you a story"
    token_ids = tokenizer.encode(prompt)
    input_ids = torch.tensor(token_ids, dtype=torch.long, device=args.device).unsqueeze(0)
    with torch.no_grad():
        for _ in range(50):  # generate 50 tokens
            input_ids_cond = input_ids[:, -model.max_seq_len:]
            token_positions = torch.arange(input_ids_cond.shape[1], device=args.device).unsqueeze(0)
            logits = model(input_ids_cond, token_positions)
            logits = logits[:, -1, :] / 0.8
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            input_ids = torch.cat([input_ids, next_token], dim=1)
            if next_token.item() == tokenizer.vcab2id[tokenizer.special_tokens[0]]:
                break
    prompt_len = len(token_ids)
    generated_ids = input_ids[0, prompt_len:].tolist()
    if generated_ids and generated_ids[-1] == tokenizer.vcab2id[tokenizer.special_tokens[0]]:
        generated_ids.pop()
    print(f"\nPrompt: {prompt}")
    print(f"Completion: {tokenizer.decode(generated_ids)}")

if __name__ == "__main__":
    main()