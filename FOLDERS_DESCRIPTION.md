# Folder Descriptions for llm-from-scratch

## alignment
Contains scripts and configurations for model alignment training, including:
- Supervised Fine-Tuning (SFT)
- Reinforcement Learning from Human Feedback (RLHF)
- Group Relative Policy Optimization (GRPO)
- Dataset handling and prompt templates
Key files: `args.py`, `dataset.py`, `grpo.py`, `sft.py`, `train_rl.py`, and prompt templates in `prompts/`.

## bench_mark
Benchmarking scripts to measure performance of various components:
- Attention mechanisms (standard, flash attention, JIT compiled)
- Distributed Data Parallel (DDP) training
- Model inference speed
Key files: `bench_mark_atten.py`, `bench_mark_flash_attention.py`, `bench_mark_ddp.py`, `bench_mark_model.py`.

## checkpoints_small
Directory intended for storing small model checkpoints (currently empty).

## checkpoints_test
Stores large model checkpoint files used during testing:
- `model_10.pt` and `model_5.pt` (approximately 94 MB each) are saved model states.

## data
Holds the training and validation datasets:
- Raw text datasets: `TinyStories_small.txt`, `TinyStories_train_small.txt`, `TinyStories_valid_small.txt`, `TinyStoriesV2-GPT4-train.txt`
- Tokenizer files: `tokenizer_small`, `tokenizer_small_test`
- Pre-tokenized data in NumPy format: `training_data_small.npy`, `validation_data_small.npy`, and their test variants.

## data_processing
Scripts for preparing and cleaning the training data:
--Bret
- deduplicate.py: Remove duplicate lines from documents.
- harmful_detect.py: Detect harmful content.
- html_process.py: Strip HTML tags and extract text.
- language_identification.py: Identify language of text.
- mask_pii.py: Mask personally identifiable information.
- quality_classfier.py: Classify text quality (note: spelling as in original).
- quality_filter.py: Filter low-quality data.

## doc_scripts
Utility scripts for documentation:
- export_platform_posts.py: Export documentation to various platforms.
- sync_lark_doc.py: Synchronize with Lark docs.

## docs
Documentation source code:
- source/: Contains the Sphinx documentation source, including chapters, images, and configuration.

## img
Image files used in the project:
- loss.png: Plot of training loss over time.
- lr.png: Plot of learning rate schedule.

## kernel
Custom kernel implementations for acceleration:
- flash_attention_mock.py: Mock implementation of flash attention.
- flash_attention_triton.py: Triton implementation of flash attention.

## llm
Core LLM implementation:
- args.py: Command-line arguments parsing.
- bpe_tokenizer.py: Byte Pair Encoding tokenizer.
- checkpoint.py: Model checkpoint saving and loading.
- generating.py: Text generation loop.
- training.py: Model training loop.
- transformer.py: Transformer model definition.

## log_small
Directory for small log files (currently empty).

## logs_test
Directory for test log files (currently empty).

## parallel
Utilities for distributed training:
- ddp.py: Distributed Data Parallel setup.
- sharded_optimizer.py: Sharded optimizer for memory efficiency.

## site
Website source built with Astro:
- public/: Static assets (favicon, images).
- src/: Astro components, layouts, and pages for the project's documentation site.
- Configuration files: astro.config.mjs, package.json, playwright.config.ts, tsconfig.json.

## tests
Unit and integration tests:
- Test modules for attention, data processing, DDP, generating, model, optimizer, etc.
- Fixtures: Sample texts, tokenization files, and test datasets.
- Snapshots: Expected outputs for various tests.

