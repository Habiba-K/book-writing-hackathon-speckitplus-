# Research: Qdrant Retrieval Testing

**Feature**: 005-qdrant-retrieval-test
**Date**: 2025-12-17

## Technology Decisions

### 1. Qdrant Client for Retrieval
**Decision**: Use Qdrant Python client for retrieval operations
**Rationale**:
- Official Qdrant client provides proper SDK for search operations
- Supports semantic search with configurable top-k results
- Handles metadata retrieval correctly
- User already has Qdrant client dependency from embedding pipeline

**Configuration**:
- Search method: `search()` with vector query
- Distance metric: Cosine similarity (matches embedding pipeline)
- Top-k parameter: Configurable via function parameter

### 2. Text Similarity Approach
**Decision**: Use semantic search via vector similarity rather than keyword search
**Rationale**:
- Aligns with embedding pipeline that stores semantic vectors
- Enables true RAG functionality with semantic matching
- More effective than keyword matching for documentation retrieval
- Matches Cohere embedding model capabilities

**Implementation**:
- Convert query text to embedding using same Cohere model as pipeline
- Use embedding vector for semantic search in Qdrant
- Return top-k results based on cosine similarity

### 3. Metadata Retrieval
**Decision**: Retrieve complete metadata (URL, chunk_id, title, text) with each result
**Rationale**:
- Essential for verification of retrieval accuracy
- Enables source tracing for retrieved content
- Critical for RAG applications
- Matches requirements in feature spec

**Payload Structure**:
- text: Original chunk content
- url: Source URL for citation
- title: Page title for context
- chunk_index: Position in original document

### 4. Error Handling Strategy
**Decision**: Implement comprehensive error handling for retrieval operations
**Rationale**:
- Qdrant may be unavailable or rate-limited
- Queries may be malformed or empty
- Network issues can occur during API calls
- Need graceful degradation with clear error messages

**Approach**:
- Try-catch blocks around Qdrant operations
- Specific handling for empty queries
- Connection error detection and retry logic
- Validation of query parameters before search

### 5. Output Format
**Decision**: Return clean JSON structure with consistent fields
**Rationale**:
- Required by feature specification
- Enables integration with other services
- Facilitates testing and validation
- Provides structured data for RAG applications

**JSON Structure**:
```json
{
  "query": "original query text",
  "results": [
    {
      "text": "retrieved chunk text",
      "url": "source URL",
      "title": "page title",
      "chunk_index": 0,
      "similarity_score": 0.95
    }
  ],
  "retrieval_time_ms": 150
}
```

## Dependencies

```toml
[project]
name = "qdrant-retrieval-test"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "qdrant-client>=1.7.0",
    "cohere>=5.0.0",
    "python-dotenv>=1.0.0",
]
```

## Environment Variables Required

```
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
```

## Function Design

Based on user requirements, single file `retrieving.py` with:

1. `retrieve(query: str, top_k: int = 5) -> dict` - Main retrieval function
2. `convert_query_to_embedding(query: str) -> list[float]` - Query embedding
3. `validate_retrieval_results(results: list) -> bool` - Result validation
4. `format_retrieval_output(results: list, query: str, execution_time: float) -> dict` - Output formatting

## Constitution Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| Simplicity | PASS | Single file design with clear function separation |
| Accuracy | PASS | Using official Qdrant/Cohere SDKs |
| Minimalism | PASS | Only essential dependencies and functions |
| Free-Tier Friendly | PASS | Uses free-tier Qdrant/Cohere |
| Student-Focused Clarity | PASS | Well-documented functions |
| Documentation-Based | PASS | Following official SDK docs |
| Consistency | PASS | Standard Python conventions |