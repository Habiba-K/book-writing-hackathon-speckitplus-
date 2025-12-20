# Qdrant Retrieval System

A Python-based retrieval system that queries Qdrant vector database to retrieve semantically similar content using Cohere embeddings. This system complements the embedding pipeline by providing retrieval capabilities for RAG applications.

## RAG Agent Integration

This system includes a RAG (Retrieval-Augmented Generation) agent that uses OpenAI's API to generate contextual answers based on the retrieved information. The agent integrates with the existing retrieval functionality to provide comprehensive question-answering capabilities.

## FastAPI Integration

The RAG agent is also available through a FastAPI web service with the following endpoints:

- `/ask` - Process user queries through the RAG agent
- `/health` - Health check endpoint

To run the API server:
```bash
uvicorn api:app --reload --port 8000
```

## Setup

1. Install UV package manager:
   ```bash
   # For Windows (PowerShell):
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # For Linux/macOS:
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Install dependencies:
   ```bash
   cd backend
   uv add qdrant-client cohere python-dotenv
   ```

3. Set up environment variables:
   ```bash
   # Copy the example file and add your keys
   cp .env .env.local
   # Edit .env.local and add your API keys
   ```

4. Set up environment variables:
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here  # Format: sk-... followed by 48 characters
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io:6333
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Features

- Semantic search using Cohere embeddings
- Qdrant vector database integration
- Configurable top-k retrieval
- Comprehensive result validation
- Performance timing and monitoring
- Command-line interface for easy testing
- Integration with existing embedding pipeline

## Usage

### Command Line Interface

The system provides a command-line interface for easy testing:

```bash
# Run comprehensive tests
python retrieving.py --test-mode

# Query with custom parameters
python retrieving.py --query "What is ROS 2?" --top_k 5

# Get help
python retrieving.py --help
```

### Direct Function Usage

```python
from retrieving import retrieve

# Basic retrieval
results = retrieve("What is ROS 2?", top_k=3)
print(f"Retrieved {results['total_results']} results in {results['retrieval_time_ms']}ms")

# Access individual results
for result in results['results']:
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    print(f"Similarity: {result['similarity_score']:.3f}")
    print(f"Text: {result['text'][:100]}...")
```

### RAG Agent Usage

The RAG agent provides a complete question-answering system that combines retrieval with answer generation:

```bash
# Run the agent test
python agent.py
```

```python
from agent import RAGAgent

# Initialize the agent
agent = RAGAgent()

# Process a query
response = agent.process_query("What is ROS 2?")
print(f"Answer: {response['answer']}")
print(f"Sources: {len(response['sources'])}")
print(f"Query time: {response['query_time']}s")
print(f"Success: {response['success']}")
```

## Functions

### `retrieve(query: str, top_k: int = 5) -> Dict[str, Any]`
Main retrieval function to search Qdrant for semantically similar content.

Parameters:
- `query`: Text query for semantic search
- `top_k`: Number of top results to return (default: 5)

Returns:
- Dictionary with query, results, retrieval time, and metadata

### `initialize_qdrant_client() -> QdrantClient`
Initialize Qdrant client with error handling and connection validation.

### `convert_query_to_embedding(query: str) -> List[float]`
Convert text query to embedding vector using Cohere API.

### `validate_retrieval_results(results: List[Dict], original_texts: List[str] = None) -> bool`
Validate that retrieved results meet quality criteria.

### `format_retrieval_output(results: List[Dict], query: str, execution_time: float, top_k: int) -> Dict[str, Any]`
Format raw Qdrant results into structured output.

## Response Format

The retrieval function returns a dictionary with the following structure:

```json
{
  "query": "What is ROS 2?",
  "results": [
    {
      "text": "ROS 2 (Robot Operating System 2) is a flexible framework...",
      "url": "https://example.com/ros2-intro",
      "title": "Introduction to ROS 2",
      "chunk_index": 0,
      "similarity_score": 0.856
    }
  ],
  "retrieval_time_ms": 150.25,
  "total_results": 3,
  "top_k_requested": 3,
  "timing_info": {
    "client_initialization_ms": 25.1,
    "embedding_generation_ms": 75.3,
    "search_execution_ms": 50.1,
    "total_retrieval_ms": 150.25
  }
}
```

## Configuration Constants

- `COLLECTION_NAME`: "rag_embedding" - Qdrant collection name
- `VECTOR_SIZE`: 1024 - Dimension of embeddings
- `DEFAULT_TOP_K`: 5 - Default number of results
- `SIMILARITY_THRESHOLD`: 0.3 - Minimum similarity threshold
- `MAX_QUERY_LENGTH`: 2000 - Maximum query length in characters

## Error Handling

The system includes comprehensive error handling:
- Input validation for queries and parameters
- Connection error handling for Qdrant and Cohere
- Retry mechanism with exponential backoff
- Graceful failure with informative error messages

## Testing

Run the comprehensive test suite:

```bash
python retrieving.py --test-mode
```

This will run:
- Multiple query types and top_k values
- Acceptance scenario validation
- Performance testing
- Error handling verification

## Performance

The system is designed to achieve response times under 2 seconds. Performance timing is included for each stage:
- Client initialization
- Embedding generation
- Search execution
- Total retrieval time