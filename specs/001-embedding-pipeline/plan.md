# Implementation Plan: Embedding Pipeline Setup

**Branch**: `001-embedding-pipeline` | **Date**: 2025-12-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-embedding-pipeline/spec.md`

## Summary

Build a Python backend pipeline that extracts text from the deployed Docusaurus site (`https://book-writing-hackathon-speckitplus.vercel.app/`), generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval. Single file design (`main.py`) with 7 core functions, using UV package manager.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: cohere, qdrant-client, requests, beautifulsoup4, python-dotenv
**Package Manager**: UV (user specified)
**Storage**: Qdrant Cloud (free tier) - Collection: `rag_embedding`
**Testing**: Manual verification via Qdrant dashboard
**Target Platform**: CLI script (cross-platform)
**Project Type**: Single file backend script
**Performance Goals**: Process 29 pages in under 5 minutes
**Constraints**: Free-tier APIs only (Cohere, Qdrant)
**Scale/Scope**: 29 pages, ~100-200 text chunks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. Simplicity | PASS | Single file with 7 clearly named functions |
| II. Accuracy | PASS | Using official Cohere/Qdrant Python SDKs |
| III. Minimalism | PASS | Only 5 dependencies, no extras |
| IV. Free-Tier Friendly | PASS | Cohere free tier (1000 calls/month), Qdrant free tier (1GB) |
| V. Student-Focused Clarity | PASS | Clear function names, documented signatures |
| VI. Documentation-Based | PASS | Following official SDK documentation |
| VII. Consistency | PASS | Standard Python naming conventions |

**Gate Result**: PASS - No violations

## Project Structure

### Documentation (this feature)

```text
specs/001-embedding-pipeline/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
├── contracts/           # Function signatures
│   └── function-signatures.md
└── tasks.md             # (Created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── .env                 # API keys (gitignored)
├── .python-version      # Python version for UV
├── pyproject.toml       # UV project config
├── uv.lock             # Dependency lock
└── main.py             # Pipeline implementation (single file)
```

**Structure Decision**: Single project with one Python file as explicitly requested by user. No tests directory as this is a script-based pipeline.

## Implementation Details

### Target Site
- **Base URL**: `https://book-writing-hackathon-speckitplus.vercel.app/`
- **Sitemap**: `https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml`
- **Total Pages**: 29

### Functions in main.py

| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `get_all_urls` | Parse sitemap.xml | sitemap_url | list[str] |
| `extract_text_from_url` | Fetch & clean page | url | dict (url, title, text) |
| `chunk_text` | Split into segments | text, size, overlap | list[str] |
| `embed` | Cohere embeddings | list[str] | list[vector] |
| `create_collection` | Init Qdrant collection | collection_name | None |
| `save_chunk_to_qdrant` | Upsert embeddings | chunks, vectors, metadata | None |
| `main` | Orchestrate pipeline | None | None |

### Configuration Constants

```python
SITEMAP_URL = "https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml"
COLLECTION_NAME = "rag_embedding"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COHERE_MODEL = "embed-english-v3.0"
VECTOR_SIZE = 1024
```

### Environment Variables

```env
COHERE_API_KEY=xxx
QDRANT_URL=https://xxx.cloud.qdrant.io:6333
QDRANT_API_KEY=xxx
```

## Complexity Tracking

> No violations to justify - all principles satisfied.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

## Phase Completion

- [x] Phase 0: Research (research.md)
- [x] Phase 1: Design (data-model.md, contracts/, quickstart.md)
- [ ] Phase 2: Tasks (run `/sp.tasks` to generate)

## Next Steps

Run `/sp.tasks` to generate the implementation task list.
