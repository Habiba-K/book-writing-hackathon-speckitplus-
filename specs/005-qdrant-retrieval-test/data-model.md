# Data Model: Qdrant Retrieval Testing

**Feature**: 005-qdrant-retrieval-test
**Date**: 2025-12-17

## Entities

### 1. RetrievalQuery
Represents a search query submitted for semantic retrieval.

| Field | Type | Description |
|-------|------|-------------|
| query_text | string | The text content of the search query |
| top_k | int | Number of results to retrieve (default: 5) |
| query_embedding | float[1024] | Vector embedding of the query text |

### 2. RetrievedResult
A single result returned from the Qdrant semantic search.

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique identifier for the retrieved chunk |
| text | string | The original text content of the chunk |
| url | string | Source URL where the content originated |
| title | string | Title of the source page |
| chunk_index | int | Position of this chunk in the original document |
| similarity_score | float | Cosine similarity score between query and result |
| vector | float[1024] | The stored embedding vector |

### 3. RetrievalResponse
The structured response returned by the retrieval system.

| Field | Type | Description |
|-------|------|-------------|
| query | string | The original query text |
| results | array[RetrievedResult] | Array of retrieved results |
| retrieval_time_ms | int | Time taken to perform the retrieval |
| total_results | int | Total number of results returned |
| top_k_requested | int | Number of results requested |

## Qdrant Collection Schema

**Collection Name**: `rag_embedding` (same as embedding pipeline)

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
User Query
    │
    ▼
┌─────────────────┐
│ convert_query_to_embedding  │ → Query embedding vector
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Qdrant Search   │ → Top-k similar vectors with payloads
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ format_results  │ → Structured RetrievalResponse
└─────────────────┘
```

## Validation Rules

1. **Query Validation**: Query text must be non-empty and not exceed 2000 characters
2. **Top-K Validation**: top_k parameter must be between 1 and 100
3. **Similarity Threshold**: Results should have similarity score > 0.3 (configurable)
4. **Content Integrity**: Retrieved text chunks must match stored content exactly
5. **Metadata Completeness**: Each result must include URL, title, and chunk_index