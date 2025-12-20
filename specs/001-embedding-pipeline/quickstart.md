# Quickstart: Embedding Pipeline

**Feature**: 001-embedding-pipeline
**Time to complete**: ~10 minutes

## Prerequisites

- Python 3.10+
- Cohere API key (free tier: https://dashboard.cohere.com/api-keys)
- Qdrant Cloud account (free tier: https://cloud.qdrant.io/)

## Step 1: Create Backend Folder

```bash
# From repository root
mkdir backend
cd backend
```

## Step 2: Initialize with UV

```bash
# Install UV if not installed
# Windows (PowerShell):
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project
uv init
```

## Step 3: Add Dependencies

```bash
uv add cohere qdrant-client requests beautifulsoup4 python-dotenv
```

## Step 4: Create Environment File

Create `backend/.env`:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Step 5: Create main.py

Create `backend/main.py` with the 7 functions:
- `get_all_urls(sitemap_url)`
- `extract_text_from_url(url)`
- `chunk_text(text, chunk_size, overlap)`
- `embed(texts)`
- `create_collection(collection_name)`
- `save_chunk_to_qdrant(chunks, embeddings, url, title)`
- `main()`

## Step 6: Run the Pipeline

```bash
cd backend
uv run python main.py
```

## Expected Output

```
Creating collection: rag_embedding
Fetching sitemap: https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml
Found 29 URLs
Processing: https://book-writing-hackathon-speckitplus.vercel.app/
  - Extracted 2500 characters
  - Created 3 chunks
  - Generated embeddings
  - Saved to Qdrant
Processing: https://book-writing-hackathon-speckitplus.vercel.app/module-1/
  ...
Pipeline complete! Processed 29 pages.
```

## Verify in Qdrant

1. Go to https://cloud.qdrant.io/
2. Select your cluster
3. Click on `rag_embedding` collection
4. You should see points with payloads containing `text`, `url`, `title`

## Troubleshooting

| Error | Solution |
|-------|----------|
| `COHERE_API_KEY not set` | Add key to `.env` file |
| `Connection refused` | Check QDRANT_URL is correct |
| `401 Unauthorized` | Verify API keys are valid |
| `Collection not found` | Run `create_collection()` first |

## Project Structure (Final)

```
backend/
├── .env              # API keys (gitignored)
├── .python-version   # Python version for UV
├── pyproject.toml    # Dependencies
├── uv.lock          # Lock file
└── main.py          # Pipeline implementation
```
