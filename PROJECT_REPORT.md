# Project Report: llm-from-scratch

## Overview
[中文](./README_cn.md)

# LLM from Scratch

This repository contains a from-scratch implementation of a modern decoder-only Transformer model in PyTorch, built for educational purposes. It includes all the essential building blocks of a modern language model, written in a clear, modular, and understandable way. The goal of this project is to provide a comprehensive resource for learning how large language models are built from the ground up.

[My open source book for LLM](https://fangpin.github.io/llm-from-scratch/)

## PDF and EPUB

The **Deploy docs** GitHub Actions workflow builds PDF and EPUB editions from
the Sphinx sources in `docs/source/`, alongside the HTML site. It runs on pushes
to `main` or `master`, or manually from **Actions → Deploy docs → Run workflow**.
Download **book-pdf** and **book-epub** from the completed run's **Artifacts** section.

To build locally, install the Python documentation dependencies and a TeX Live
distribution with XeLaTeX, latexmk, Chinese language support (including the Fandol
fonts), FreeFont, and dvisvgm. On Ubuntu, install the system dependencies with:

```bash

## Folder Descriptions
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


## Complete File List
./.git/config
./.git/description
./.git/HEAD
./.git/hooks/applypatch-msg.sample
./.git/hooks/commit-msg.sample
./.git/hooks/fsmonitor-watchman.sample
./.git/hooks/post-update.sample
./.git/hooks/pre-applypatch.sample
./.git/hooks/pre-commit.sample
./.git/hooks/pre-merge-commit.sample
./.git/hooks/prepare-commit-msg.sample
./.git/hooks/pre-push.sample
./.git/hooks/pre-rebase.sample
./.git/hooks/pre-receive.sample
./.git/hooks/push-to-checkout.sample
./.git/hooks/sendemail-validate.sample
./.git/hooks/update.sample
./.git/index
./.git/info/exclude
./.git/logs/HEAD
./.git/logs/refs/heads/master
./.git/logs/refs/remotes/origin/HEAD
./.git/objects/pack/pack-83202bd1b740edcf66c6d4ecd467b5a59212de83.idx
./.git/objects/pack/pack-83202bd1b740edcf66c6d4ecd467b5a59212de83.pack
./.git/objects/pack/pack-83202bd1b740edcf66c6d4ecd467b5a59212de83.rev
./.git/packed-refs
./.git/refs/heads/master
./.git/refs/remotes/origin/HEAD
./.github/FUNDING.yml
./.github/workflows/docs.yml
./.gitignore
./.pytest_cache/.gitignore
./.pytest_cache/CACHEDIR.TAG
./.pytest_cache/README.md
./.pytest_cache/v/cache/lastfailed
./.pytest_cache/v/cache/nodeids
./alignment/__init__.py
./alignment/__pycache__/__init__.cpython-311.pyc
./alignment/__pycache__/evaluate.cpython-311.pyc
./alignment/args.py
./alignment/dataset.py
./alignment/drgrpo_grader.py
./alignment/evaluate.py
./alignment/grpo.py
./alignment/prompts/alpaca_sft.prompt
./alignment/prompts/question_only.prompt
./alignment/prompts/r1_zero.prompt
./alignment/prompts/zero_shot_system_prompt.prompt
./alignment/r1_prompt.py
./alignment/sft.py
./alignment/sft_tokenizer_saver.py
./alignment/train_rl.py
./alignment/util.py
./bench_mark/__init__.py
./bench_mark/bench_mark_atten.py
./bench_mark/bench_mark_atten_jit.py
./bench_mark/bench_mark_ddp.py
./bench_mark/bench_mark_flash_attention.py
./bench_mark/bench_mark_model.py
./BENCHMARK.md
./checkpoints_test/model_10.pt
./checkpoints_test/model_5.pt
./data/TinyStories_small.txt
./data/TinyStories_train_small.txt
./data/TinyStories_valid_small.txt
./data/TinyStoriesV2-GPT4-train.txt
./data/tokenizer_small
./data/tokenizer_small_test
./data/training_data_small.npy
./data/training_data_small_test.npy
./data/validation_data_small.npy
./data/validation_data_small_test.npy
./data_processing/__init__.py
./data_processing/__pycache__/__init__.cpython-311.pyc
./data_processing/__pycache__/deduplicate.cpython-311.pyc
./data_processing/__pycache__/harmful_detect.cpython-311.pyc
./data_processing/__pycache__/html_process.cpython-311.pyc
./data_processing/__pycache__/language_identification.cpython-311.pyc
./data_processing/__pycache__/mask_pii.cpython-311.pyc
./data_processing/__pycache__/quality_classfier.cpython-311.pyc
./data_processing/__pycache__/quality_filter.cpython-311.pyc
./data_processing/deduplicate.py
./data_processing/harmful_detect.py
./data_processing/html_process.py
./data_processing/language_identification.py
./data_processing/mask_pii.py
./data_processing/quality_classfier.py
./data_processing/quality_filter.py
./doc.mk
./doc_scripts/__pycache__/export_platform_posts.cpython-311.pyc
./doc_scripts/__pycache__/sync_lark_doc.cpython-311.pyc
./doc_scripts/export_platform_posts.py
./doc_scripts/sync_lark_doc.py
./docs/source/_templates/footer.html
./docs/source/assets/images/02-llm/image-01.png
./docs/source/assets/images/02-llm/image-02.png
./docs/source/assets/images/02-llm/image-03.png
./docs/source/assets/images/02-llm/image-04.webp
./docs/source/assets/images/02-llm/image-05.png
./docs/source/assets/images/03-bpe-tokenizer/image-01.png
./docs/source/assets/images/04-transformer-decoder-only/image-01.png
./docs/source/assets/images/04-transformer-decoder-only/image-02.png
./docs/source/assets/images/04-transformer-decoder-only/image-03.png
./docs/source/assets/images/04-transformer-decoder-only/image-04.png
./docs/source/assets/images/04-transformer-decoder-only/image-05.png
./docs/source/assets/images/04-transformer-decoder-only/image-06.png
./docs/source/assets/images/04-transformer-decoder-only/image-07.png
./docs/source/assets/images/04-transformer-decoder-only/image-08.png
./docs/source/assets/images/05-attention-alternatives-moe/image-01.png
./docs/source/assets/images/05-attention-alternatives-moe/image-02.png
./docs/source/assets/images/05-attention-alternatives-moe/image-03.png
./docs/source/assets/images/05-attention-alternatives-moe/image-04.png
./docs/source/assets/images/06-chapter/image-01.png
./docs/source/assets/images/06-chapter/image-02.png
./docs/source/assets/images/06-chapter/image-03.png
./docs/source/assets/images/06-chapter/image-04.png
./docs/source/assets/images/06-chapter/image-05.png
./docs/source/assets/images/06-chapter/image-06.png
./docs/source/assets/images/06-chapter/image-07.png
./docs/source/assets/images/06-chapter/image-08.png
./docs/source/assets/images/06-chapter/image-09.png
./docs/source/assets/images/06-chapter/image-10.png
./docs/source/assets/images/06-chapter/image-11.png
./docs/source/assets/images/07-chapter/image-01.png
./docs/source/assets/images/07-chapter/image-02.png
./docs/source/assets/images/07-chapter/image-03.png
./docs/source/assets/images/07-chapter/image-04.png
./docs/source/assets/images/07-chapter/image-05.png
./docs/source/assets/images/07-chapter/image-06.png
./docs/source/assets/images/07-chapter/image-07.png
./docs/source/assets/images/07-chapter/image-08.png
./docs/source/assets/images/07-chapter/image-09.png
./docs/source/assets/images/07-chapter/image-10.png
./docs/source/assets/images/07-chapter/image-11.png
./docs/source/assets/images/07-chapter/image-12.png
./docs/source/assets/images/07-chapter/image-13.png
./docs/source/assets/images/07-chapter/image-14.png
./docs/source/assets/images/07-chapter/image-15.png
./docs/source/assets/images/07-chapter/image-16.png
./docs/source/assets/images/07-chapter/image-17.png
./docs/source/assets/images/07-chapter/image-18.png
./docs/source/assets/images/08-scaling-laws/image-01.png
./docs/source/assets/images/08-scaling-laws/image-02.png
./docs/source/assets/images/08-scaling-laws/image-03.png
./docs/source/assets/images/08-scaling-laws/image-04.png
./docs/source/assets/images/08-scaling-laws/image-05.png
./docs/source/assets/images/08-scaling-laws/image-06.png
./docs/source/assets/images/08-scaling-laws/image-07.png
./docs/source/assets/images/08-scaling-laws/image-08.png
./docs/source/assets/images/10-chapter/image-01.png
./docs/source/assets/images/10-chapter/image-02.png
./docs/source/assets/images/10-chapter/image-03.png
./docs/source/assets/images/10-chapter/image-04.png
./docs/source/assets/images/10-chapter/image-05.png
./docs/source/assets/images/10-chapter/image-06.png
./docs/source/assets/images/10-chapter/image-07.png
./docs/source/assets/images/10-chapter/image-08.png
./docs/source/assets/images/11-chapter/image-01.png
./docs/source/assets/images/11-chapter/image-02.png
./docs/source/assets/images/11-chapter/image-03.png
./docs/source/assets/images/11-chapter/image-04.png
./docs/source/assets/images/11-chapter/image-05.png
./docs/source/assets/images/11-chapter/image-06.png
./docs/source/assets/images/12-sft/image-01.png
./docs/source/assets/images/12-sft/image-02.png
./docs/source/assets/images/12-sft/image-03.png
./docs/source/assets/images/13-rlhf/image-01.png
./docs/source/assets/images/13-rlhf/image-02.png
./docs/source/assets/images/13-rlhf/image-03.png
./docs/source/assets/images/13-rlhf/image-04.png
./docs/source/assets/images/13-rlhf/image-05.png
./docs/source/assets/images/14-rlvr/image-01.png
./docs/source/assets/images/14-rlvr/image-02.png
./docs/source/assets/images/14-rlvr/image-03.png
./docs/source/assets/images/14-rlvr/image-04.png
./docs/source/assets/images/14-rlvr/image-05.png
./docs/source/assets/images/14-rlvr/image-06.png
./docs/source/assets/images/15-chapter/image-01.png
./docs/source/assets/images/15-chapter/image-02.png
./docs/source/assets/images/15-chapter/image-03.png
./docs/source/assets/images/15-chapter/image-04.png
./docs/source/assets/images/15-chapter/image-05.png
./docs/source/assets/images/15-chapter/image-06.png
./docs/source/assets/images/15-chapter/image-07.png
./docs/source/assets/images/15-chapter/image-08.png
./docs/source/chapters/01-build-llm-from-scratch.md
./docs/source/chapters/02-llm.md
./docs/source/chapters/03-bpe-tokenizer.md
./docs/source/chapters/04-transformer-decoder-only.md
./docs/source/chapters/05-attention-alternatives-moe.md
./docs/source/chapters/06-chapter.md
./docs/source/chapters/07-chapter.md
./docs/source/chapters/08-scaling-laws.md
./docs/source/chapters/09-chapter.md
./docs/source/chapters/10-chapter.md
./docs/source/chapters/11-chapter.md
./docs/source/chapters/12-sft.md
./docs/source/chapters/13-rlhf.md
./docs/source/chapters/14-rlvr.md
./docs/source/chapters/15-chapter.md
./docs/source/chapters/16-chapter.md
./docs/source/chapters/17-chapter.md
./docs/source/conf.py
./docs/source/index.md
./FOLDERS_DESCRIPTION.md
./img/loss.png
./img/lr.png
./install.sh
./kernel/__init__.py
./kernel/__pycache__/__init__.cpython-311.pyc
./kernel/__pycache__/flash_attention_mock.cpython-311.pyc
./kernel/__pycache__/flash_attention_triton.cpython-311.pyc
./kernel/flash_attention_mock.py
./kernel/flash_attention_triton.py
./llm/__init__.py
./llm/__pycache__/__init__.cpython-311.pyc
./llm/__pycache__/__init__.cpython-312.pyc
./llm/__pycache__/args.cpython-311.pyc
./llm/__pycache__/args.cpython-312.pyc
./llm/__pycache__/bpe_tokenizer.cpython-311.pyc
./llm/__pycache__/bpe_tokenizer.cpython-312.pyc
./llm/__pycache__/checkpoint.cpython-311.pyc
./llm/__pycache__/checkpoint.cpython-312.pyc
./llm/__pycache__/generating.cpython-311.pyc
./llm/__pycache__/training.cpython-311.pyc
./llm/__pycache__/training.cpython-312.pyc
./llm/__pycache__/transformer.cpython-311.pyc
./llm/__pycache__/transformer.cpython-312.pyc
./llm/args.py
./llm/bpe_tokenizer.py
./llm/checkpoint.py
./llm/generating.py
./llm/training.py
./llm/transformer.py
./nul
./parallel/__init__.py
./parallel/__pycache__/__init__.cpython-311.pyc
./parallel/__pycache__/__init__.cpython-312.pyc
./parallel/__pycache__/ddp.cpython-311.pyc
./parallel/__pycache__/ddp.cpython-312.pyc
./parallel/__pycache__/sharded_optimizer.cpython-311.pyc
./parallel/__pycache__/sharded_optimizer.cpython-312.pyc
./parallel/ddp.py
./parallel/sharded_optimizer.py
./PROJECT_REPORT.md
./pyproject.toml
./README.md
./README_cn.md
./requirements-docs.txt
./site/.npmrc
./site/astro.config.mjs
./site/package.json
./site/package-lock.json
./site/playwright.config.ts
./site/public/favicon.svg
./site/public/images/loss.png
./site/public/images/lr.png
./site/src/components/ArchitectureFlow.astro
./site/src/components/DocsChapterNav.astro
./site/src/components/FeaturePortalGrid.astro
./site/src/components/HeroBackground.astro
./site/src/components/HeroSection.astro
./site/src/components/MermaidInit.astro
./site/src/components/MetricCards.astro
./site/src/components/ProofBand.astro
./site/src/components/SectionIntro.astro
./site/src/components/SiteFooter.astro
./site/src/components/SiteHeader.astro
./site/src/content/site.ts
./site/src/layouts/BaseLayout.astro
./site/src/layouts/DocsLayout.astro
./site/src/lib/docs.ts
./site/src/lib/locale.ts
./site/src/pages/architecture.astro
./site/src/pages/benchmarks.astro
./site/src/pages/docs/[slug].astro
./site/src/pages/docs/index.astro
./site/src/pages/index.astro
./site/src/pages/sft-rlft.astro
./site/src/pages/zh/architecture.astro
./site/src/pages/zh/benchmarks.astro
./site/src/pages/zh/docs/[slug].astro
./site/src/pages/zh/docs/index.astro
./site/src/pages/zh/index.astro
./site/src/pages/zh/sft-rlft.astro
./site/src/styles/global.css
./site/tests/content.spec.ts
./site/tests/docs.spec.ts
./site/tests/e2e/site.spec.ts
./site/tests/package-lock.spec.ts
./site/tests/routes.spec.ts
./site/tsconfig.json
./test_generate.py
./tests/__init__.py
./tests/__pycache__/__init__.cpython-311.pyc
./tests/__pycache__/adapters.cpython-311.pyc
./tests/__pycache__/common.cpython-311.pyc
./tests/__pycache__/conftest.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_attention.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_data.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_ddp.cpython-311.pyc
./tests/__pycache__/test_ddp.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_ddp_individual_parameters.cpython-311.pyc
./tests/__pycache__/test_ddp_individual_parameters.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_deduplication.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_dpo.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_export_platform_posts.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_extract.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_generating.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_grpo.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_langid.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_metrics.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_model.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_nn_utils.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_optimizer.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_pii.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_quality.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_serialization.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_sft.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_sharded_optimizer.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_sync_lark_doc.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_tokenizer.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_toxicity.cpython-311-pytest-8.4.1.pyc
./tests/__pycache__/test_train_bpe.cpython-311-pytest-8.4.1.pyc
./tests/_snapshots/test_4d_scaled_dot_product_attention.npz
./tests/_snapshots/test_adamw.npz
./tests/_snapshots/test_compute_entropy.npz
./tests/_snapshots/test_compute_group_normalized_rewards_no_normalize_by_std.npz
./tests/_snapshots/test_compute_group_normalized_rewards_normalize_by_std.npz
./tests/_snapshots/test_compute_grpo_clip_loss_large_cliprange.npz
./tests/_snapshots/test_compute_grpo_clip_loss_small_cliprange.npz
./tests/_snapshots/test_compute_naive_policy_gradient_loss.npz
./tests/_snapshots/test_compute_policy_gradient_loss_grpo_clip.npz
./tests/_snapshots/test_compute_policy_gradient_loss_no_baseline.npz
./tests/_snapshots/test_compute_policy_gradient_loss_reinforce_with_baseline.npz
./tests/_snapshots/test_embedding.npz
./tests/_snapshots/test_get_response_log_probs.npz
./tests/_snapshots/test_grpo_microbatch_train_step_grpo_clip.npz
./tests/_snapshots/test_grpo_microbatch_train_step_grpo_clip_10_steps.npz
./tests/_snapshots/test_linear.npz
./tests/_snapshots/test_masked_mean_dim0.npz
./tests/_snapshots/test_masked_mean_dim1.npz
./tests/_snapshots/test_masked_mean_dimlast.npz
./tests/_snapshots/test_masked_mean_dimNone.npz
./tests/_snapshots/test_masked_normalize_dim0.npz
./tests/_snapshots/test_masked_normalize_dim1.npz
./tests/_snapshots/test_masked_normalize_dimlast.npz
./tests/_snapshots/test_masked_normalize_dimNone.npz
./tests/_snapshots/test_multihead_self_attention.npz
./tests/_snapshots/test_multihead_self_attention_with_rope.npz
./tests/_snapshots/test_positionwise_feedforward.npz
./tests/_snapshots/test_rmsnorm.npz
./tests/_snapshots/test_rope.npz
./tests/_snapshots/test_scaled_dot_product_attention.npz
./tests/_snapshots/test_sft_microbatch_train_step.npz
./tests/_snapshots/test_sft_microbatch_train_step_10_steps.npz
./tests/_snapshots/test_sft_microbatch_train_step_normalize.npz
./tests/_snapshots/test_swiglu.npz
./tests/_snapshots/test_tokenize_prompt_and_output.npz
./tests/_snapshots/test_train_bpe_special_tokens.pkl
./tests/_snapshots/test_transformer_block.npz
./tests/_snapshots/test_transformer_lm.npz
./tests/_snapshots/test_transformer_lm_truncated_input.npz
./tests/adapters.py
./tests/common.py
./tests/conftest.py
./tests/fixtures/address.txt
./tests/fixtures/corpus.en
./tests/fixtures/ddp_test_data.pt
./tests/fixtures/ddp_test_labels.pt
./tests/fixtures/documents_line_deduplicated/doc1.txt
./tests/fixtures/documents_line_deduplicated/doc2.txt
./tests/fixtures/documents_line_deduplicated/doc3.txt
./tests/fixtures/documents_line_deduplicated/doc4.txt
./tests/fixtures/documents_line_deduplicated/doc5.txt
./tests/fixtures/documents_with_fuzzy_duplicates/pytorch_license.txt
./tests/fixtures/documents_with_fuzzy_duplicates/rails_mit_license.txt
./tests/fixtures/documents_with_fuzzy_duplicates/react_mit_license.txt
./tests/fixtures/documents_with_line_duplicates/doc1.txt
./tests/fixtures/documents_with_line_duplicates/doc2.txt
./tests/fixtures/documents_with_line_duplicates/doc3.txt
./tests/fixtures/documents_with_line_duplicates/doc4.txt
./tests/fixtures/documents_with_line_duplicates/doc5.txt
./tests/fixtures/german.txt
./tests/fixtures/gpt2_merges.txt
./tests/fixtures/gpt2_vocab.json
./tests/fixtures/high_quality_wiki_reference.txt
./tests/fixtures/low_quality_cc.txt
./tests/fixtures/Meta-Llama-3-8B/special_tokens_map.json
./tests/fixtures/Meta-Llama-3-8B/tokenizer.json
./tests/fixtures/Meta-Llama-3-8B/tokenizer_config.json
./tests/fixtures/moby.html
./tests/fixtures/moby_extracted.txt
./tests/fixtures/sft_sample.jsonl
./tests/fixtures/special_token_double_newlines_non_whitespace.txt
./tests/fixtures/special_token_trailing_newlines.txt
./tests/fixtures/tiny-gpt2/config.json
./tests/fixtures/tiny-gpt2/generation_config.json
./tests/fixtures/tiny-gpt2/model.safetensors
./tests/fixtures/tiny-gpt2-ref/config.json
./tests/fixtures/tiny-gpt2-ref/generation_config.json
./tests/fixtures/tiny-gpt2-ref/model.safetensors
./tests/fixtures/tinystories_sample.txt
./tests/fixtures/tinystories_sample_5M.txt
./tests/fixtures/tokenized_sft_sample.json
./tests/fixtures/train-bpe-reference-merges.txt
./tests/fixtures/train-bpe-reference-vocab.json
./tests/fixtures/ts_tests/model.pt
./tests/fixtures/ts_tests/model_config.json
./tests/test_attention.py
./tests/test_data.py
./tests/test_ddp.py
./tests/test_ddp_individual_parameters.py
./tests/test_deduplication.py
./tests/test_dpo.py
./tests/test_export_platform_posts.py
./tests/test_extract.py
./tests/test_generating.py
./tests/test_grpo.py
./tests/test_langid.py
./tests/test_metrics.py
./tests/test_model.py
./tests/test_nn_utils.py
./tests/test_optimizer.py
./tests/test_pii.py
./tests/test_quality.py
./tests/test_serialization.py
./tests/test_sft.py
./tests/test_sharded_optimizer.py
./tests/test_sync_lark_doc.py
./tests/test_tokenizer.py
./tests/test_toxicity.py
./tests/test_train_bpe.py
./train_quick.py
./train_quick_fixed.py
./train_simple.py
./TRAINING_GUIDE.md
./uv.lock
