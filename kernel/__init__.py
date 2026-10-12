from .flash_attention_mock import *

try:
    from .flash_attention_triton import *
except ImportError:
    pass
