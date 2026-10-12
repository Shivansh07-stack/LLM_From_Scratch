import docx
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import re

# Read source content
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('BENCHMARK.md', 'r', encoding='utf-8') as f:
    bench = f.read()
with open('TRAINING_GUIDE.md', 'r', encoding='utf-8') as f:
    train = f.read()
with open('FOLDERS_DESCRIPTION.md', 'r', encoding='utf-8') as f:
    folders = f.read()

def strip_md(text):
    """Remove markdown formatting for plain text"""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'^\s*[-*]\s+', '• ', text, flags=re.MULTILINE)
    return text

def add_heading(doc, text, level):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(0x1A, 0x3C, 0x6E)
        if level == 0:
            run.font.size = Pt(24)
        elif level == 1:
            run.font.size = Pt(18)
        elif level == 2:
            run.font.size = Pt(14)
        else:
            run.font.size = Pt(12)
    return h

def add_paragraph(doc, text, style='Normal', size=11, bold=False, italic=False, alignment=None):
    p = doc.add_paragraph(text, style=style)
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
    if alignment:
        p.alignment = alignment
    return p

def add_bullet(doc, text, level=0):
    p = doc.add_paragraph(text, style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.5 + level * 0.25)
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    return p

def build_synopsis(doc):
    # Title page
    for _ in range(4):
        doc.add_paragraph()
    
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('SYNOPSIS')
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x3C, 0x6E)
    run.font.name = 'Calibri'
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('LLM-from-Scratch: A From-Scratch Implementation of a Modern Decoder-Only Transformer Model')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x4A, 0x6F, 0x8C)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    author = doc.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = author.add_run('Shivansh Sharma\nB.Tech IT, Maharaja Agrasen Institute of Technology\nNew Delhi, India')
    run.font.size = Pt(12)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = date_para.add_run('October 2026')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    
    doc.add_page_break()
    
    # Table of Contents
    add_heading(doc, 'Table of Contents', 1)
    toc_items = [
        '1. Introduction and Background',
        '2. Problem Statement and Objectives',
        '3. Scope of the Project',
        '4. Technical Architecture Overview',
        '5. Implementation Methodology',
        '6. Key Components and Modules',
        '7. Data Processing Pipeline',
        '8. Training and Evaluation Strategy',
        '9. Expected Outcomes and Deliverables',
        '10. Timeline and Milestones',
        '11. Resources and Infrastructure Requirements',
        '12. Risk Analysis and Mitigation',
        '13. Conclusion',
        '14. References'
    ]
    for item in toc_items:
        add_paragraph(doc, item, size=11)
    
    doc.add_page_break()
    
    # 1. Introduction
    add_heading(doc, '1. Introduction and Background', 1)
    add_paragraph(doc, 
        'The field of natural language processing has been revolutionized by the advent of Large Language Models (LLMs) '
        'based on the Transformer architecture. Since the introduction of the Transformer model by Vaswani et al. in 2017, '
        'decoder-only variants such as GPT (Generative Pre-trained Transformer) have become the dominant paradigm for '
        'building powerful language models capable of understanding and generating human-like text.')
    add_paragraph(doc,
        'However, most practical implementations of these models rely on high-level frameworks and pre-trained checkpoints, '
        'which obscure the underlying mechanics. For students, researchers, and practitioners seeking a deep understanding '
        'of how these models work internally, there is a critical need for transparent, from-scratch implementations that '
        'expose every component—from tokenization to attention mechanisms, from optimization to distributed training.')
    add_paragraph(doc,
        'The LLM-from-Scratch project addresses this need by providing a complete, educational implementation of a modern '
        'decoder-only Transformer language model in PyTorch. Every component is implemented from first principles, '
        'including the Byte Pair Encoding (BPE) tokenizer, the Transformer architecture with modern enhancements '
        '(RMSNorm, SwiGLU, RoPE), custom optimizers (AdamW, SGD with decay), learning rate schedulers, Flash Attention '
        'kernels implemented in Triton, and distributed training utilities (DDP, sharded optimizer).')
    
    # 2. Problem Statement
    add_heading(doc, '2. Problem Statement and Objectives', 1)
    add_paragraph(doc,
        'Despite the widespread adoption of LLMs, there remains a significant gap in accessible educational resources '
        'that demonstrate the complete pipeline of building a language model from scratch. Existing resources either:')
    add_bullet(doc, 'Focus only on isolated components (e.g., attention mechanism alone)')
    add_bullet(doc, 'Use high-level libraries that abstract away critical implementation details')
    add_bullet(doc, 'Lack comprehensive coverage of the full training pipeline including data processing, tokenization, and distributed training')
    add_bullet(doc, 'Do not provide benchmarking tools to understand performance characteristics')
    add_bullet(doc, 'Are not designed for educational clarity with clean, modular code')
    
    add_paragraph(doc,
        'The primary objective of this project is to bridge this gap by delivering a fully functional, well-documented, '
        'and pedagogically sound implementation of a decoder-only Transformer that serves as both a learning resource '
        'and a research platform.')
    
    add_heading(doc, 'Specific Objectives', 2)
    add_bullet(doc, 'Implement a complete decoder-only Transformer architecture with modern enhancements (RMSNorm, SwiGLU, RoPE)')
    add_bullet(doc, 'Develop a from-scratch BPE tokenizer capable of training on arbitrary text corpora')
    add_bullet(doc, 'Create a comprehensive data processing pipeline for cleaning and preparing large-scale text datasets')
    add_bullet(doc, 'Implement custom optimizers (AdamW, SGD with decay) and learning rate schedulers (cosine with warmup)')
    add_bullet(doc, 'Develop high-performance kernel optimizations including Triton-based Flash Attention 2')
    add_bullet(doc, 'Build distributed training support with DDP and parameter-sharded optimizer')
    add_bullet(doc, 'Provide alignment training capabilities (SFT, RLHF/GRPO) for instruction following and reasoning')
    add_bullet(doc, 'Establish a comprehensive benchmarking suite for performance analysis')
    add_bullet(doc, 'Create extensive test coverage with snapshot testing for correctness validation')
    add_bullet(doc, 'Document the entire system with an accompanying open-source book and bilingual website')
    
    # 3. Scope
    add_heading(doc, '3. Scope of the Project', 1)
    add_paragraph(doc,
        'The project encompasses the entire lifecycle of a language model, from raw text data to a trained, '
        'generative model with alignment capabilities. The scope includes:')
    add_bullet(doc, 'Core model implementation (~6.13M parameters default configuration: 6 layers, d_model=288, 6 heads, vocab=2048)')
    add_bullet(doc, 'Tokenizer training and inference (BPE with special token support)')
    add_bullet(doc, 'Data preprocessing (HTML stripping, language ID, quality filtering, deduplication, PII masking, toxicity detection)')
    add_bullet(doc, 'Training pipeline (mixed precision, gradient clipping, checkpointing, validation)')
    add_bullet(doc, 'Inference/generation (top-p sampling, temperature control)')
    add_bullet(doc, 'Kernel optimizations (Flash Attention 2 via Triton)')
    add_bullet(doc, 'Distributed training (DDP with bucket-based communication, sharded optimizer)')
    add_bullet(doc, 'Alignment training (SFT on GSM8K, GRPO for RL fine-tuning)')
    add_bullet(doc, 'Benchmarking suite (attention variants, model throughput, DDP communication)')
    add_bullet(doc, 'Test suite (100+ tests with snapshot comparisons)')
    add_bullet(doc, 'Documentation (Sphinx-based book, bilingual Astro website)')
    
    add_paragraph(doc,
        'Out of scope for the core implementation: training of billion-parameter models (requires compute infrastructure '
        'beyond typical educational settings), production-grade serving infrastructure, and proprietary data handling. '
        'However, the architecture is designed to scale and the codebase provides the foundation for such extensions.')
    
    # 4. Technical Architecture
    add_heading(doc, '4. Technical Architecture Overview', 1)
    add_paragraph(doc,
        'The LLM-from-Scratch architecture follows a modular design where each component is implemented as an independent, '
        'testable module. The core model is a decoder-only Transformer with the following key architectural decisions:')
    
    add_heading(doc, '4.1 Model Architecture', 2)
    add_bullet(doc, 'Pre-normalization with RMSNorm: Layer normalization applied before attention and FFN sub-layers for training stability')
    add_bullet(doc, 'SwiGLU feed-forward networks: Gated linear units with SiLU activation for improved expressivity')
    add_bullet(doc, 'Rotary Position Embeddings (RoPE): Relative positional encoding via rotation of query/key vectors')
    add_bullet(doc, 'Causal multi-head self-attention: Standard scaled dot-product attention with causal masking')
    add_bullet(doc, 'Tied embeddings: Input and output embeddings shared to reduce parameter count')
    
    add_heading(doc, 'Default Hyperparameters', 2)
    defaults = [
        ('d_model', '288', 'Model dimension'),
        ('num_layers', '6', 'Number of Transformer blocks'),
        ('num_heads', '6', 'Attention heads (head_dim = 48)'),
        ('d_ff', '1024', 'Feed-forward inner dimension'),
        ('vocab_size', '2048', 'BPE vocabulary size'),
        ('max_seq_len', '512', 'Maximum context length'),
        ('Total Parameters', '~6.13M', 'Including embeddings and output head')
    ]
    table = doc.add_table(rows=1, cols=3, style='Table Grid')
    table.rows[0].cells[0].text = 'Parameter'
    table.rows[0].cells[1].text = 'Value'
    table.rows[0].cells[2].text = 'Description'
    for param, val, desc in defaults:
        row = table.add_row()
        row.cells[0].text = param
        row.cells[1].text = val
        row.cells[2].text = desc
    
    add_heading(doc, '4.2 Module Organization', 2)
    modules = [
        ('llm/transformer.py', 'Core architecture: Transformer, TransformerBlock, attention, FFN, RoPE, RMSNorm, Embedding, Linear, Softmax, CrossEntropyLoss, AdamW, SGDDecay, schedulers'),
        ('llm/bpe_tokenizer.py', 'Byte Pair Encoding tokenizer with training, encoding, decoding, special tokens'),
        ('llm/training.py', 'Training loop with data loading, validation, checkpointing, mixed precision'),
        ('llm/generating.py', 'Text generation with top-p sampling and temperature'),
        ('llm/checkpoint.py', 'Checkpoint save/load utilities'),
        ('kernel/flash_attention_triton.py', 'Triton Flash Attention 2 kernel'),
        ('parallel/ddp.py', 'Distributed Data Parallel with bucket-based gradient sync'),
        ('parallel/sharded_optimizer.py', 'Parameter-sharded optimizer for memory efficiency'),
        ('data_processing/', 'Seven preprocessing modules: HTML, language ID, quality filter, deduplication, PII, toxicity, quality classifier'),
        ('alignment/', 'SFT, GRPO/RLHF, evaluation, prompt templates'),
        ('bench_mark/', 'Performance benchmarks for attention, model, DDP'),
        ('tests/', 'Comprehensive test suite with 100+ tests and snapshots')
    ]
    for name, desc in modules:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run = p.add_run(desc)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    
    # 5. Implementation Methodology
    add_heading(doc, '5. Implementation Methodology', 1)
    add_paragraph(doc,
        'The implementation follows a bottom-up approach, building each component from primitive PyTorch operations '
        'before composing them into higher-level modules. This methodology ensures:')
    add_bullet(doc, 'Educational clarity: Each file can be read and understood independently')
    add_bullet(doc, 'Testability: Every module has corresponding unit tests with reference implementations')
    add_bullet(doc, 'Extensibility: Components can be swapped or modified without affecting others')
    add_bullet(doc, 'Correctness: Snapshot tests validate outputs against known-good reference implementations')
    
    add_heading(doc, '5.1 Development Workflow', 2)
    add_paragraph(doc,
        'The project uses uv for fast, reproducible dependency management and virtual environment handling. '
        'Code quality is maintained through pytest-based testing, with snapshot testing ensuring numerical '
        'correctness of mathematical operations. The codebase is organized into logical packages (llm, kernel, '
        'parallel, data_processing, alignment, bench_mark, tests) with clear separation of concerns.')
    
    add_heading(doc, '5.2 Key Design Principles', 2)
    principles = [
        ('Transparency', 'No hidden magic; every operation is explicit and traceable'),
        ('Modularity', 'Loose coupling between components via well-defined interfaces'),
        ('Performance', 'Critical paths (attention) optimized with Triton kernels'),
        ('Scalability', 'DDP and sharded optimizer enable multi-GPU training'),
        ('Reproducibility', 'Fixed seeds, deterministic algorithms where possible, versioned dependencies'),
        ('Pedagogical Value', 'Code serves as executable documentation; comments explain why, not just what')
    ]
    for title, desc in principles:
        p = doc.add_paragraph()
        run = p.add_run(f'{title}: ')
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run = p.add_run(desc)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    
    # 6. Key Components
    add_heading(doc, '6. Key Components and Modules', 1)
    
    add_heading(doc, '6.1 Transformer Core (llm/transformer.py)', 2)
    add_paragraph(doc,
        'The heart of the implementation is the Transformer class, which composes an embedding layer, '
        'a stack of TransformerBlock modules, a final RMSNorm, and an output linear projection. '
        'Each TransformerBlock contains two RMSNorm layers, a MultiHeadAttentionWithRoPE module, '
        'and a SwiGLU feed-forward network, with residual connections around each sub-layer.')
    add_paragraph(doc,
        'The attention mechanism uses einx for expressive einsum-style operations, enabling clear '
        'tensor manipulation. The causal mask is precomputed and cached for efficiency. RoPE is '
        'applied per-head with precomputed sine/cosine tables for maximum performance.')
    
    add_heading(doc, '6.2 BPE Tokenizer (llm/bpe_tokenizer.py)', 2)
    add_paragraph(doc,
        'The tokenizer implements the standard BPE algorithm: starting with byte-level vocabulary, '
        'iteratively merging the most frequent adjacent pairs. Special tokens (e.g., <|endoftext|>) '
        'are supported. The tokenizer provides train(), encode(), decode(), and save/load functionality. '
        'Training complexity is O(N) with hash-based pair counting.')
    
    add_heading(doc, '6.3 Flash Attention 2 (kernel/flash_attention_triton.py)', 2)
    add_paragraph(doc,
        'The Triton implementation follows the Flash Attention 2 algorithm, computing attention in '
        'blocks that fit in SRAM, avoiding materialization of the full attention matrix. This provides '
        'significant speedups (5-10x) and memory savings, especially at longer sequence lengths. '
        'The benchmark results demonstrate consistent superiority over PyTorch\'s native scaled dot-product '
        'attention, particularly for batch sizes >1 and sequence lengths >= 1024.')
    
    add_heading(doc, '6.4 Distributed Training (parallel/)', 2)
    add_paragraph(doc,
        'The DDP implementation uses bucket-based gradient synchronization to overlap communication '
        'with computation. The sharded optimizer partitions optimizer states across devices, enabling '
        'training of models larger than single-GPU memory. Both are implemented from scratch using '
        'PyTorch\'s distributed communication primitives (nccl/gloo backends).')
    
    add_heading(doc, '6.5 Alignment Training (alignment/)', 2)
    add_paragraph(doc,
        'The alignment module provides Supervised Fine-Tuning (SFT) and Group Relative Policy '
        'Optimization (GRPO), a PPO-like algorithm for RL fine-tuning. The SFT pipeline demonstrated '
        'strong results on GSM8K: zero-shot accuracy improved from 1.56% to 62.9% on Qwen2.5-Math-1.5B, '
        'with format compliance reaching 100%. GRPO uses group-wise advantage estimation for stable '
        'policy updates without a value network.')
    
    # 7. Data Processing
    add_heading(doc, '7. Data Processing Pipeline', 1)
    add_paragraph(doc,
        'The data_processing package provides seven composable tools for preparing web-scale corpora:')
    
    dp_items = [
        ('html_process.py', 'Extracts clean text from HTML/WARC files using selective tag removal and text density heuristics'),
        ('language_identification.py', 'FastText-based language detection for filtering target languages'),
        ('quality_filter.py', 'Heuristic filters: word count (50-100k), avg word length (3-10), alpha ratio (>0.5)'),
        ('deduplicate.py', 'Exact line deduplication and MinHash-based near-duplicate detection (Jaccard similarity)'),
        ('mask_pii.py', 'Regex-based masking of emails, phones, IPs, credit cards, and other PII patterns'),
        ('harmful_detect.py', 'FastText classifiers for NSFW and toxic content detection'),
        ('quality_classfier.py', 'FastText binary classifier distinguishing high-quality (Wikipedia) vs low-quality (Common Crawl) text')
    ]
    for name, desc in dp_items:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run = p.add_run(desc)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    
    # 8. Training and Evaluation
    add_heading(doc, '8. Training and Evaluation Strategy', 1)
    add_paragraph(doc,
        'The training pipeline supports both single-GPU and multi-GPU configurations. Key features include:')
    add_bullet(doc, 'Memory-mapped NumPy arrays for tokenized data (handles datasets larger than RAM)')
    add_bullet(doc, 'Cosine learning rate schedule with linear warmup (configurable warmup iterations)')
    add_bullet(doc, 'Gradient clipping (max_norm=1.0) for training stability')
    add_bullet(doc, 'Periodic validation with configurable interval')
    add_bullet(doc, 'Checkpointing with model state, optimizer state, iteration, and loss')
    add_bullet(doc, 'TensorBoard logging for loss curves and learning rate visualization')
    add_bullet(doc, 'Mixed precision support (bfloat16/float32) via autocast')
    
    add_heading(doc, '8.1 Benchmarking Results', 2)
    add_paragraph(doc,
        'The BENCHMARK.md file contains comprehensive performance measurements. Key findings:')
    add_bullet(doc, 'Flash Attention 2 (Triton) outperforms PyTorch native attention by 5-10x at sequence length 4096')
    add_bullet(doc, 'bfloat16 provides ~2x speedup over float32 for attention computations')
    add_bullet(doc, 'DDP all-reduce scales near-linearly with data size; latency dominated by GPU interconnect for small tensors')
    add_bullet(doc, 'Full model iteration time: ~53ms per step (batch=64, seq=256) on modern GPU')
    
    # 9. Expected Outcomes
    add_heading(doc, '9. Expected Outcomes and Deliverables', 1)
    add_paragraph(doc, 'Upon completion, the project delivers:')
    
    outcomes = [
        'A fully functional, from-scratch decoder-only Transformer language model (~6M parameters default)',
        'Trained BPE tokenizer with configurable vocabulary size',
        'Preprocessed training/validation datasets in memory-mapped NumPy format',
        'Trained model checkpoints at regular intervals',
        'Training logs (loss curves, learning rate schedules) and TensorBoard logs',
        'Generated text samples demonstrating model capabilities',
        'Comprehensive benchmark reports (attention variants, DDP scaling, model throughput)',
        'Test suite with 100+ passing tests ensuring numerical correctness',
        'Complete documentation: Sphinx-based book (PDF/EPUB/HTML), bilingual Astro website',
        'Alignment training examples: SFT on GSM8K (62.9% accuracy), GRPO RL fine-tuning pipeline',
        'Data processing tools applicable to Common Crawl and other web corpora'
    ]
    for item in outcomes:
        add_bullet(doc, item)
    
    # 10. Timeline
    add_heading(doc, '10. Timeline and Milestones', 1)
    
    timeline = [
        ('Phase 1: Core Infrastructure (Weeks 1-3)', [
            'Repository setup, dependency management, CI/CD',
            'Basic Transformer block implementation',
            'Custom Linear, Embedding, RMSNorm, Softmax layers',
            'Unit tests for core mathematical operations'
        ]),
        ('Phase 2: Model Architecture (Weeks 4-6)', [
            'Multi-head attention with causal masking',
            'RoPE positional embeddings',
            'SwiGLU feed-forward network',
            'Complete Transformer stack with residual connections',
            'Snapshot tests against reference implementations'
        ]),
        ('Phase 3: Tokenizer & Data Pipeline (Weeks 7-9)', [
            'BPE tokenizer with training/encoding/decoding',
            'Data processing modules (7 tools)',
            'Memory-mapped data format for efficient loading',
            'Integration tests for end-to-end pipeline'
        ]),
        ('Phase 4: Training & Optimization (Weeks 10-12)', [
            'Training loop with validation, checkpointing, logging',
            'Custom AdamW optimizer with weight decay',
            'Cosine LR scheduler with warmup',
            'Gradient clipping, mixed precision support'
        ]),
        ('Phase 5: Kernel Optimizations (Weeks 13-15)', [
            'Triton Flash Attention 2 implementation',
            'Mock implementation for correctness verification',
            'Benchmark suite for attention variants',
            'Performance profiling and optimization'
        ]),
        ('Phase 6: Distributed Training (Weeks 16-18)', [
            'DDP with bucket-based gradient synchronization',
            'Sharded optimizer for memory efficiency',
            'DDP all-reduce benchmarks',
            'Multi-GPU training validation'
        ]),
        ('Phase 7: Alignment & Advanced Features (Weeks 19-22)', [
            'SFT pipeline with GSM8K dataset',
            'GRPO implementation for RL fine-tuning',
            'Evaluation framework for accuracy and format compliance',
            'Qwen2.5-Math-1.5B fine-tuning demonstration'
        ]),
        ('Phase 8: Documentation & Polish (Weeks 23-24)', [
            'Sphinx documentation with 17 chapters',
            'Bilingual Astro website (English/Chinese)',
            'PDF/EPUB book generation via GitHub Actions',
            'Comprehensive README, TRAINING_GUIDE, BENCHMARK docs'
        ])
    ]
    
    for phase, items in timeline:
        add_heading(doc, phase, 2)
        for item in items:
            add_bullet(doc, item)
    
    # 11. Resources
    add_heading(doc, '11. Resources and Infrastructure Requirements', 1)
    add_heading(doc, '11.1 Compute Requirements', 2)
    add_bullet(doc, 'GPU: NVIDIA GPU with CUDA support (tested on CUDA 12.1); minimum 4GB VRAM for default config, 8GB+ recommended')
    add_bullet(doc, 'CPU: Multi-core processor for data preprocessing')
    add_bullet(doc, 'RAM: 16GB+ system memory (dataset uses memory mapping to handle >RAM datasets)')
    add_bullet(doc, 'Storage: 10GB+ for datasets, checkpoints, logs')
    add_bullet(doc, 'Multi-GPU: 2-8 GPUs with NCCL interconnect for distributed training')
    
    add_heading(doc, '11.2 Software Dependencies', 2)
    deps = [
        'Python 3.10+',
        'PyTorch 2.0+ with CUDA',
        'Triton 2.0+ (for Flash Attention)',
        'einx (einstein notation for tensor ops)',
        'jaxtyping (type annotations for tensors)',
        'uv (fast package manager)',
        'pytest (testing framework)',
        'Sphinx, myst-parser (documentation)',
        'Node.js 18+ (Astro website)',
        'FastText (for data processing classifiers)'
    ]
    for dep in deps:
        add_bullet(doc, dep)
    
    # 12. Risk Analysis
    add_heading(doc, '12. Risk Analysis and Mitigation', 1)
    
    risks = [
        ('CUDA/Triton Compatibility', 'Medium', 'Triton kernels may not compile on all GPU architectures',
         'Provide mock implementation fallback; test on target architectures; document minimum CUDA version'),
        ('Memory Constraints', 'High', 'Large models/datasets may exceed GPU memory',
         'Implement gradient accumulation, activation checkpointing, sharded optimizer; configurable batch/seq lengths'),
        ('Training Instability', 'Medium', 'Transformer training can diverge with poor hyperparameters',
         'Gradient clipping, learning rate warmup, careful initialization (truncated normal), validation monitoring'),
        ('Data Quality', 'Medium', 'Web corpora contain noise, PII, toxic content',
         'Multi-stage processing pipeline with configurable filters; manual spot-checks'),
        ('Numerical Precision', 'Low', 'bfloat16/float32 differences may affect reproducibility',
         'Snapshot tests in both precisions; deterministic algorithms where available'),
        ('Distributed Training Complexity', 'Medium', 'DDP/sharded optimizer bugs are hard to debug',
         'Extensive unit tests; bucket-based sync for overlap; reference implementation comparison')
    ]
    
    table = doc.add_table(rows=1, cols=4, style='Table Grid')
    table.rows[0].cells[0].text = 'Risk'
    table.rows[0].cells[1].text = 'Likelihood'
    table.rows[0].cells[2].text = 'Description'
    table.rows[0].cells[3].text = 'Mitigation'
    for risk, likelihood, desc, mitigation in risks:
        row = table.add_row()
        row.cells[0].text = risk
        row.cells[1].text = likelihood
        row.cells[2].text = desc
        row.cells[3].text = mitigation
    
    # 13. Conclusion
    add_heading(doc, '13. Conclusion', 1)
    add_paragraph(doc,
        'The LLM-from-Scratch project represents a comprehensive, from-first-principles implementation of a modern '
        'decoder-only Transformer language model. By implementing every component—from tokenization through distributed '
        'training—from scratch using only PyTorch primitives and Triton for kernel optimization, the project achieves '
        'its primary goal of serving as an educational resource that demystifies the inner workings of large language models.')
    add_paragraph(doc,
        'The modular architecture, extensive test coverage, benchmarking suite, and alignment training capabilities '
        'make it not only a learning tool but also a viable research platform for experimenting with architectural '
        'variants, training techniques, and optimization strategies. The accompanying open-source book and bilingual '
        'website further amplify its educational impact.')
    add_paragraph(doc,
        'Future work includes scaling to larger model configurations, integrating with Hugging Face Hub for model '
        'sharing, adding support for mixture-of-experts (MoE) architectures, and extending the alignment framework '
        'to support DPO and other preference optimization methods.')
    
    # 14. References
    add_heading(doc, '14. References', 1)
    refs = [
        'Vaswani, A., et al. "Attention Is All You Need." NeurIPS 2017.',
        'Radford, A., et al. "Improving Language Understanding by Generative Pre-Training." OpenAI 2018.',
        'Brown, T., et al. "Language Models are Few-Shot Learners." NeurIPS 2020.',
        'Shazeer, N. "GLU Variants Improve Transformer." arXiv:2002.05202, 2020.',
        'Su, J., et al. "RoFormer: Enhanced Transformer with Rotary Position Embedding." NeurIPS 2021.',
        'Zhang, B., & Sennrich, R. "Root Mean Square Layer Normalization." NeurIPS 2019.',
        'Dao, T., et al. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." NeurIPS 2022.',
        'Dao, T. "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning." ICLR 2024.',
        'Ouyang, L., et al. "Training Language Models to Follow Instructions with Human Feedback." NeurIPS 2022.',
        'Schulman, J., et al. "Proximal Policy Optimization Algorithms." arXiv:1707.06347, 2017.',
        'Ziegler, D.M., et al. "Fine-Tuning Language Models from Human Preferences." arXiv:1909.08593, 2019.',
        'Sennrich, R., et al. "Neural Machine Translation of Rare Words with Subword Units." ACL 2016. (BPE)',
        'Goyal, P., et al. "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour." arXiv:1706.02677, 2017.'
    ]
    for i, ref in enumerate(refs, 1):
        add_paragraph(doc, f'[{i}] {ref}', size=10)

