#!/usr/bin/env python3
"""
embedder.py — Text Embedding Module for Chronocodex

Author: Bradley Ryan Kinnard
License: MIT

Description:
Provides functions to convert text into vector embeddings using OpenAI's API.
Maintains compatibility with modular embedding injection patterns.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --- Direct embedding function using OpenAI v1 client ---
def embed_text_openai(text: str) -> list[float]:
    """
    Embed the given text using OpenAI's Embedding API (text-embedding-ada-002).
    Returns a list of floats representing the embedding vector.
    """
    if not text or not text.strip():
        return []
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[text]
        )
        return response.data[0].embedding
    except Exception as e:
        raise RuntimeError(f"Embedding error: {e}")

def embed_summary(text: str) -> list[float]:
    """
    Generate an embedding vector for the given text using OpenAI's API.
    Alias to embed_text_openai for CLI compatibility.
    """
    return embed_text_openai(text)

# --- Wrapper for compatibility with potential embedder interfaces ---
def embed_text(text: str, embedder=None) -> list[float]:
    """
    Embed text using an optional embedder interface. Defaults to OpenAI direct.
    """
    if embedder and hasattr(embedder, "embed_query"):
        return embedder.embed_query(text)
    return embed_text_openai(text)

# Optional test block for standalone usage
if __name__ == "__main__":
    sample = "def foo():\n    return 42"
    vec = embed_summary(sample)
    print("Embedding length:", len(vec), "sample data:", vec[:5])
