# Research: Embedding Pipeline Setup

**Feature**: 001-embedding-pipeline
**Date**: 2025-12-17

## Technology Decisions

### 1. Package Manager: UV

**Decision**: Use UV as the Python package manager
**Rationale**:
- UV is a fast, modern Python package manager written in Rust
- Provides faster dependency resolution than pip
- User explicitly requested UV package manager
**Alternatives Considered**:
- pip: Traditional but slower
- poetry: More complex setup
- pipenv: Slower than UV

### 2. Embedding Service: Cohere

**Decision**: Use Cohere's `embed-english-v3.0` model
**Rationale**:
- User explicitly specified Cohere
- Free tier available (aligns with constitution's "Free-Tier Friendly Architecture")
- `embed-english-v3.0` produces 1024-dimensional vectors
- Supports batch embedding for efficiency
**Configuration**:
- Model: `embed-english-v3.0`
- Embedding dimension: 1024
- Input type: `search_document` for indexing, `search_query` for queries

### 3. Vector Database: Qdrant

**Decision**: Use Qdrant Cloud (free tier) or local Docker instance
**Rationale**:
- User explicitly specified Qdrant
- Free tier: 1GB storage, 1M vectors
- Collection name: `rag_embedding` (user specified)
- Supports upsert operations for re-indexing
**Configuration**:
- Collection: `rag_embedding`
- Vector size: 1024 (matching Cohere)
- Distance metric: Cosine similarity

### 4. URL Extraction: Sitemap Parsing

**Decision**: Parse sitemap.xml to get all URLs
**Rationale**:
- Docusaurus generates sitemap.xml automatically
- More reliable than crawling
- Sitemap already contains all public pages
**Target Sitemap**: `https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml`

### 5. Text Extraction: BeautifulSoup + requests

**Decision**: Use BeautifulSoup4 for HTML parsing
**Rationale**:
- Lightweight, no browser required
- Docusaurus renders static HTML (no JS needed)
- Can target specific content elements (article, main)
**Content Selectors**:
- Primary: `article` tag (Docusaurus main content)
- Fallback: `main` tag
- Exclude: `nav`, `footer`, `aside`, `.navbar`, `.sidebar`

### 6. Text Chunking Strategy

**Decision**: Character-based chunking with overlap
**Rationale**:
- Simpler than token-based (no tokenizer dependency)
- Configurable chunk size and overlap
**Configuration**:
- Chunk size: 1000 characters
- Overlap: 200 characters
- Preserves context across chunks

## Dependencies

```toml
[project]
name = "embedding-pipeline"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "cohere>=5.0.0",
    "qdrant-client>=1.7.0",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
    "python-dotenv>=1.0.0",
]
```

## Environment Variables Required

```
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key
```

## Sitemap Content (29 URLs)

The target site has 29 pages across 4 modules:
- Homepage: 1 page
- Module 1 (ROS 2): 7 pages
- Module 2 (Digital Twin): 8 pages
- Module 3 (NVIDIA Isaac): 6 pages
- Module 4 (VLA): 6 pages

## Function Design

Based on user requirements, single file `main.py` with:

1. `get_all_urls(sitemap_url: str) -> list[str]` - Parse sitemap XML
2. `extract_text_from_url(url: str) -> dict` - Fetch and clean page content
3. `chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]` - Split into chunks
4. `embed(texts: list[str]) -> list[list[float]]` - Generate Cohere embeddings
5. `create_collection(collection_name: str)` - Create Qdrant collection if not exists
6. `save_chunk_to_qdrant(chunks: list, embeddings: list, metadata: dict)` - Upsert to Qdrant
7. `main()` - Orchestrate the pipeline

## Constitution Compliance

| Principle | Status | Notes |
|-----------|--------|-------|
| Simplicity | PASS | Single file design, clear function names |
| Accuracy | PASS | Using official Cohere/Qdrant SDKs |
| Minimalism | PASS | Only essential dependencies |
| Free-Tier Friendly | PASS | Cohere free tier, Qdrant free tier |
| Student-Focused Clarity | PASS | Well-documented functions |
| Documentation-Based | PASS | Following official SDK docs |
| Consistency | PASS | Standard Python conventions |