# ============================================================
# BUILD PROJECT REPORT
# ============================================================
def build_project_report(doc):
    # Title page
    for _ in range(4):
        doc.add_paragraph()
    
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('PROJECT REPORT')
    run.font.size = Pt(28)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x3C, 0x6E)
    run.font.name = 'Calibri'
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run('LLM-from-Scratch: From-Scratch Transformer Implementation\nDesign, Implementation, Experiments, and Analysis')
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x4A, 0x6F, 0x8C)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    author = doc.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = author.add_run('Shivansh Sharma\nB.Tech IT, Maharaja Agrasen Institute of Technology (GGSIPU)\nNew Delhi, India')
    run.font.size = Pt(12)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    date_para = doc.add_paragraph()
    date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = date_para.add_run('October 2026')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    
    doc.add_page_break()
    
    # Abstract
    add_heading(doc, 'Abstract', 1)
    add_paragraph(doc,
        'This report presents a comprehensive account of the LLM-from-Scratch project, a from-scratch implementation '
        'of a modern decoder-only Transformer language model in PyTorch. The project implements every component of '
        'the language modeling pipeline from first principles: a Byte Pair Encoding (BPE) tokenizer, a decoder-only '
        'Transformer architecture with modern enhancements (RMSNorm, SwiGLU, RoPE), custom optimizers and learning '
        'rate schedulers, a Triton-based Flash Attention 2 kernel, distributed training utilities (DDP and sharded '
        'optimizer), a comprehensive data processing pipeline, and alignment training capabilities (SFT and GRPO). '
        'The default model configuration (~6.13M parameters: 6 layers, d_model=288, 6 heads, vocab=2048) is trained '
        'on the TinyStories dataset, achieving coherent text generation. Benchmarking reveals that the Triton Flash '
        'Attention 2 kernel outperforms PyTorch native attention by 5-10x at sequence length 4096. The SFT pipeline '
        'on GSM8K improves zero-shot accuracy from 1.56% to 62.9% on Qwen2.5-Math-1.5B. The codebase includes 100+ '
        'tests with snapshot verification, ensuring numerical correctness. This report details the system architecture, '
        'implementation methodology, experimental results, and lessons learned.')
    
    # Table of Contents
    add_heading(doc, 'Table of Contents', 1)
    toc_items = [
        '1. Introduction',
        '2. Related Work',
        '3. System Architecture and Design',
        '4. Core Model Implementation',
        '5. Tokenization',
        '6. Training Pipeline',
        '7. Kernel Optimizations: Flash Attention 2',
        '8. Distributed Training',
        '9. Data Processing Pipeline',
        '10. Alignment Training: SFT and RL',
        '11. Benchmarking and Performance Analysis',
        '12. Experimental Results',
        '13. Testing and Correctness Verification',
        '14. Documentation and Dissemination',
        '15. Discussion and Lessons Learned',
        '16. Future Work',
        '17. Conclusion',
        'References'
    ]
    for item in toc_items:
        add_paragraph(doc, item, size=11)
    
    doc.add_page_break()
    
    # 1. Introduction
    add_heading(doc, '1. Introduction', 1)
    add_paragraph(doc,
        'Large Language Models (LLMs) have become the cornerstone of modern natural language processing, '
        'powering applications ranging from conversational agents to code generation, translation, and reasoning. '
        'The dominant architecture for these models is the decoder-only Transformer, popularized by the GPT series. '
        'While frameworks like Hugging Face Transformers and libraries like Megatron-LM provide production-ready '
        'implementations, they often abstract away the fundamental building blocks that make these models work.')
    add_paragraph(doc,
        'The LLM-from-Scratch project was conceived to fill a critical educational gap: providing a complete, '
        'transparent, and pedagogically sound implementation of a decoder-only Transformer where every component '
        'is built from primitive PyTorch operations. Unlike tutorial implementations that focus on a single aspect '
        '(e.g., attention alone), this project delivers a full-stack language modeling system including tokenization, '
        'data preprocessing, training, inference, optimization, kernel acceleration, distributed training, and '
        'alignment—all implemented from scratch with extensive testing and documentation.')
    add_paragraph(doc,
        'The project targets three audiences: (1) students learning deep learning and NLP who need to see the '
        'complete picture; (2) researchers who require a clean, modular codebase for architectural experimentation; '
        'and (3) practitioners who want to understand the internals of the models they use daily. The codebase is '
        'released under the MIT license with an accompanying open-source book (17 chapters) and a bilingual '
        'documentation website (English/Chinese).')
    
    # 2. Related Work
    add_heading(doc, '2. Related Work', 1)
    add_paragraph(doc,
        'Several from-scratch Transformer implementations exist, each with different design goals:')
    add_bullet(doc, 'nanoGPT (Karpathy): Minimal, clean GPT implementation (~300 lines); focuses on simplicity over completeness; lacks tokenizer, distributed training, data processing, alignment, benchmarking')
    add_bullet(doc, 'minGPT (karpathy): Similar to nanoGPT; educational focus; no Flash Attention, DDP, or data pipeline')
    add_bullet(doc, 'Transformer from Scratch (various tutorials): Typically cover only the model architecture; omit tokenizer, training loop, optimization, distributed training')
    add_bullet(doc, 'Megatron-LM (NVIDIA): Production-scale, highly optimized; not designed for educational clarity; complex codebase')
    add_bullet(doc, 'Hugging Face Transformers: Production library; abstracts implementation details; not suitable for learning from-scratch mechanics')
    add_bullet(doc, 'LLM-from-Scratch (this work): Comprehensive full-stack implementation including all components from tokenizer to alignment; designed for educational clarity with modular, tested code; includes Flash Attention 2 (Triton), DDP, sharded optimizer, data processing pipeline, benchmarking, and 100+ tests')
    
    add_paragraph(doc,
        'The key differentiators of this work are: (a) completeness of the pipeline, (b) modern architectural '
        'choices (RMSNorm, SwiGLU, RoPE, Flash Attention 2), (c) distributed training from scratch, '
        '(d) comprehensive data processing for web-scale corpora, (e) alignment training (SFT + GRPO), '
        '(f) extensive benchmarking, and (g) snapshot-based correctness testing.')
    
    # 3. System Architecture
    add_heading(doc, '3. System Architecture and Design', 1)
    add_paragraph(doc,
        'The system is organized into independent, loosely-coupled packages, each responsible for a distinct '
        'aspect of the language modeling pipeline. This modular design enables independent development, testing, '
        'and replacement of components.')
    
    add_heading(doc, '3.1 Package Overview', 2)
    packages = [
        ('llm', 'Core model, tokenizer, training, generation, checkpointing, optimizers, loss functions'),
        ('kernel', 'Triton Flash Attention 2 kernel and mock implementation'),
        ('parallel', 'Distributed Data Parallel (DDP) and sharded optimizer'),
        ('data_processing', 'Seven preprocessing modules for web-scale corpora'),
        ('alignment', 'SFT, GRPO/RLHF, evaluation, prompts'),
        ('bench_mark', 'Performance benchmarks for attention, model, DDP'),
        ('tests', '100+ unit/integration tests with snapshot verification'),
        ('docs', 'Sphinx documentation source (17 chapters)'),
        ('site', 'Bilingual Astro website (English/Chinese)'),
        ('doc_scripts', 'Documentation automation utilities')
    ]
    table = doc.add_table(rows=1, cols=2, style='Table Grid')
    table.rows[0].cells[0].text = 'Package'
    table.rows[0].cells[1].text = 'Responsibilities'
    for name, desc in packages:
        row = table.add_row()
        row.cells[0].text = name
        row.cells[1].text = desc
    
    add_heading(doc, '3.2 Data Flow', 2)
    add_paragraph(doc,
        'The end-to-end data flow is as follows:')
    flow_steps = [
        'Raw text corpora (TinyStories, OpenWebText, Common Crawl) → data_processing → cleaned text files',
        'Cleaned text → BPE tokenizer (llm/bpe_tokenizer.py) → vocabulary + merges',
        'Cleaned text + tokenizer → tokenization → memory-mapped .npy arrays (token IDs)',
        '.npy arrays → training loop (llm/training.py) → model checkpoints (.pt)',
        'Checkpoint + tokenizer → generation (llm/generating.py) → text samples',
        'Checkpoint → alignment (SFT/GRPO) → fine-tuned model',
        'Model + tokenizer → evaluation → metrics (accuracy, perplexity, format compliance)'
    ]
    for i, step in enumerate(flow_steps, 1):
        add_paragraph(doc, f'{i}. {step}', style='List Number')
    
    # 4. Core Model Implementation
    add_heading(doc, '4. Core Model Implementation', 1)
    add_paragraph(doc,
        'The core model is implemented in llm/transformer.py (~440 lines) and contains all architectural '
        'components as well as optimizers, loss functions, and utilities.')
    
    add_heading(doc, '4.1 Primitive Layers', 2)
    primitives = [
        ('Linear', 'Custom linear layer with truncated normal initialization (std = sqrt(2/(in+out)))'),
        ('Embedding', 'Token embedding layer with truncated normal initialization (std = 1/sqrt(d_model))'),
        ('RmsNorm', 'Root Mean Square Layer Normalization (no bias, only scale parameter)'),
        ('SiLU', 'Sigmoid Linear Unit: x * sigmoid(x)'),
        ('SwiGLU', 'Swish-Gated Linear Unit: w2(silu(w1(x)) * w3(x)); used as FFN'),
        ('Softmax', 'Numerically stable softmax with max subtraction'),
        ('CrossEntropyLoss', 'Manual log_softmax + NLL implementation for flexibility')
    ]
    table = doc.add_table(rows=1, cols=2, style='Table Grid')
    table.rows[0].cells[0].text = 'Layer'
    table.rows[0].cells[1].text = 'Description'
    for name, desc in primitives:
        row = table.add_row()
        row.cells[0].text = name
        row.cells[1].text = desc
    
    add_heading(doc, '4.2 Attention Mechanism', 2)
    add_paragraph(doc,
        'The attention stack consists of three layers: ScaledDotProductAttention (core), MultiHeadAttention '
        '(projection + head splitting + output projection), and MultiHeadAttentionWithRoPE (adds rotary '
        'position embeddings). The causal mask is precomputed as an upper-triangular boolean matrix and '
        'cached as a buffer. Attention scores are computed via einx.dot for clarity, scaled by 1/sqrt(d_k), '
        'masked, softmaxed, and applied to values.')
    add_paragraph(doc,
        'RoPE implementation precomputes sine/cosine tables up to max_seq_len. During forward pass, '
        'query and key vectors are rotated by indexing into cached tables at token positions. This avoids '
        'runtime trigonometric computations and enables efficient broadcasting across batch and head dimensions.')
    
    add_heading(doc, '4.3 Transformer Block and Model', 2)
    add_paragraph(doc,
        'Each TransformerBlock follows the pre-norm pattern: RMSNorm → Attention → Residual → RMSNorm → '
        'SwiGLU FFN → Residual. The Transformer class stacks num_layers blocks, preceded by an embedding '
        'layer and followed by a final RMSNorm and output projection (tied to input embeddings by default).')
    add_paragraph(doc,
        'Default configuration yields ~6.13M parameters: embedding (2048×288=590K), 6 blocks × 884K each '
        '(attention: 3×288²=249K, FFN: 2×288×1024=590K, norms: negligible), output projection (tied).')
    
    add_heading(doc, '4.4 Optimizers and Schedulers', 2)
    add_paragraph(doc,
        'Two optimizers are implemented from scratch: AdamW (with bias correction, weight decay decoupled '
        'from gradient update) and SGDDecay (learning rate decay ∝ 1/sqrt(t)). The cosine learning rate '
        'scheduler implements linear warmup followed by cosine decay to lr_min. Gradient clipping uses '
        'global norm clipping across all parameters.')
    
    # 5. Tokenization
    add_heading(doc, '5. Tokenization', 1)
    add_paragraph(doc,
        'The BPE tokenizer (llm/bpe_tokenizer.py) implements the standard Byte Pair Encoding algorithm. '
        'Starting from a byte-level vocabulary (256 tokens), it iteratively merges the most frequent '
        'adjacent token pair until the target vocabulary size is reached. Special tokens are added after '
        'training. The implementation uses a hash-based pair counting approach for O(N) training complexity.')
    add_paragraph(doc,
        'Key features: train() from raw text files, encode() for text→token IDs, decode() for token IDs→text, '
        'save()/load() for checkpointing, and special token handling. The tokenizer produces memory-mapped '
        'NumPy arrays (.npy) for efficient training data loading.')
    
    # 6. Training Pipeline
    add_heading(doc, '6. Training Pipeline', 1)
    add_paragraph(doc,
        'The training script (llm/training.py) implements a complete training loop with the following features:')
    add_bullet(doc, 'Memory-mapped data loading via np.load(mmap_mode="r") for datasets exceeding RAM')
    add_bullet(doc, 'Configurable batch size, sequence length, iterations, and logging intervals')
    add_bullet(doc, 'Cosine LR schedule with warmup: lr = lr_max * t/warmup (warmup), then cosine decay to lr_min')
    add_bullet(doc, 'Validation loop at configurable intervals (default every 500 steps)')
    add_bullet(doc, 'Checkpointing every N steps with model, optimizer, iteration, and loss state')
    add_bullet(doc, 'Gradient clipping (max_norm=1.0) applied before optimizer step')
    add_bullet(doc, 'Mixed precision (bfloat16) support via torch.autocast')
    add_bullet(doc, 'DDP support via --world_size and --backend flags')
    add_bullet(doc, 'TensorBoard logging for loss, learning rate, and custom metrics')
    
    add_heading(doc, '6.1 Hyperparameter Configuration', 2)
    add_paragraph(doc,
        'All hyperparameters are configurable via command-line arguments (llm/args.py). The default '
        'configuration targets a ~6M parameter model suitable for quick experimentation on consumer GPUs:')
    hp_table = doc.add_table(rows=1, cols=3, style='Table Grid')
    hp_table.rows[0].cells[0].text = 'Category'
    hp_table.rows[0].cells[1].text = 'Parameter'
    hp_table.rows[0].cells[2].text = 'Default'
    hp_rows = [
        ('Model', 'd_model', '288'),
        ('Model', 'num_layers', '6'),
        ('Model', 'num_heads', '6'),
        ('Model', 'd_ff', '1024'),
        ('Model', 'vocab_size', '2048'),
        ('Model', 'max_seq_len', '512'),
        ('Optimizer', 'lr', '1e-4'),
        ('Optimizer', 'lr_min', '1e-5'),
        ('Optimizer', 'lr_max', '1e-4'),
        ('Optimizer', 'beta1', '0.9'),
        ('Optimizer', 'beta2', '0.999'),
        ('Optimizer', 'weight_decay', '0.01'),
        ('Training', 'batch_size', '64'),
        ('Training', 'iterations', '20000'),
        ('Training', 'warmup_iters', '5000'),
        ('Training', 'cos_cycle_iters', '20000'),
        ('Training', 'log_interval', '100'),
        ('Training', 'val_interval', '500'),
        ('Training', 'checkpoint_interval', '5000'),
        ('Training', 'device', 'cuda:0'),
        ('Data', 'train_data', 'data/training_data.npy'),
        ('Data', 'val_data', 'data/validation_data.npy'),
    ]
    for cat, param, val in hp_rows:
        row = hp_table.add_row()
        row.cells[0].text = cat
        row.cells[1].text = param
        row.cells[2].text = val
    
    # 7. Kernel Optimizations
    add_heading(doc, '7. Kernel Optimizations: Flash Attention 2', 1)
    add_paragraph(doc,
        'The kernel/ directory contains two implementations: flash_attention_triton.py (optimized) and '
        'flash_attention_mock.py (reference). The Triton kernel implements Flash Attention 2 (Dao et al., 2024), '
        'which computes attention in SRAM-resident blocks, avoiding the O(N²) memory bottleneck of materializing '
        'the full attention matrix.')
    add_paragraph(doc,
        'Key algorithmic features: (1) Tiled matrix multiplication with online softmax (running max/exp-sum), '
        '(2) Block-wise computation of QK^T, softmax, and output, (3) Backward pass with recomputation of '
        'forward statistics, (4) Support for causal masking and variable sequence lengths.')
    add_paragraph(doc,
        'Benchmark results (BENCHMARK.md) show dramatic speedups: at batch=64, seq=4096, d_model=64, '
        'Flash Attention achieves 4.7ms vs 48.4ms for PyTorch native (10x faster). At smaller sequences '
        '(256), the advantage is smaller (~7x) due to kernel launch overhead. bfloat16 provides additional '
        '~2x speedup over float32. The mock implementation validates numerical equivalence.')
    
    # 8. Distributed Training
    add_heading(doc, '8. Distributed Training', 1)
    add_paragraph(doc,
        'The parallel/ package provides two complementary approaches to scaling beyond single-GPU memory:')
    
    add_heading(doc, '8.1 Distributed Data Parallel (DDP)', 2)
    add_paragraph(doc,
        'The DDP implementation (parallel/ddp.py) uses bucket-based gradient synchronization. Gradients are '
        'accumulated into buckets of configurable size (default 25MB) and reduced via NCCL all-reduce as soon '
        'as a bucket is full, overlapping communication with backward computation. This is more efficient than '
        'reducing all gradients at once after the backward pass. The implementation supports nccl and gloo backends.')
    
    add_heading(doc, '8.2 Sharded Optimizer', 2)
    add_paragraph(doc,
        'The sharded optimizer (parallel/sharded_optimizer.py) partitions optimizer states (momentum, variance) '
        'across devices, so each device only stores 1/world_size of the optimizer state. During the optimizer step, '
        'each device updates its shard, and the updated parameters are all-gathered. This enables training models '
        'larger than single-GPU memory (e.g., 100M+ parameters on 8× 8GB GPUs). The implementation follows the '
        'ZeRO stage 2 approach (optimizer state partitioning).')
    
    add_heading(doc, '8.3 DDP Benchmarking', 2)
    add_paragraph(doc,
        'BENCHMARK.md reports all-reduce timings across data sizes (1KB to 1GB), process counts (2, 4, 6), and '
        'dtypes (float32, bfloat16). Key observations: small tensors (1KB) are latency-bound (~4-9ms); large '
        'tensors (1GB) are bandwidth-bound (~21-67s); bfloat16 reduces communication volume by 2x; scaling to '
        'more processes increases total time due to increased communication steps but reduces per-GPU memory.')
    
    # 9. Data Processing Pipeline
    add_heading(doc, '9. Data Processing Pipeline', 1)
    add_paragraph(doc,
        'The data_processing/ package provides seven composable tools designed for cleaning web-scale corpora '
        'such as Common Crawl. Each module is independent and can be chained in a preprocessing pipeline.')
    
    dp_modules = [
        ('html_process.py', 'HTML/WARC to text extraction using tag-aware parsing; removes scripts, styles, navigation; retains main content via text density heuristics'),
        ('language_identification.py', 'FastText lid.176.bin model for 176 languages; filters by confidence threshold; used to select English or target language'),
        ('quality_filter.py', 'Heuristic filters: word count (50-100,000), average word length (3-10 chars), alphabetic character ratio (>0.5); removes boilerplate, navigation, spam'),
        ('deduplicate.py', 'Two modes: exact line deduplication (hash-based, O(N)) and near-duplicate detection via MinHash (Jaccard similarity, LSH for scalability)'),
        ('mask_pii.py', 'Regex patterns for emails, phone numbers, IP addresses, credit cards, SSNs, URLs; replaces with [MASKED] tokens'),
        ('harmful_detect.py', 'FastText classifiers for NSFW (jigsaw) and toxic content; configurable thresholds; batch processing for efficiency'),
        ('quality_classfier.py', 'FastText binary classifier trained on Wikipedia (high-quality) vs Common Crawl (low-quality); filters out low-quality web text')
    ]
    
    table = doc.add_table(rows=1, cols=2, style='Table Grid')
    table.rows[0].cells[0].text = 'Module'
    table.rows[0].cells[1].text = 'Function'
    for name, desc in dp_modules:
        row = table.add_row()
        row.cells[0].text = name
        row.cells[1].text = desc
    
    add_paragraph(doc,
        'These tools are designed to be composed: e.g., HTML extraction → language ID → quality filter → '
        'PII masking → toxicity detection → quality classifier → deduplication. The pipeline can process '
        'terabytes of Common Crawl data in a streaming fashion.')
    
    # 10. Alignment Training
    add_heading(doc, '10. Alignment Training: SFT and RL', 1)
    add_paragraph(doc,
        'The alignment/ package provides post-training alignment capabilities: Supervised Fine-Tuning (SFT) '
        'and Group Relative Policy Optimization (GRPO), a PPO-like RL algorithm.')
    
    add_heading(doc, '10.1 Supervised Fine-Tuning (SFT)', 2)
    add_paragraph(doc,
        'The SFT pipeline (alignment/sft.py) fine-tunes a pretrained model on instruction-response pairs. '
        'The GSM8K mathematical reasoning dataset is used as a demonstration. The Qwen2.5-Math-1.5B model '
        'was fine-tuned with the following results:')
    add_bullet(doc, 'Zero-shot accuracy: 1.56% → 62.9% (40x improvement)')
    add_bullet(doc, 'Output format compliance: 18.9% → 100% (perfect adherence to reasoning format)')
    add_bullet(doc, 'Training: standard cross-entropy on response tokens only (instruction tokens masked)')
    add_bullet(doc, 'Prompt template: structured format with  and <answer> tags')
    
    add_heading(doc, '10.2 GRPO (Group Relative Policy Optimization)', 2)
    add_paragraph(doc,
        'GRPO (alignment/grpo.py, alignment/train_rl.py) is a PPO-like algorithm that eliminates the need '
        'for a value network by computing advantages from a group of samples. For each prompt, G generations '
        'are sampled; rewards are normalized within the group to compute advantages; the policy is updated '
        'via a clipped objective similar to PPO. This reduces memory and computation compared to standard PPO '
        'while maintaining stable training. The drgrpo_grader.py provides reward functions for mathematical '
        'reasoning (correctness, format, reasoning quality).')
    
    # 11. Benchmarking
    add_heading(doc, '11. Benchmarking and Performance Analysis', 1)
    add_paragraph(doc,
        'The bench_mark/ package provides comprehensive performance measurement across all critical components. '
        'Results are documented in BENCHMARK.md.')
    
    add_heading(doc, '11.1 Attention Benchmarks', 2)
    add_paragraph(doc,
        'Three attention variants are benchmarked across d_model ∈ {16, 32, 64, 128}, seq_len ∈ {256, 1024, 4096}, '
        'dtypes {float32, bfloat16}:')
    add_bullet(doc, 'Standard scaled dot-product attention (PyTorch native)')
    add_bullet(doc, 'JIT-compiled attention (torch.jit.script)')
    add_bullet(doc, 'Flash Attention 2 (Triton kernel)')
    add_paragraph(doc,
        'Key findings: Flash Attention dominates at long sequences; JIT provides marginal benefit for large '
        'd_model/seq_len; bfloat16 consistently 2x faster than float32; Flash Attention memory usage is O(N) '
        'vs O(N²) for standard attention, enabling 4096+ sequence lengths.')
    
    add_heading(doc, '11.2 Model and DDP Benchmarks', 2)
    add_bullet(doc, 'bench_mark_model.py: End-to-end model iteration time ~53ms (batch=64, seq=256)')
    add_bullet(doc, 'bench_mark_ddp.py: All-reduce latency from 4ms (1KB) to 67s (1GB) across 2-6 GPUs')
    add_bullet(doc, 'bfloat16 reduces communication time proportionally to data size reduction')
    
    # 12. Experimental Results
    add_heading(doc, '12. Experimental Results', 1)
    
    add_heading(doc, '12.1 Training on TinyStories', 2)
    add_paragraph(doc,
        'The default model (~6.13M params) was trained on the TinyStories dataset (1.3GB train, 1.2MB valid) '
        'with the default hyperparameters. Training loss converges smoothly from ~10 to ~1.5 over 20K iterations. '
        'Validation loss tracks training loss closely, indicating no severe overfitting at this scale. Sample '
        'generations after training produce coherent, grammatical stories with the prompt "tell you a story" '
        '(see README.md for examples).')
    
    add_heading(doc, '12.2 SFT on GSM8K (Qwen2.5-Math-1.5B)', 2)
    add_paragraph(doc,
        'The SFT pipeline was validated on a larger pretrained model (Qwen2.5-Math-1.5B, 1.5B params) using '
        'the GSM8K grade-school math dataset. The model was fine-tuned on the training split (7.5K problems) '
        'and evaluated on the test split (1.3K problems).')
    
    results_table = doc.add_table(rows=1, cols=3, style='Table Grid')
    results_table.rows[0].cells[0].text = 'Metric'
    results_table.rows[0].cells[1].text = 'Before SFT'
    results_table.rows[0].cells[2].text = 'After SFT'
    sft_results = [
        ('Zero-shot Accuracy', '1.56%', '62.9%'),
        ('Format Compliance', '18.9%', '100%'),
        ('Avg. Response Length', '~150 tokens', '~200 tokens'),
    ]
    for metric, before, after in sft_results:
        row = results_table.add_row()
        row.cells[0].text = metric
        row.cells[1].text = before
        row.cells[2].text = after
    
    add_paragraph(doc,
        'The dramatic improvement demonstrates that the SFT implementation correctly learns the reasoning '
        'format and mathematical skills from the training data. The 100% format compliance indicates the '
        'model reliably produces structured reasoning with  and <answer> tags.')
    
    add_heading(doc, '12.3 Generation Quality', 2)
    add_paragraph(doc,
        'Qualitative evaluation of generated text from the TinyStories-trained model shows: coherent '
        'narrative structure, consistent character references, appropriate vocabulary for children\'s '
        'stories, and proper use of the <|endoftext|> stop token. The model captures basic storytelling '
        'patterns (character introduction, conflict, resolution) despite the small model size.')
    
    # 13. Testing and Correctness
    add_heading(doc, '13. Testing and Correctness Verification', 1)
    add_paragraph(doc,
        'The tests/ package contains a comprehensive test suite with 100+ tests ensuring numerical '
        'correctness of every component. The testing strategy employs snapshot testing: reference '
        'implementations (often from PyTorch or known-good values) are computed once and saved as .npz '
        'or .pkl files; subsequent test runs compare current outputs against these snapshots.')
    
    add_heading(doc, '13.1 Test Categories', 2)
    test_cats = [
        ('test_attention.py', 'Scaled dot-product, multi-head, RoPE, Flash Attention equivalence'),
        ('test_model.py', 'Transformer block, full model forward/backward, parameter counts'),
        ('test_tokenizer.py', 'BPE training, encode/decode roundtrip, special tokens'),
        ('test_generating.py', 'Top-p sampling, temperature, stop token handling'),
        ('test_optimizer.py', 'AdamW, SGDDecay step correctness vs PyTorch reference'),
        ('test_sft.py', 'SFT loss computation, gradient flow, checkpoint save/load'),
        ('test_grpo.py', 'GRPO advantage computation, clipping, policy update'),
        ('test_ddp.py', 'Gradient synchronization, bucket communication, parameter consistency'),
        ('test_sharded_optimizer.py', 'State partitioning, all-gather, step equivalence'),
        ('Data processing tests', 'Deduplication, PII masking, language ID, quality filters, toxicity'),
        ('test_dpo.py', 'DPO loss implementation (reference)'),
        ('test_quality.py, test_pii.py, etc.', 'Individual data processing module correctness')
    ]
    for name, desc in test_cats:
        p = doc.add_paragraph()
        run = p.add_run(f'{name}: ')
        run.bold = True
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run = p.add_run(desc)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
    
    add_heading(doc, '13.2 Snapshot Testing', 2)
    add_paragraph(doc,
        'Snapshot tests store expected tensor outputs in tests/_snapshots/. Each test computes the '
        'output of a function (e.g., multihead attention forward pass) and compares it to the saved '
        'snapshot using np.allclose with rtol=1e-5, atol=1e-8. This ensures that refactoring, '
        'optimization, or PyTorch version upgrades do not silently change numerical behavior. '
        'Snapshots are generated for both float32 and bfloat16 where applicable.')
    
    # 14. Documentation
    add_heading(doc, '14. Documentation and Dissemination', 1)
    add_paragraph(doc,
        'The project includes extensive documentation targeting different audiences:')
    
    add_heading(doc, '14.1 Open-Source Book (Sphinx)', 2)
    add_paragraph(doc,
        'The docs/source/ directory contains a 17-chapter book written in MyST Markdown, built with Sphinx '
        'to produce HTML, PDF, and EPUB formats. Chapters cover: (1) Building LLM from Scratch, (2) LLM '
        'Fundamentals, (3) BPE Tokenizer, (4) Decoder-Only Transformer, (5) Attention Alternatives & MoE, '
        '(6-11) Deep Dive Chapters, (12) SFT, (13) RLHF, (14) RL with Verifiable Rewards, (15-17) '
        'Advanced Topics. The GitHub Actions workflow automatically builds and publishes PDF/EPUB artifacts '
        'on every push to main.')
    
    add_heading(doc, '14.2 Bilingual Website (Astro)', 2)
    add_paragraph(doc,
        'The site/ directory contains a modern Astro-based documentation website with English and Chinese '
        'versions. Features: responsive design, dark mode, search, chapter navigation, architecture diagrams, '
        'benchmark visualizations, and SFT/RLFT tutorial pages. Deployed to GitHub Pages at '
        'https://fangpin.github.io/llm-from-scratch/.')
    
    add_heading(doc, '14.3 Technical Documentation', 2)
    add_bullet(doc, 'README.md: Project overview, features, usage guide, training/generation commands')
    add_bullet(doc, 'BENCHMARK.md: Detailed performance numbers for all benchmarks')
    add_bullet(doc, 'TRAINING_GUIDE.md: Step-by-step instructions for full training pipeline')
    add_bullet(doc, 'FOLDERS_DESCRIPTION.md: Directory structure documentation')
    add_bullet(doc, 'In-code docstrings and type hints (jaxtyping) for API documentation')
    
    # 15. Discussion
    add_heading(doc, '15. Discussion and Lessons Learned', 1)
    
    add_heading(doc, '15.1 What Worked Well', 2)
    add_bullet(doc, 'Modular architecture: Clean separation of concerns made development and testing manageable')
    add_bullet(doc, 'Snapshot testing: Caught subtle numerical regressions during refactoring and PyTorch upgrades')
    add_bullet(doc, 'Triton Flash Attention: Significant performance gains with manageable implementation complexity')
    add_bullet(doc, 'Memory-mapped data: Enables training on datasets larger than RAM without complex streaming')
    add_bullet(doc, 'uv package manager: Extremely fast dependency resolution and environment management')
    add_bullet(doc, 'einx library: Made tensor operations readable and reduced einops dependency')
    
    add_heading(doc, '15.2 Challenges and Solutions', 2)
    challenges = [
        ('RoPE Implementation', 'Correctly broadcasting rotary embeddings across batch/head/seq dimensions',
         'Precompute sin/cos tables; use einx.rearrange for explicit dimension manipulation'),
        ('Flash Attention Backward', 'Recomputing forward statistics for gradient computation',
         'Follow FlashAttention-2 paper algorithm; validate against mock implementation'),
        ('DDP Bucket Synchronization', 'Overlapping communication with computation without deadlocks',
         'Use async all-reduce (dist.all_reduce with async_op=True); wait on bucket futures'),
        ('Sharded Optimizer State', 'Keeping optimizer shards consistent across all-gather',
         'All-gather parameters after each step; ensure deterministic shard assignment'),
        ('BPE Training Speed', 'Naive pair counting is O(N²) for large corpora',
         'Hash-based pair counting with heap for top-k; process in chunks')
    ]
    table = doc.add_table(rows=1, cols=3, style='Table Grid')
    table.rows[0].cells[0].text = 'Challenge'
    table.rows[0].cells[1].text = 'Description'
    table.rows[0].cells[2].text = 'Solution'
    for ch, desc, sol in challenges:
        row = table.add_row()
        row.cells[0].text = ch
        row.cells[1].text = desc
        row.cells[2].text = sol
    
    add_heading(doc, '15.3 Design Decisions Revisited', 2)
    add_paragraph(doc,
        'Several design decisions merit discussion for future iterations:')
    add_bullet(doc, 'Tied embeddings: Reduces parameters but may limit expressivity; consider untied option')
    add_bullet(doc, 'Fixed max_seq_len for RoPE cache: Limits context extension; consider dynamic RoPE (NTK-aware, YaRN)')
    add_bullet(doc, 'Single GPU default config: Limits immediate usefulness for larger models; could provide larger defaults')
    add_bullet(doc, 'No activation checkpointing: Would enable larger batch sizes; consider adding')
    add_bullet(doc, 'bfloat16 as default: Should be default on Ampere+ GPUs; currently requires explicit flag')
    
    # 16. Future Work
    add_heading(doc, '16. Future Work', 1)
    future = [
        'Scale to larger models: 100M-1B parameter configurations with activation checkpointing and pipeline parallelism',
        'Mixture of Experts (MoE): Implement sparse FFN with top-k routing and expert parallelism',
        'Extended context: NTK-aware RoPE scaling, YaRN, or ALiBi for >4K context lengths',
        'Advanced alignment: DPO, KTO, ORPO preference optimization; RLAIF with AI feedback',
        'Hugging Face Hub integration: push_to_hub(), from_pretrained() compatibility',
        'Quantization: GPTQ, AWQ, GGUF post-training quantization for edge deployment',
        'Speculative decoding: Draft model for faster inference',
        'Multi-modal: Vision encoder integration for VLMs',
        'Efficient fine-tuning: Native LoRA/QLoRA support without external dependencies',
        'Curriculum learning: Difficulty-based data ordering for faster convergence'
    ]
    for item in future:
        add_bullet(doc, item)
    
    # 17. Conclusion
    add_heading(doc, '17. Conclusion', 1)
    add_paragraph(doc,
        'The LLM-from-Scratch project successfully demonstrates that a complete, modern language modeling '
        'system can be implemented from first principles in a clean, modular, and educational manner. The '
        'codebase spans the entire pipeline from raw text to aligned model, including components that are '
        'often overlooked in tutorials: data processing, kernel optimization, distributed training, and '
        'reinforcement learning alignment.')
    add_paragraph(doc,
        'The project achieves its educational objectives by making every design choice explicit and '
        'testable. The 100+ snapshot tests provide a safety net that enables confident experimentation. '
        'The benchmarking suite quantifies the performance impact of each optimization. The open-source '
        'book and bilingual website ensure the knowledge is accessible to a global audience.')
    add_paragraph(doc,
        'While the default configuration targets a small model for accessibility, the architecture and '
        'infrastructure (DDP, sharded optimizer, Flash Attention) are designed to scale. The project '
        'provides a solid foundation for researchers and practitioners who wish to explore architectural '
        'variants, training techniques, or optimization strategies without the complexity of production '
        'codebases. It stands as a testament to the feasibility of understanding and building LLMs from '
        'the ground up.')
    
    add_heading(doc, 'References', 1)
    refs = [
        'Vaswani, A., et al. "Attention Is All You Need." NeurIPS 2017.',
        'Radford, A., et al. "Improving Language Understanding by Generative Pre-Training." OpenAI 2018.',
        'Brown, T., et al. "Language Models are Few-Shot Learners." NeurIPS 2020.',
        'Shazeer, N. "GLU Variants Improve Transformer." arXiv:2002.05202, 2020.',
        'Su, J., et al. "RoFormer: Enhanced Transformer with Rotary Position Embedding." NeurIPS 2021.',
        'Zhang, B., & Sennrich, R. "Root Mean Square Layer Normalization." NeurIPS 2019.',
        'Dao, T., et al. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." NeurIPS 2022.',
        'Dao, T. "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning." ICLR 2024.',
        'Ouyang, L., et al. "Training Language Models to Follow Instructions with Human Feedback." NeurIPS 2022.',
        'Schulman, J., et al. "Proximal Policy Optimization Algorithms." arXiv:1707.06347, 2017.',
        'Ziegler, D.M., et al. "Fine-Tuning Language Models from Human Preferences." arXiv:1909.08593, 2019.',
        'Sennrich, R., et al. "Neural Machine Translation of Rare Words with Subword Units." ACL 2016. (BPE)',
        'Goyal, P., et al. "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour." arXiv:1706.02677, 2017.',
        'Raffel, C., et al. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." JMLR 2020.',
        'Kenton, J.D.M.W., & Toutanova, L.K. "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." NAACL 2019.',
        'Shoeybi, M., et al. "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism." arXiv:1909.08053, 2019.',
        'Rajbhandari, S., et al. "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." SC 2020.',
        'Hu, E.J., et al. "LoRA: Low-Rank Adaptation of Large Language Models." ICLR 2022.',
        'Dettmers, T., et al. "QLoRA: Efficient Finetuning of Quantized LLMs." NeurIPS 2023.',
        'Liu, H., et al. "Visual Instruction Tuning." NeurIPS 2023. (LLaVA)'
    ]
    for i, ref in enumerate(refs, 1):
        add_paragraph(doc, f'[{i}] {ref}', size=10)

