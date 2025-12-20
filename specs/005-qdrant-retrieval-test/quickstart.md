# Quickstart: Qdrant Retrieval Testing

**Feature**: 005-qdrant-retrieval-test
**Time to complete**: ~5 minutes

## Prerequisites

- Python 3.10+
- Qdrant vector database with embeddings already stored
- Cohere API key for query embedding generation

## Step 1: Navigate to Backend Directory

```bash
cd backend
```

## Step 2: Install Dependencies (if not already installed)

```bash
# Using UV (if not already installed)
# Windows (PowerShell):
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize project with dependencies
uv add qdrant-client cohere python-dotenv
```

## Step 3: Update Environment File

Ensure your `backend/.env` file contains:

```env
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Step 4: Create retrieving.py

Create `backend/retrieving.py` with the retrieval functions:

```python
import os
import time
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models

# Load environment variables
load_dotenv()

# Configuration constants
COLLECTION_NAME = "rag_embedding"
VECTOR_SIZE = 1024
DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.3
MAX_QUERY_LENGTH = 2000

def initialize_qdrant_client():
    """Initialize Qdrant client with error handling"""
    try:
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url or not qdrant_api_key:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")

        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        return client
    except Exception as e:
        logging.error(f"Failed to initialize Qdrant client: {e}")
        raise

def convert_query_to_embedding(query: str) -> List[float]:
    """
    Convert text query to embedding vector using Cohere API.
    """
    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    co = cohere.Client(cohere_api_key)

    response = co.embed(
        texts=[query],
        model="embed-english-v3.0",  # Same model used in embedding pipeline
        input_type="search_query"  # Using search_query for retrieval
    )

    # Validate that embedding has correct dimensions
    embedding = response.embeddings[0]
    if len(embedding) != VECTOR_SIZE:
        raise ValueError(f"Embedding has {len(embedding)} dimensions, expected {VECTOR_SIZE}")

    return embedding

def validate_retrieval_results(results: List[Dict]) -> bool:
    """
    Validate that retrieved results meet quality criteria.
    """
    for result in results:
        # Check required fields exist
        if not all(key in result for key in ['text', 'url', 'title', 'chunk_index']):
            return False

        # Check text content is not empty
        if not result['text'] or len(result['text'].strip()) == 0:
            return False

        # Check URL is valid (basic check)
        if not result['url'] or not result['url'].startswith(('http://', 'https://')):
            return False

    return True

def format_retrieval_output(results: List[Dict], query: str, execution_time: float, top_k: int) -> Dict[str, Any]:
    """
    Format raw Qdrant results into structured output.
    """
    formatted_results = []

    for point in results:
        payload = point.payload
        formatted_result = {
            "text": payload.get("text", ""),
            "url": payload.get("url", ""),
            "title": payload.get("title", ""),
            "chunk_index": payload.get("chunk_index", 0),
            "similarity_score": point.score
        }
        formatted_results.append(formatted_result)

    return {
        "query": query,
        "results": formatted_results,
        "retrieval_time_ms": execution_time,
        "total_results": len(formatted_results),
        "top_k_requested": top_k
    }

def retrieve(query: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Main retrieval function to search Qdrant for semantically similar content.
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if not (1 <= top_k <= 100):
        raise ValueError("top_k must be between 1 and 100")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters")

    start_time = time.time()

    try:
        # Initialize clients
        qdrant_client = initialize_qdrant_client()

        # Convert query to embedding
        query_embedding = convert_query_to_embedding(query)

        # Perform semantic search in Qdrant
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )

        # Calculate execution time
        execution_time = round((time.time() - start_time) * 1000, 2)

        # Format results
        output = format_retrieval_output(search_results, query, execution_time, top_k)

        # Validate results
        if not validate_retrieval_results(output["results"]):
            logging.warning("Retrieved results did not pass validation")

        return output

    except Exception as e:
        logging.error(f"Retrieval failed: {e}")
        raise

# Example usage
if __name__ == "__main__":
    try:
        # Example retrieval
        results = retrieve("What is ROS 2?", top_k=3)
        print(f"Retrieved {results['total_results']} results in {results['retrieval_time_ms']}ms")

        for i, result in enumerate(results['results']):
            print(f"Result {i+1}:")
            print(f"  URL: {result['url']}")
            print(f"  Title: {result['title']}")
            print(f"  Similarity: {result['similarity_score']:.3f}")
            print(f"  Text Preview: {result['text'][:100]}...")
            print()

    except Exception as e:
        print(f"Error during retrieval: {e}")
```

## Step 5: Run the Retrieval Test

```bash
cd backend
uv run python retrieving.py
```

## Expected Output

```
Retrieved 3 results in 150.25ms
Result 1:
  URL: https://book-writing-hackathon-speckitplus.vercel.app/module-1/
  Title: ROS 2 - The Robotic Nervous System
  Similarity: 0.842
  Text Preview: ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications...

Result 2:
  URL: https://book-writing-hackathon-speckitplus.vercel.app/module-1/architecture
  Title: ROS 2 Architecture
  Similarity: 0.795
  Text Preview: The architecture of ROS 2 is designed to be modular and distributed...

Result 3:
  URL: https://book-writing-hackathon-speckitplus.vercel.app/module-1/communication
  Title: ROS 2 Communication Patterns
  Similarity: 0.756
  Text Preview: Communication in ROS 2 is based on DDS (Data Distribution Service)...
```

## Verification

1. Check that results are semantically relevant to the query
2. Verify that text content matches original stored content
3. Confirm that metadata (URL, title, chunk_index) is correctly returned
4. Validate that JSON output structure is consistent

## Troubleshooting

| Error | Solution |
|-------|----------|
| `QDRANT_URL not set` | Add URL to `.env` file |
| `Connection refused` | Check QDRANT_URL is correct |
| `401 Unauthorized` | Verify API keys are valid |
| `Collection not found` | Ensure embedding pipeline has populated the collection |
| `Rate limit exceeded` | Add delays between requests or upgrade API tier |