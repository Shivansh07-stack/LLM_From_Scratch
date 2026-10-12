import torch
from llm.args import get_parser
from llm.transformer import Transformer, Softmax
from llm.bpe_tokenizer import BpeTokenizer
import os

def generate_random(prompt: str, model: Transformer, tokenizer: BpeTokenizer, device: str, max_new_tokens: int = 20):
    model.eval()
    token_ids = tokenizer.encode(prompt)
    input_ids = torch.tensor(token_ids, dtype=torch.long, device=device).unsqueeze(0)
    with torch.no_grad():
        for _ in range(max_new_tokens):
            input_ids_cond = input_ids[:, -model.max_seq_len:]
            token_positions = torch.arange(input_ids_cond.shape[1], device=device).unsqueeze(0)
            logits = model(input_ids_cond, token_positions)
            logits = logits[:, -1, :] / args.temperature
            probs = Softmax()(logits)
            # Simple greedy for demo
            next_token = torch.argmax(probs, dim=-1, keepdim=True)
            input_ids = torch.cat([input_ids, next_token], dim=1)
            if next_token.item() == tokenizer.vcab2id[tokenizer.special_tokens[0]]:
                break
    prompt_len = len(token_ids)
    generated_ids = input_ids[0, prompt_len:].tolist()
    if generated_ids and generated_ids[-1] == tokenizer.vcab2id[tokenizer.special_tokens[0]]:
        generated_ids.pop()
    return tokenizer.decode(generated_ids), generated_ids

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    # Override device to cpu
    args.device = "cpu"
    # Use the small tokenizer we trained
    tokenizer_path = "data/tokenizer_small"
    tokenizer = BpeTokenizer(special_tokens=["<|endoftext|>"])
    tokenizer.load(tokenizer_path)
    args.vocab_size = len(tokenizer.vcab2id)
    # Initialize model with random weights
    model = Transformer(
        d_model=args.d_model,
        num_heads=args.num_heads,
        d_ff=args.d_ff,
        vocab_size=args.vocab_size,
        num_layers=args.num_layers,
        max_seq_len=args.max_seq_len,
        device=args.device,
    ).to(args.device)
    prompt = "tell you a story"
    print(f"Prompt: {prompt}")
    output, output_token_ids = generate_random(prompt, model, tokenizer, args.device, max_new_tokens=20)
    print(f"Completion: {output}")
    print(f"Token IDs: {output_token_ids}")