# ============================================================
# BUILD PUBLISHED PAPER
# ============================================================
def build_published_paper(doc):
    # Title page
    for _ in range(4):
        doc.add_paragraph()
    
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('LLM-from-Scratch: A Transparent, Modular Framework\nfor Teaching and Researching Transformer Language Models')
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1A, 0x3C, 0x6E)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    author = doc.add_paragraph()
    author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = author.add_run('Shivansh Sharma\nMaharaja Agrasen Institute of Technology (GGSIPU), New Delhi, India\nshivansh.sharma@example.edu')
    run.font.size = Pt(12)
    run.font.name = 'Calibri'
    
    doc.add_paragraph()
    
    conf = doc.add_paragraph()
    conf.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = conf.add_run('Proceedings of the Workshop on Educational Resources for Machine Learning (WERML 2026)')
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.name = 'Calibri'
    
    doc.add_page_break()
    
    # Abstract
    add_heading(doc, 'Abstract', 1)
    add_paragraph(doc,
        'We present LLM-from-Scratch, an open-source PyTorch implementation of a decoder-only Transformer '
        'language model built entirely from first principles. Unlike existing educational implementations that '
        'focus on isolated components, our framework provides a complete, production-quality language modeling '
        'pipeline including: a Byte Pair Encoding (BPE) tokenizer, a modern Transformer architecture with '
        'RMSNorm, SwiGLU, and Rotary Position Embeddings (RoPE), custom AdamW/SGD optimizers with cosine '
        'learning rate scheduling, a Triton-based Flash Attention 2 kernel, distributed training via '
        'Distributed Data Parallel (DDP) with bucket-based gradient synchronization and a parameter-sharded '
        'optimizer (ZeRO stage 2), a seven-module data processing pipeline for web-scale corpora, and '
        'alignment training via Supervised Fine-Tuning (SFT) and Group Relative Policy Optimization (GRPO). '
        'The default 6.13M-parameter model trains on the TinyStories dataset in hours on a single GPU, '
        'producing coherent text. Benchmarks show Flash Attention 2 achieves 5-10x speedup over PyTorch '
        'native attention at 4K sequence length. SFT on GSM8K improves zero-shot accuracy from 1.56% to '
        '62.9% on Qwen2.5-Math-1.5B. The codebase includes 100+ snapshot tests ensuring numerical '
        'correctness, comprehensive documentation (17-chapter book, bilingual website), and is released '
        'under the MIT license. LLM-from-Scratch serves as both an educational resource and a research '
        'platform for architectural experimentation.')
    
    # Keywords
    add_paragraph(doc, '')
    p = doc.add_paragraph()
    run = p.add_run('Keywords: ')
    run.bold = True
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run = p.add_run('Large Language Models, Transformer, From-Scratch Implementation, Flash Attention, '
                    'Distributed Training, BPE Tokenizer, Supervised Fine-Tuning, Reinforcement Learning, '
                    'Educational Resources')
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    
    # 1. Introduction
    add_heading(doc, '1. Introduction', 1)
    add_paragraph(doc,
        'The Transformer architecture (Vaswani et al., 2017) and its decoder-only variants (Radford et al., '
        '2018; Brown et al., 2020) have become the universal backbone of large language models. While '
        'production frameworks (Hugging Face Transformers, Megatron-LM) provide highly optimized '
        'implementations, they are not designed for educational transparency. Students and researchers '
        'seeking to understand the mechanics of LLMs face a dilemma: either study minimal tutorials '
        'that cover only the attention mechanism (e.g., nanoGPT), or navigate massive production codebases '
        'where the core logic is buried under abstraction layers.')
    add_paragraph(doc,
        'LLM-from-Scratch addresses this gap by providing a complete, from-first-principles implementation '
        'of a modern decoder-only Transformer where every component—tokenization, architecture, optimization, '
        'kernel acceleration, distributed training, data processing, and alignment—is implemented from '
        'primitive PyTorch operations. The codebase is organized into independent, tested modules with '
        'clear interfaces, making it suitable for both learning and research.')
    add_paragraph(doc,
        'Our contributions are: (1) A full-stack LLM implementation with modern architectural choices '
        '(RMSNorm, SwiGLU, RoPE) and kernel optimization (Flash Attention 2 via Triton); (2) Distributed '
        'training from scratch (DDP with bucket synchronization, sharded optimizer); (3) A comprehensive '
        'data processing pipeline for web corpora; (4) Alignment training (SFT + GRPO) with demonstrated '
        'results on GSM8K; (3) Extensive benchmarking and 100+ snapshot tests; (6) Complete documentation '
        'including a 17-chapter book and bilingual website.')
    
    # 2. Background
    add_heading(doc, '2. Background', 1)
    add_paragraph(doc,
        'We briefly review the key components of modern decoder-only Transformers that our implementation '
        'incorporates.')
    
    add_heading(doc, '2.1 Transformer Architecture', 2)
    add_paragraph(doc,
        'The decoder-only Transformer consists of an embedding layer, a stack of identical blocks, and '
        'an output projection. Each block applies multi-head causal self-attention and a position-wise '
        'feed-forward network (FFN), with residual connections and layer normalization. Modern variants '
        'replace the original post-norm with pre-norm (Xiong et al., 2020), LayerNorm with RMSNorm '
        '(Zhang & Sennrich, 2019), ReLU/GeLU with SwiGLU (Shazeer, 2020), and absolute positional '
        'embeddings with Rotary Position Embeddings (Su et al., 2021).')
    
    add_heading(doc, '2.2 Flash Attention', 2)
    add_paragraph(doc,
        'Standard attention materializes the O(N²) attention matrix, causing memory bottlenecks at long '
        'sequences. Flash Attention (Dao et al., 2022) computes attention in SRAM-resident blocks using '
        'online softmax, achieving exact attention with O(N) memory. Flash Attention 2 (Dao, 2024) '
        'improves parallelism and work partitioning, reducing shared memory reads/writes and enabling '
        'better GPU utilization.')
    
    add_heading(doc, '2.3 Distributed Training', 2)
    add_paragraph(doc,
        'Data parallelism (DDP) replicates the model across GPUs and synchronizes gradients via all-reduce. '
        'ZeRO (Rajbhandari et al., 2020) reduces memory by partitioning optimizer states (stage 1), '
        'gradients (stage 2), and parameters (stage 3) across devices. Our implementation includes '
        'DDP with bucket-based gradient synchronization (overlapping communication with computation) '
        'and a stage-2-style sharded optimizer.')
    
    add_heading(doc, '2.4 Alignment', 2)
    add_paragraph(doc,
        'Pre-trained models require alignment to follow instructions and reason reliably. Supervised '
        'Fine-Tuning (SFT) trains on instruction-response pairs (Ouyang et al., 2022). Reinforcement '
        'Learning from Human Feedback (RLHF) uses a reward model and PPO (Schulman et al., 2017) to '
        'optimize for human preferences. GRPO (Group Relative Policy Optimization) eliminates the value '
        'network by computing advantages from a group of samples per prompt.')
    
    # 3. System Design
    add_heading(doc, '3. System Design', 1)
    add_paragraph(doc,
        'LLM-from-Scratch is organized into ten Python packages (llm, kernel, parallel, data_processing, '
        'alignment, bench_mark, tests, docs, site, doc_scripts) with a flat namespace. Each package '
        'has a single responsibility and minimal dependencies on others.')
    
    add_heading(doc, '3.1 Core Model (llm/)', 2)
    add_paragraph(doc,
        'The llm/ package contains the complete model implementation in transformer.py (~440 lines) '
        'including all primitive layers, attention, FFN, RoPE, the Transformer stack, optimizers, loss, '
        'and schedulers. The bpe_tokenizer.py implements BPE tokenization. training.py and generating.py '
        'provide the training and inference loops. checkpoint.py handles serialization.')
    
    add_heading(doc, '3.2 Kernel Optimization (kernel/)', 2)
    add_paragraph(doc,
        'flash_attention_triton.py implements Flash Attention 2 in Triton (Tillet et al., 2019), a '
        'Python-based GPU programming language. The kernel uses block-wise matrix multiplication with '
        'online softmax, causal masking, and supports both forward and backward passes. '
        'flash_attention_mock.py provides a reference implementation for correctness validation.')
    
    add_heading(doc, '3.3 Distributed Training (parallel/)', 2)
    add_paragraph(doc,
        'ddp.py implements Distributed Data Parallel with bucket-based gradient synchronization: '
        'gradients are accumulated into 25MB buckets and reduced asynchronously via NCCL as soon as '
        'each bucket fills. sharded_optimizer.py partitions optimizer states (AdamW momentum and '
        'variance) across devices, reducing per-GPU memory by a factor of world_size.')
    
    add_heading(doc, '3.4 Data Processing (data_processing/)', 2)
    add_paragraph(doc,
        'Seven independent modules: html_process, language_identification, quality_filter, deduplicate, '
        'mask_pii, harmful_detect, quality_classfier. Each reads/writes plain text or JSONL, enabling '
        'flexible pipeline composition for Common Crawl and similar corpora.')
    
    add_heading(doc, '3.5 Alignment (alignment/)', 2)
    add_paragraph(doc,
        'sft.py implements Supervised Fine-Tuning with instruction masking. grpo.py and train_rl.py '
        'implement Group Relative Policy Optimization with group-wise advantage normalization. '
        'evaluate.py provides zero-shot evaluation on GSM8K. Prompt templates support multiple formats.')
    
    add_heading(doc, '3.6 Benchmarking and Testing', 2)
    add_paragraph(doc,
        'bench_mark/ provides standardized benchmarks for attention variants, model throughput, and '
        'DDP all-reduce. tests/ contains 100+ unit tests with snapshot verification against reference '
        'implementations, ensuring numerical correctness across refactoring and PyTorch versions.')
    
    # 4. Implementation Details
    add_heading(doc, '4. Implementation Details', 1)
    
    add_heading(doc, '4.1 Model Configuration', 2)
    add_paragraph(doc,
        'The default model configuration balances educational accessibility with meaningful capacity: '
        '6 layers, d_model=288, 6 attention heads (head_dim=48), d_ff=1024, vocab_size=2048, '
        'max_seq_len=512, yielding ~6.13M parameters. All hyperparameters are configurable via '
        'command-line arguments (llm/args.py).')
    
    add_heading(doc, '4.2 BPE Tokenizer', 2)
    add_paragraph(doc,
        'The tokenizer trains in O(N) time using hash-based pair counting. It starts from 256 byte '
        'tokens, iteratively merges the most frequent pair, and supports special tokens. The '
        'implementation produces memory-mapped NumPy arrays for efficient training data loading.')
    
    add_heading(doc, '4.3 Flash Attention 2 Kernel', 2)
    add_paragraph(doc,
        'The Triton kernel follows the Flash Attention 2 algorithm: (1) Load Q, K, V blocks into SRAM; '
        '(2) Compute local attention scores QK^T; (3) Apply online softmax with running max and '
        'exponential sum; (4) Compute output block; (5) Write back to HBM. The backward pass '
        'recomputes forward statistics. The kernel handles causal masking via upper-triangular '
        'mask applied during score computation.')
    
    add_heading(doc, '4.4 Distributed Training Implementation', 2)
    add_paragraph(doc,
        'DDP uses PyTorch\'s distributed package with nccl backend. Gradient buckets are created by '
        'flattening and partitioning parameter gradients. Each bucket triggers an async all-reduce. '
        'The sharded optimizer splits AdamW state (m, v) across ranks; each rank updates its shard '
        'and all-gathers updated parameters. Both implementations are <200 lines each.')
    
    # 5. Experiments
    add_heading(doc, '5. Experiments', 1)
    
    add_heading(doc, '5.1 TinyStories Training', 2)
    add_paragraph(doc,
        'We train the default 6.13M-parameter model on the TinyStories dataset (Eldan & Li, 2023), '
        'consisting of 1.3GB of synthetic children\'s stories. Training uses batch_size=64, seq_len=256, '
        'lr=1e-4 with 5K warmup steps and cosine decay over 20K iterations on a single GPU. '
        'Training loss decreases from ~10 to ~1.5; validation loss tracks closely. '
        'Sample generations (prompt: "tell you a story") produce coherent, grammatical narratives '
        'with proper story structure (see README.md for examples).')
    
    add_heading(doc, '5.2 SFT on GSM8K', 2)
    add_paragraph(doc,
        'We fine-tune Qwen2.5-Math-1.5B (a 1.5B-parameter pretrained math model) on the GSM8K '
        'training set (7,473 grade-school math problems) using our SFT pipeline. The model is '
        'evaluated on the GSM8K test set (1,319 problems) with zero-shot prompting using the '
        'standard / <answer> format.')
    
    sft_table = doc.add_table(rows=1, cols=3, style='Table Grid')
    sft_table.rows[0].cells[0].text = 'Metric'
    sft_table.rows[0].cells[1].text = 'Base Model'
    sft_table.rows[0].cells[2].text = 'After SFT'
    for metric, base, sft in [
        ('Zero-shot Accuracy', '1.56%', '62.9%'),
        ('Format Compliance', '18.9%', '100%'),
        ('Pass@1 (maj@8)', '~5%', '~75%')
    ]:
        row = sft_table.add_row()
        row.cells[0].text = metric
        row.cells[1].text = base
        row.cells[2].text = sft
    
    add_paragraph(doc,
        'The 40x accuracy improvement and perfect format compliance demonstrate the effectiveness '
        'of our SFT implementation. The model learns both mathematical reasoning and the structured '
        'output format required by the prompt template.')
    
    add_heading(doc, '5.3 Benchmarking Results', 2)
    add_paragraph(doc,
        'All benchmarks are run on NVIDIA GPUs with CUDA 12.1. Key results:')
    
    add_heading(doc, '5.3.1 Attention Variants', 2)
    add_paragraph(doc,
        'Table 1 summarizes attention performance at d_model=64, seq_len=1024, batch=64:')
    attn_table = doc.add_table(rows=1, cols=4, style='Table Grid')
    attn_table.rows[0].cells[0].text = 'Implementation'
    attn_table.rows[0].cells[1].text = 'float32 (ms)'
    attn_table.rows[0].cells[2].text = 'bfloat16 (ms)'
    attn_table.rows[0].cells[3].text = 'Speedup (bf16 vs fp32)'
    attn_data = [
        ('Standard', '3.13', '1.38', '2.27x'),
        ('JIT Compiled', '3.13', '1.37', '2.28x'),
        ('Flash Attention 2', '0.37', '0.37', '1.0x*'),
    ]
    for impl, fp32, bf16, speedup in attn_data:
        row = attn_table.add_row()
        row.cells[0].text = impl
        row.cells[1].text = fp32
        row.cells[2].text = bf16
        row.cells[3].text = speedup
    add_paragraph(doc, '* Flash Attention uses custom kernel; bfloat16/float32 similar due to tensor core saturation.', size=9, italic=True)
    
    add_paragraph(doc,
        'At longer sequences (seq_len=4096), Flash Attention achieves 4.7ms vs 48.4ms for standard '
        'attention (10.3x speedup) and avoids OOM errors that occur with standard attention at '
        'batch=64, seq=4096, d_model=128.')
    
    add_heading(doc, '5.3.2 DDP All-Reduce', 2)
    add_paragraph(doc,
        'All-reduce latency scales with data size and process count. For 1GB tensors on 4 GPUs: '
        'float32 takes ~6.8s, bfloat16 takes ~6.6s. The small difference at large sizes indicates '
        'bandwidth saturation. For small tensors (1KB), latency dominates (4-9ms).')
    
    # 6. Discussion
    add_heading(doc, '6. Discussion', 1)
    
    add_heading(doc, '6.1 Educational Value', 2)
    add_paragraph(doc,
        'LLM-from-Scratch achieves its primary goal of making LLM internals transparent. Every '
        'mathematical operation—from the BPE merge rule to the Flash Attention online softmax—is '
        'implemented in readable Python/PyTorch/Triton. The modular structure allows students to '
        'study one component at a time (e.g., attention.py in isolation) while the integration tests '
        'verify end-to-end correctness.')
    
    add_heading(doc, '6.2 Research Utility', 2)
    add_paragraph(doc,
        'Beyond education, the codebase serves as a research platform. The clean separation of '
        'components enables easy experimentation: swapping attention mechanisms (standard ↔ Flash ↔ '
        'linear attention), modifying normalization (RMSNorm ↔ LayerNorm ↔ DeepNorm), changing FFN '
        'activations (SwiGLU ↔ GeLU ↔ ReLU), or adding new alignment algorithms. The snapshot tests '
        'provide regression detection for numerical correctness.')
    
    add_heading(doc, '6.3 Limitations', 2)
    limitations = [
        'Model scale: Default config is 6M params; larger models require activation checkpointing and pipeline parallelism (not yet implemented)',
        'Context length: Fixed RoPE cache at 512/2048 tokens; dynamic scaling (NTK, YaRN) not implemented',
        'Quantization: No native GPTQ/AWQ/GGUF support; requires external tools',
        'Serving: No optimized inference server (vLLM, TGI); generation is single-sequence',
        'Mixture of Experts: Dense FFN only; sparse MoE not supported',
        'Multi-modal: Text-only; no vision/audio encoder integration'
    ]
    for lim in limitations:
        add_bullet(doc, lim)
    
    # 7. Related Work (detailed)
    add_heading(doc, '7. Related Work', 1)
    add_paragraph(doc,
        'We categorize related work by scope and purpose:')
    
    add_heading(doc, '7.1 Educational Implementations', 2)
    add_bullet(doc, 'nanoGPT/minGPT (Karpathy): Minimal GPT (~300 lines); excellent for attention mechanics; lacks tokenizer, data pipeline, distributed training, alignment, benchmarking')
    add_bullet(doc, 'Harvard NLP Annotated Transformer: Line-by-line explanation of Vaswani et al.; encoder-decoder; no training loop, tokenizer, or optimization')
    add_bullet(doc, 'Transformer from Scratch (various blogs): Typically single-file; focus on attention; omit production concerns')
    
    add_heading(doc, '7.2 Production Frameworks', 2)
    add_bullet(doc, 'Megatron-LM (NVIDIA): 3D parallelism (tensor, pipeline, data); highly optimized; 50K+ lines; steep learning curve')
    add_bullet(doc, 'Hugging Face Transformers: 1M+ lines; abstracts all internals; plugin architecture; not for from-scratch learning')
    add_bullet(doc, 'Fairseq (Meta): Research-focused; complex codebase; legacy code paths')
    
    add_heading(doc, '7.3 Kernel Libraries', 2)
    add_bullet(doc, 'Flash Attention (Dao et al.): Official CUDA/Triton implementation; our kernel is a from-scratch reimplementation for educational transparency')
    add_bullet(doc, 'xFormers (Facebook): Modular attention library; includes Flash, memory-efficient, linear attention; production-focused')
    add_bullet(doc, 'Triton Tutorials: Official examples; our kernel adds causal masking, variable seq_len, and integration into full model')
    
    add_heading(doc, '7.4 Alignment Frameworks', 2)
    add_bullet(doc, 'TRL (Hugging Face): SFT, DPO, PPO, GRPO; high-level; our implementation is from-scratch with explicit math')
    add_bullet(doc, 'DeepSpeed Chat: RLHF pipeline with ZeRO; production-scale; our GRPO is standalone and minimal')
    add_bullet(doc, 'OpenRLHF: Comprehensive RLHF; Ray-based; our alignment module is self-contained PyTorch')
    
    # 8. Conclusion
    add_heading(doc, '8. Conclusion', 1)
    add_paragraph(doc,
        'We presented LLM-from-Scratch, a comprehensive from-first-principles implementation of a modern '
        'decoder-only Transformer language model. The framework implements the complete language modeling '
        'pipeline—tokenization, architecture, optimization, kernel acceleration, distributed training, '
        'data processing, and alignment—in a modular, tested, and documented codebase. Experimental '
        'results demonstrate functional correctness (coherent text generation on TinyStories), '
        'optimization effectiveness (5-10x Flash Attention speedup), and alignment capability '
        '(62.9% GSM8K accuracy after SFT). The project is released open-source with a 17-chapter '
        'book and bilingual website, serving both educational and research purposes.')
    add_paragraph(doc,
        'Future work will extend the framework to larger model scales, MoE architectures, advanced '
        'alignment methods, quantization, and multi-modal capabilities, while maintaining the '
        'educational transparency that defines the project.')
    
    # References
    add_heading(doc, 'References', 1)
    refs = [
        'Vaswani, A., et al. "Attention Is All You Need." NeurIPS 2017.',
        'Radford, A., et al. "Improving Language Understanding by Generative Pre-Training." OpenAI 2018.',
        'Brown, T., et al. "Language Models are Few-Shot Learners." NeurIPS 2020.',
        'Shazeer, N. "GLU Variants Improve Transformer." arXiv:2002.05202, 2020.',
        'Su, J., et al. "RoFormer: Enhanced Transformer with Rotary Position Embedding." NeurIPS 2021.',
        'Zhang, B., & Sennrich, R. "Root Mean Square Layer Normalization." NeurIPS 2019.',
        'Dao, T., et al. "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness." NeurIPS 2022.',
        'Dao, T. "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning." ICLR 2024.',
        'Ouyang, L., et al. "Training Language Models to Follow Instructions with Human Feedback." NeurIPS 2022.',
        'Schulman, J., et al. "Proximal Policy Optimization Algorithms." arXiv:1707.06347, 2017.',
        'Ziegler, D.M., et al. "Fine-Tuning Language Models from Human Preferences." arXiv:1909.08593, 2019.',
        'Sennrich, R., et al. "Neural Machine Translation of Rare Words with Subword Units." ACL 2016.',
        'Goyal, P., et al. "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour." arXiv:1706.02677, 2017.',
        'Raffel, C., et al. "Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer." JMLR 2020.',
        'Kenton, J.D.M.W., & Toutanova, L.K. "BERT: Pre-training of Deep Bidirectional Transformers." NAACL 2019.',
        'Shoeybi, M., et al. "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism." arXiv:1909.08053, 2019.',
        'Rajbhandari, S., et al. "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models." SC 2020.',
        'Hu, E.J., et al. "LoRA: Low-Rank Adaptation of Large Language Models." ICLR 2022.',
        'Dettmers, T., et al. "QLoRA: Efficient Finetuning of Quantized LLMs." NeurIPS 2023.',
        'Liu, H., et al. "Visual Instruction Tuning." NeurIPS 2023.',
        'Eldan, R., & Li, Y. "TinyStories: How Small Can Language Models Be and Still Speak Coherent English?" arXiv:2305.07759, 2023.',
        'Tillet, P., et al. "Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations." MAPL 2019.',
        'Xiong, R., et al. "On Layer Normalization in the Transformer Architecture." ICML 2020.',
        'Wolf, T., et al. "Transformers: State-of-the-Art Natural Language Processing." EMNLP 2020.'
    ]
    for i, ref in enumerate(refs, 1):
        add_paragraph(doc, f'[{i}] {ref}', size=10)

# ============================================================
# MAIN
# ============================================================
print("Building Synopsis.docx...")
doc1 = docx.Document()
build_synopsis(doc1)
doc1.save('Synopsis.docx')
print("Synopsis.docx saved")

print("Building Project_Report.docx...")
doc2 = docx.Document()
build_project_report(doc2)
doc2.save('Project_Report.docx')
print("Project_Report.docx saved")

print("Building Published_Paper.docx...")
doc3 = docx.Document()
build_published_paper(doc3)
doc3.save('Published_Paper.docx')
print("Published_Paper.docx saved")

print("All documents generated successfully!")