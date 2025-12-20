# Data Model: Embedding Pipeline

**Feature**: 001-embedding-pipeline
**Date**: 2025-12-17

## Entities

### 1. Document

Represents a single page from the Docusaurus site.

| Field | Type | Description |
|-------|------|-------------|
| url | string | Full URL of the page |
| title | string | Page title extracted from HTML |
| text | string | Cleaned text content |
| fetched_at | datetime | When the page was fetched |

### 2. TextChunk

A segment of document text suitable for embedding.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier (hash of url + chunk_index) |
| text | string | Chunk text content |
| chunk_index | int | Position in the original document (0-based) |
| source_url | string | URL of the parent document |
| source_title | string | Title of the parent document |

### 3. Embedding (Qdrant Point)

Vector representation stored in Qdrant.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Same as TextChunk.id (for upsert) |
| vector | float[1024] | Cohere embedding vector |
| payload.text | string | Original chunk text |
| payload.url | string | Source URL |
| payload.title | string | Source page title |
| payload.chunk_index | int | Chunk position |

## Qdrant Collection Schema

**Collection Name**: `rag_embedding`

```json
{
  "name": "rag_embedding",
  "vectors": {
    "size": 1024,
    "distance": "Cosine"
  }
}
```

### Payload Schema

```json
{
  "text": "string - the chunk text for display",
  "url": "string - source URL for citation",
  "title": "string - page title for context",
  "chunk_index": "integer - position in document"
}
```

## Data Flow

```
Sitemap XML
    │
    ▼
┌─────────────────┐
│  get_all_urls   │  → List of 29 URLs
└─────────────────┘
    │
    ▼
┌─────────────────────────┐
│ extract_text_from_url   │  → Document (url, title, text)
└─────────────────────────┘
    │
    ▼
┌─────────────────┐
│   chunk_text    │  → List of TextChunks
└─────────────────┘
    │
    ▼
┌─────────────────┐
│     embed       │  → List of Embeddings (vectors)
└─────────────────┘
    │
    ▼
┌─────────────────────────┐
│  save_chunk_to_qdrant   │  → Qdrant Points (upserted)
└─────────────────────────┘
```

## ID Generation Strategy

To enable upsert (update existing, insert new), each chunk needs a stable ID:

```python
import hashlib

def generate_chunk_id(url: str, chunk_index: int) -> str:
    """Generate deterministic ID for upsert capability."""
    content = f"{url}:{chunk_index}"
    return hashlib.md5(content.encode()).hexdigest()
```

This ensures:
- Same URL + chunk_index = same ID (enables update on re-run)
- Different chunks get different IDs
- No collisions between pages
