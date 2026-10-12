# 🧠 LLM From Scratch

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Tests](https://img.shields.io/badge/tests-52%20passed-brightgreen.svg)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Shivansh07--stack%2FLLM__From__Scratch-black?logo=github)](https://github.com/Shivansh07-stack/LLM_From_Scratch)

> **No black boxes. No monolithic wrappers. Just pure PyTorch, raw mathematics, and clean Python.**

Welcome to **LLM From Scratch** — a ground-up journey through modern decoder-only language model engineering. If you've ever wanted to dissect how GPTs and modern open-source models actually tick under the hood—from raw byte tokenization to RoPE rotary math, SwiGLU activations, distributed gradient bucketing, and RL post-training alignment—this repository is your playground.

---

## ⚡ The "Twitch": Why Build This?

Most tutorials stop at vanilla 2017 Transformers with sinusoidal embeddings and standard GeLU. **Modern LLMs don't look like that anymore.**

This repository implements the actual, production-grade battle-tested primitives powering frontier LLMs today:
* **Pre-Layer RMSNorm** instead of legacy LayerNorm.
* **SwiGLU** (Swish-Gated Linear Units) instead of plain feed-forward layers.
* **Rotary Position Embeddings (RoPE)** instead of static positional encodings.
* **From-Scratch Byte Pair Encoding (BPE)** with special token manipulation.
* **Distributed Training** featuring custom **DDP** gradient bucketing and a **Sharded Optimizer** (ZeRO-1 style).
* **Alignment Lab**: Supervised Fine-Tuning (SFT) & Group-wise Reward Policy Optimization (GRPO) for reasoning models.

---

## 🧬 Architectural Anatomy

```
                     ┌────────────────────────────────────────┐
                     │          Prompt Input String           │
                     └───────────────────┬────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │      BpeTokenizer (Byte-Pair)          │
                     └───────────────────┬────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │       Token Embedding Layer            │
                     └───────────────────┬────────────────────┘
                                         ▼
               ┌────────────────────────────────────────────────────┐
               │         Transformer Block (× N Layers)             │
               │                                                    │
               │  Input ───► RMSNorm ───► Multi-Head Attn ──► (+)  │
               │                            (RoPE + Flash)     │    │
               │                                               ▼    │
               │  (+) ─────► RMSNorm ───► SwiGLU FFN ───────► (+)  │
               └─────────────────────────┬──────────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │          Final RMSNorm                 │
                     └───────────────────┬────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │      Linear Projection Head            │
                     └───────────────────┬────────────────────┘
                                         ▼
                     ┌────────────────────────────────────────┐
                     │  Autoregressive Sampling (Top-p / Temp)│
                     └────────────────────────────────────────┘
```

| Component | File | What Makes It Special |
|---|---|---|
| **Transformer** | [`llm/transformer.py`](llm/transformer.py) | Full decoder-only autoregressive stack with KV caches and pre-normalization. |
| **RoPE** | [`llm/transformer.py`](llm/transformer.py) | Complex rotation matrices applied directly to queries and keys. |
| **SwiGLU** | [`llm/transformer.py`](llm/transformer.py) | Gated activation ($\text{Swish}(x W_1) \otimes (x W_3) W_2$). |
| **BPE Tokenizer** | [`llm/bpe_tokenizer.py`](llm/bpe_tokenizer.py) | Pure byte-level pair encoding with merge rank caching and custom regex splits. |
| **Flash Attention** | [`kernel/`](kernel/) | Triton v2 GPU kernels + a pure PyTorch mock autograd fallback. |
| **DDP & Sharding** | [`parallel/`](parallel/) | Bucket-based gradient all-reduce + parameter-sharded optimizer. |
| **Curation Suite** | [`data_processing/`](data_processing/) | Exact line deduplication, MinHash, PII redactor, and quality filters. |
| **Alignment** | [`alignment/`](alignment/) | SFT microbatching and GRPO policy gradient loss with group normalization. |

---

## 🚀 Quickstart: Zero to Text in 10 Seconds

### 1. Setup Environment
Clone the repository and install dependencies using [`uv`](https://docs.astral.sh/uv/) (lightning fast) or `pip`:

```bash
git clone https://github.com/Shivansh07-stack/LLM_From_Scratch.git
cd LLM_From_Scratch

# Using uv
uv sync

# Or standard virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Ignite the Training Loop
Run an end-to-end 10-iteration training and inference verification on CPU/GPU:

```bash
uv run python train_quick.py
```

Watch the model initialize, calculate loss, decay learning rate with cosine warmup, save checkpoints, and start generating tokens:
```text
Vocab size: 1024
Model parameters: 7.89 M
Iter    0 | Val Loss: 7.0092 | Train Loss: 7.1760 | LR: 0.000000
Iter    5 | Val Loss: 6.9096 | Train Loss: 7.1179 | LR: 0.000349  -> Saved model_5.pt
Iter   10 | Val Loss: 7.0273 | Train Loss: 6.7817 | LR: 0.000010  -> Saved model_10.pt
Training completed in 7.58 seconds!

Prompt: tell you a story
Completion:  tr ne farm *B abust I it elpler rainLraurnckK
```

### 3. Generate with Custom Prompts
Test greedy and temperature-scaled text generation with the standalone generator:

```bash
uv run python test_generate.py
```

---

## 📖 Training on the TinyStories Dataset

The repository is built to train on the high-quality synthetic [TinyStories](https://huggingface.co/datasets/roneneldan/TinyStories) dataset.

### Step 1: Grab the Raw Data
```bash
mkdir -p data
cd data
# Download Training set (1.35 GB text corpus)
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-train.txt
# Download Validation set (22.5 MB)
wget https://huggingface.co/datasets/roneneldan/TinyStories/resolve/main/TinyStoriesV2-GPT4-valid.txt
cd ..
```
*(On Windows PowerShell, use `curl.exe -L -o "data/TinyStoriesV2-GPT4-valid.txt" "<URL>"`)*

### Step 2: Tokenize into Memory-Mapped Arrays
Compile the text into binary NumPy token arrays (`.npy`) for zero-overhead streaming:
```bash
uv run python tokenize_tinystories.py
```
* Generates `data/training_data.npy` (3,190,000+ tokens)
* Generates `data/validation_data.npy` (318,000+ tokens)

### Step 3: Train Like a Pro
Train on your local device (CPU or single GPU) with live loss tracking:
```bash
uv run python train_simple.py
```
Or launch multi-GPU distributed training with DDP and parameter sharding:
```bash
uv run python -m llm.training --world_size 4 --batch_size 64 --iterations 20000
```

---

## 🔬 Data Processing & Curation Suite

Real LLMs are only as good as their data diet. This repository includes a full preprocessing pipeline under [`data_processing/`](data_processing/):

* **MinHash Deduplication** ([`deduplicate.py`](data_processing/deduplicate.py)): Removes near-duplicate text using Jaccard similarity hashing.
* **PII Redaction** ([`mask_pii.py`](data_processing/mask_pii.py)): Replaces emails, phone numbers, and IP addresses with safe tokens.
* **Quality Filtering** ([`quality_filter.py`](data_processing/quality_filter.py)): Gopher-style heuristics (word count, average token length, symbol-to-word ratios).
* **HTML Stripping** ([`html_process.py`](data_processing/html_process.py)): Cleans web scrapes into clean plaintext.

---

## 🎯 Alignment & Reasoning (SFT & GRPO)

Take base models beyond next-token prediction:

1. **Supervised Fine-Tuning (SFT)** ([`alignment/sft.py`](alignment/sft.py)):
   * Fine-tune on prompt-response pairs with prompt masking (loss only on answer tokens).
2. **Group-wise Reward Policy Optimization (GRPO)** ([`alignment/grpo.py`](alignment/grpo.py)):
   * PPO-style RL without an expensive critic network.
   * Samples group outputs, calculates group-normalized advantage scores, and optimizes policy clip objectives with entropy bonuses.

---

## 🧪 Bulletproof Testing Suite

Every mathematical operation and utility is rigorously verified via `pytest`:

```bash
uv run pytest tests/test_model.py tests/test_tokenizer.py tests/test_data.py tests/test_deduplication.py tests/test_pii.py tests/test_serialization.py tests/test_optimizer.py tests/test_nn_utils.py tests/test_generating.py -v
```

**Results:** **52 Passed, 0 Failed** (100% pass rate).

---

## ⚙️ Default Hyperparameter Spec

```yaml
Architecture:
  d_model: 288
  num_heads: 6
  d_ff: 1024
  num_layers: 6
  max_seq_len: 512
  vocab_size: 1024
  activation: SwiGLU
  normalization: RMSNorm
  positional_encoding: RoPE

Optimization:
  optimizer: AdamW
  learning_rate: 5e-4
  min_learning_rate: 1e-5
  weight_decay: 0.01
  betas: [0.9, 0.999]
  warmup_iters: 10
  lr_schedule: Cosine with warmup
```

---

## 🤝 Contributing

Contributions, optimizations, and PRs are always welcome!
If you build something cool with this or spot an optimization, feel free to open an issue or pull request.

## 📄 License

Licensed under the MIT License. Build, learn, and hack freely!
