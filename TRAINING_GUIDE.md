# llm-from-scratch Training Instructions

## Status
Repository successfully cloned and verified at:
C:\Users\Sharma\Documents\Python Projects\LLM\llm-from-scratch

Dataset downloaded:
- data/TinyStoriesV2-GPT4-train.txt (1.3 GB)
- data/TinyStoriesV2-GPT4-valid.txt (1.2 MB)

## Quick Test Completed
A minimal training run was executed to verify the pipeline:
- Used small subset of data (first 1000 training lines)
- Trained for 10 iterations
- Generated sample text (showed repetitive patterns due to minimal training)
- Confirmed all components work: tokenizer, model, training loop, generation

## For Meaningful Training (Full Dataset)

### 1. Install CUDA-enabled PyTorch (if GPU available)
The current uv environment has CPU-only PyTorch. To use CUDA:

```bash
# Option A: Using uv (recommended)
uv pip uninstall torch torchaudio torchvision -y
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Option B: Using regular pip
pip uninstall torch torchaudio torchvision -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Verify installation:
```bash
uv run python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

### 2. Tokenize the Full Dataset
Run the BPE tokenizer on the complete text files to create memory-mapped arrays:

```bash
uv run -m llm.bpe_tokenizer \
  --train_source_file data/TinyStoriesV2-GPT4-train.txt \
  --valid_source_file data/TinyStoriesV2-GPT4-valid.txt \
  --tokenizer_checkpoint data/tokenizer \
  --train_data data/training_data.npy \
  --val_data data/validation_data.npy \
  --vocab_size 2048
```

This produces:
- `data/tokenizer`: trained BPE model
- `data/training_data.npy`: tokenized training data (~1.3GB)
- `data/validation_data.npy`: tokenized validation data

### 3. Launch Training
Start the training loop with appropriate hyperparameters:

```bash
uv run -m llm.training \
  --device cuda:0 \
  --world_size 1 \
  --backend gloo \
  --iterations 20000 \
  --batch_size 64 \
  --max_seq_len 256 \
  --log_interval 100 \
  --val_interval 500 \
  --warmup_iters 2000 \
  --cos_cycle_iters 20000 \
  --lr 1e-4 \
  --lr_min 1e-5 \
  --lr_max 1e-4 \
  --train_data data/training_data.npy \
  --val_data data/validation_data.npy \
  --tokenizer_checkpoint data/tokenizer \
  --checkpoint_path checkpoints \
  --log_dir logs
```

### 4. Monitor Progress
- Console output shows training/validation loss every log_interval
- TensorBoard: `tensorboard --logdir logs` (install with `uv pip install tensorboard`)
- Checkpoints saved to `checkpoints/chpt_*.pt`

### 5. Generate Text After Training
Sample from a trained checkpoint:

```bash
uv run -m llm.generating \
  --device cuda:0 \
  --checkpoint_path checkpoints \
  --tokenizer_checkpoint data/tokenizer \
  --iterations 18000  # or whichever checkpoint you prefer
```

## Hyperparameter Adjustments
- For GTX 1650 (4GB VRAM): batch_size=32-64, max_seq_len=128-256
- For longer training: increase iterations to 50k+
- For larger models: increase d_model, n_layers, n_heads (adjust accordingly in llm/args.py)

## Notes
- The training script uses memory-mapped files (`mmap_mode='r'`) so it can handle datasets larger than RAM.
- Validation runs every val_interval steps to track overfitting.
- Learning rate follows cosine decay with warmup.
- Checkpoints include model state, optimizer state, and iteration count.

## Repository Structure
Key directories/files:
- `llm/`: Core model (transformer.py), tokenizer (bpe_tokenizer.py), training/generation scripts
- `data/`: Dataset files and tokenized outputs
- `checkpoints/`: Saved model checkpoints (created during training)
- `logs/`: TensorBoard logs
- `alignment/`: SFT and RLHF scripts (for advanced fine-tuning)

## Troubleshooting
- **CUDA not available**: Reinstall PyTorch with correct CUDA wheel
- **Out of memory**: Reduce batch_size or max_seq_len
- **Slow data loading**: Ensure you're using the .npy files (not raw text) for train_data/val_data
- **Tokenizer mismatches**: Always use the same tokenizer checkpoint for training and generation

You now have a complete, working llm-from-scratch implementation ready for experimentation!