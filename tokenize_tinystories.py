import time
import numpy as np
from llm.bpe_tokenizer import BpeTokenizer

def main():
    print("Loading tokenizer from data/tokenizer_small...")
    tokenizer = BpeTokenizer(special_tokens=["<|endoftext|>"])
    tokenizer.load("data/tokenizer_small")
    print(f"Tokenizer loaded with vocabulary size: {len(tokenizer.vcab2id)}")

    # Tokenize training data
    print("Reading from data/TinyStoriesV2-GPT4-train.txt...")
    t0 = time.time()
    # Read first 10MB (~3.2 million tokens) for high quality CPU training
    with open("data/TinyStoriesV2-GPT4-train.txt", "r", encoding="utf-8", errors="replace") as f:
        train_text = f.read(10_000_000)
    print(f"Read {len(train_text)} characters. Tokenizing...")
    train_tokens = tokenizer.encode(train_text)
    train_arr = np.array(train_tokens, dtype=np.uint16)
    np.save("data/training_data.npy", train_arr)
    print(f"Saved {len(train_arr)} tokens to data/training_data.npy in {time.time() - t0:.2f}s")

    # Tokenize validation data
    print("Reading from data/TinyStoriesV2-GPT4-valid.txt...")
    t0 = time.time()
    with open("data/TinyStoriesV2-GPT4-valid.txt", "r", encoding="utf-8", errors="replace") as f:
        valid_text = f.read(1_000_000)
    print(f"Read {len(valid_text)} characters. Tokenizing...")
    valid_tokens = tokenizer.encode(valid_text)
    valid_arr = np.array(valid_tokens, dtype=np.uint16)
    np.save("data/validation_data.npy", valid_arr)
    print(f"Saved {len(valid_arr)} tokens to data/validation_data.npy in {time.time() - t0:.2f}s")

if __name__ == "__main__":
    main()
