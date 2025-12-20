# Function Contracts: main.py

**Feature**: 001-embedding-pipeline
**Date**: 2025-12-17

## Overview

Single file implementation with 7 functions as specified by user.

---

## 1. get_all_urls

```python
def get_all_urls(sitemap_url: str) -> list[str]:
    """
    Parse sitemap.xml and extract all page URLs.

    Args:
        sitemap_url: Full URL to sitemap.xml
                     e.g., "https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml"

    Returns:
        List of page URLs found in sitemap

    Raises:
        requests.RequestException: If sitemap cannot be fetched

    Example:
        urls = get_all_urls("https://example.com/sitemap.xml")
        # Returns: ["https://example.com/", "https://example.com/page1", ...]
    """
```

---

## 2. extract_text_from_url

```python
def extract_text_from_url(url: str) -> dict:
    """
    Fetch page and extract clean text content.

    Args:
        url: Full URL of the page to extract

    Returns:
        Dictionary with keys:
        - "url": str - the source URL
        - "title": str - page title (from <title> or <h1>)
        - "text": str - cleaned text content

    Raises:
        requests.RequestException: If page cannot be fetched

    Example:
        doc = extract_text_from_url("https://example.com/page1")
        # Returns: {"url": "...", "title": "Page Title", "text": "Content..."}
    """
```

---

## 3. chunk_text

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: Full text content to chunk
        chunk_size: Maximum characters per chunk (default: 1000)
        overlap: Characters to overlap between chunks (default: 200)

    Returns:
        List of text chunks

    Example:
        chunks = chunk_text("Long text content...", chunk_size=500, overlap=100)
        # Returns: ["First chunk...", "...overlap first chunk second...", ...]
    """
```

---

## 4. embed

```python
def embed(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for text chunks using Cohere.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (each 1024 dimensions)

    Raises:
        cohere.CohereError: If API call fails

    Environment:
        Requires COHERE_API_KEY

    Example:
        vectors = embed(["Hello world", "Another text"])
        # Returns: [[0.1, 0.2, ...], [0.3, 0.4, ...]]
    """
```

---

## 5. create_collection

```python
def create_collection(collection_name: str = "rag_embedding") -> None:
    """
    Create Qdrant collection if it doesn't exist.

    Args:
        collection_name: Name of the collection (default: "rag_embedding")

    Environment:
        Requires QDRANT_URL and QDRANT_API_KEY

    Notes:
        - Vector size: 1024 (Cohere embed-english-v3.0)
        - Distance: Cosine
        - Idempotent: Safe to call multiple times

    Example:
        create_collection("rag_embedding")
    """
```

---

## 6. save_chunk_to_qdrant

```python
def save_chunk_to_qdrant(
    chunks: list[str],
    embeddings: list[list[float]],
    url: str,
    title: str,
    collection_name: str = "rag_embedding"
) -> None:
    """
    Upsert chunks with embeddings to Qdrant.

    Args:
        chunks: List of text chunks
        embeddings: Corresponding embedding vectors
        url: Source URL for metadata
        title: Source page title for metadata
        collection_name: Target collection (default: "rag_embedding")

    Notes:
        - Uses deterministic IDs for upsert behavior
        - Stores text, url, title, chunk_index in payload

    Example:
        save_chunk_to_qdrant(
            chunks=["chunk1", "chunk2"],
            embeddings=[[0.1, ...], [0.2, ...]],
            url="https://example.com/page",
            title="Page Title"
        )
    """
```

---

## 7. main

```python
def main() -> None:
    """
    Execute the complete embedding pipeline.

    Steps:
        1. Load environment variables
        2. Create Qdrant collection
        3. Fetch all URLs from sitemap
        4. For each URL:
           a. Extract text
           b. Chunk text
           c. Generate embeddings
           d. Save to Qdrant
        5. Print summary

    Environment:
        - COHERE_API_KEY: Cohere API key
        - QDRANT_URL: Qdrant server URL
        - QDRANT_API_KEY: Qdrant API key

    Example:
        python main.py
    """
```

---

## Constants

```python
SITEMAP_URL = "https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml"
COLLECTION_NAME = "rag_embedding"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COHERE_MODEL = "embed-english-v3.0"
VECTOR_SIZE = 1024
```
