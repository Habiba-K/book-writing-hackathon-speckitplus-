# Quickstart: RAG Agent with Groq API

**Feature**: 001-rag-agent
**Time to complete**: ~10 minutes

## Prerequisites

- Python 3.10+
- Groq API key
- Existing Qdrant vector database with embeddings
- Cohere API key
- Existing retrieval functionality (retrieving.py)

## Step 1: Navigate to Backend Directory

```bash
cd backend
```

## Step 2: Install Dependencies

```bash
# Using UV (if not already installed)
# Windows (PowerShell):
# powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install required dependencies
uv add groq python-dotenv
```

## Step 3: Update Environment File

Ensure your `backend/.env` file contains:

```env
GROQ_API_KEY=your_groq_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Step 4: Create agent.py

Create `backend/agent.py` with the RAG agent implementation:

```python
import os
import time
import logging
from typing import Dict, Any, List
from dotenv import load_dotenv
from groq import Groq
from retrieving import retrieve  # Import the existing retrieve function

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
AGENT_NAME = "RAG-Agent"
AGENT_INSTRUCTIONS = "You are a helpful assistant that answers questions using retrieved information from the Physical AI & Humanoid Robotics book content. Provide concise answers and cite sources. If the question is not related to the book content, respond with 'sorry this content is not related to this book.'"
AGENT_MODEL = "llama-3.1-8b-instant"  # Groq-supported model
MAX_QUERY_LENGTH = 2000  # Maximum length of user query in characters
DEFAULT_TIMEOUT = 30  # Default timeout for agent operations in seconds
OUT_OF_SCOPE_RESPONSE = "sorry this content is not related to this book"

class RAGAgent:
    """
    RAG Agent using Groq API that integrates with existing retrieval functionality
    and supports single clickable source display and out-of-scope query handling.
    """

    def __init__(self):
        """
        Initialize the RAG agent with Groq client and configuration.
        """
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")

        self.client = Groq(api_key=groq_api_key)
        self.model = AGENT_MODEL

    def process_query(self, query: str) -> Dict[str, Any]:
        """
        Process a user query through the RAG agent.

        Args:
            query: Natural language question or request from user

        Returns:
            Dictionary with answer, primary_source, sources, matched chunks, and metadata
        """
        if not query or len(query.strip()) == 0:
            raise ValueError("Query cannot be empty")

        if len(query) > MAX_QUERY_LENGTH:
            raise ValueError(f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters")

        start_time = time.time()

        try:
            # Check if query is within scope
            is_out_of_scope = self._check_query_scope(query)

            if is_out_of_scope:
                # Return out-of-scope response without retrieval
                query_time = round(time.time() - start_time, 2)
                return {
                    "answer": OUT_OF_SCOPE_RESPONSE,
                    "primary_source": None,
                    "sources": [],
                    "matched_chunks": [],
                    "query_time": query_time,
                    "success": True,
                    "is_out_of_scope": True
                }

            # Use the existing retrieve function to get relevant information
            retrieval_results = retrieve(query, top_k=5)

            # Format the retrieved information for the LLM
            context = self._format_context_for_llm(retrieval_results)

            # Generate an answer using the Groq API
            answer = self._generate_answer(query, context)

            # Calculate query time
            query_time = round(time.time() - start_time, 2)

            # Extract sources and chunks
            sources = self._extract_sources(retrieval_results)
            matched_chunks = self._extract_chunks(retrieval_results)

            # Select the primary source for clickable display
            primary_source = self._select_primary_source(sources) if sources else None

            # Format the response according to the required structure
            response = {
                "answer": answer,
                "primary_source": primary_source,
                "sources": sources,
                "matched_chunks": matched_chunks,
                "query_time": query_time,
                "success": True,
                "is_out_of_scope": False
            }

            return response

        except Exception as e:
            logging.error(f"Error processing query: {e}")
            query_time = round(time.time() - start_time, 2)

            return {
                "answer": "",
                "primary_source": None,
                "sources": [],
                "matched_chunks": [],
                "query_time": query_time,
                "success": False,
                "is_out_of_scope": False,
                "error": str(e)
            }

    def _check_query_scope(self, query: str) -> bool:
        """
        Check if the query is within the book's scope.

        Args:
            query: The user's query to check

        Returns:
            Boolean indicating if the query is within the book's scope
        """
        # Define scope keywords related to the book content
        scope_keywords = [
            "physical ai", "humanoid robotics", "ros 2", "isaac", "qdrant",
            "robotics", "ai", "machine learning", "computer vision", "navigation",
            "manipulation", "locomotion", "sensor fusion", "control systems"
        ]

        query_lower = query.lower()

        # Check if any scope keyword appears in the query
        for keyword in scope_keywords:
            if keyword in query_lower:
                return False  # Query is in scope

        # If no scope-related keywords found, likely out of scope
        return True

    def _select_primary_source(self, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Select the most relevant source to be displayed as the single clickable source.

        Args:
            sources: List of all retrieved sources

        Returns:
            The most relevant source to display as primary source
        """
        # For now, return the first source as primary
        # In a more sophisticated implementation, this could use similarity scores
        # or other relevance metrics
        if sources:
            return sources[0]
        return None

    def _format_context_for_llm(self, retrieval_results: Dict[str, Any]) -> str:
        """
        Format retrieval results into a context string for the LLM.

        Args:
            retrieval_results: Results from the retrieve function

        Returns:
            Formatted context string
        """
        context_parts = ["Here is the relevant information to answer the user's query:"]

        for i, result in enumerate(retrieval_results.get("results", [])):
            text = result.get("text", "")
            url = result.get("url", "")
            title = result.get("title", "")
            similarity = result.get("similarity_score", 0)

            context_parts.append(
                f"Document {i+1}: {title}\n"
                f"URL: {url}\n"
                f"Similarity: {similarity}\n"
                f"Content: {text}\n"
            )

        return "\n".join(context_parts)

    def _generate_answer(self, query: str, context: str) -> str:
        """
        Generate an answer using the Groq API with the provided context.

        Args:
            query: Original user query
            context: Formatted context from retrieval results

        Returns:
            Generated answer string
        """
        prompt = (
            "Please answer the user's question based on the following context. "
            "Provide a clean, readable answer without citation prefixes like 'According to Document 1:'. "
            "If the context doesn't contain sufficient information, please say so. "
            "Always cite your sources when providing information from the context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}"
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": AGENT_INSTRUCTIONS},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1000
        )

        return response.choices[0].message.content

    def _extract_sources(self, retrieval_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract sources from retrieval results.

        Args:
            retrieval_results: Results from the retrieve function

        Returns:
            List of source dictionaries
        """
        sources = []
        for result in retrieval_results.get("results", []):
            source = {
                "url": result.get("url", ""),
                "title": result.get("title", ""),
                "chunk_index": result.get("chunk_index", 0)
            }
            sources.append(source)

        return sources

    def _extract_chunks(self, retrieval_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract content chunks from retrieval results.

        Args:
            retrieval_results: Results from the retrieve function

        Returns:
            List of chunk dictionaries
        """
        chunks = []
        for result in retrieval_results.get("results", []):
            chunk = {
                "text": result.get("text", ""),
                "similarity_score": result.get("similarity_score", 0.0),
                "source": {
                    "url": result.get("url", ""),
                    "title": result.get("title", ""),
                    "chunk_index": result.get("chunk_index", 0)
                }
            }
            chunks.append(chunk)

        return chunks


def main():
    """
    Main function for testing the RAG agent.
    """
    print("RAG Agent - Test Mode")

    try:
        # Initialize the agent
        agent = RAGAgent()
        print("Agent initialized successfully")

        # Test query in scope
        test_query = "What is ROS 2?"
        print(f"\nProcessing query: '{test_query}'")

        # Process the query
        response = agent.process_query(test_query)

        print(f"Success: {response['success']}")
        print(f"Is out of scope: {response['is_out_of_scope']}")
        print(f"Query time: {response['query_time']}s")
        print(f"Answer: {response['answer'][:200]}...")
        print(f"Primary source: {response['primary_source']}")
        print(f"Sources: {len(response['sources'])} found")
        print(f"Chunks: {len(response['matched_chunks'])} retrieved")

        # Test query out of scope
        out_of_scope_query = "What is quantum physics?"
        print(f"\nProcessing out-of-scope query: '{out_of_scope_query}'")

        out_of_scope_response = agent.process_query(out_of_scope_query)
        print(f"Success: {out_of_scope_response['success']}")
        print(f"Is out of scope: {out_of_scope_response['is_out_of_scope']}")
        print(f"Answer: {out_of_scope_response['answer']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

## Step 5: Run the Agent Test

```bash
cd backend
python agent.py
```

## Expected Output

```
RAG Agent - Test Mode
Agent initialized successfully

Processing query: 'What is ROS 2?'
Success: True
Is out of scope: False
Query time: 2.45s
Answer: ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications...
Primary source: {'url': '...', 'title': '...', 'chunk_index': 0}
Sources: 5 found
Chunks: 5 retrieved

Processing out-of-scope query: 'What is quantum physics?'
Success: True
Is out of scope: True
Answer: sorry this content is not related to this book
```

## Verification

1. Check that the agent returns answers with primary_source, sources, and matched chunks
2. Verify that query time is within acceptable limits (<5 seconds)
3. Confirm that the response follows the clean JSON format with no citation prefixes
4. Test error handling with invalid queries
5. Verify that out-of-scope queries return "sorry this content is not related to this book"
6. Confirm that primary_source is properly selected and formatted for clickable display

## Troubleshooting

| Error | Solution |
|-------|----------|
| `GROQ_API_KEY not set` | Add GROQ_API_KEY to `.env` file |
| `Connection refused` | Check API keys and network connectivity |
| `401 Unauthorized` | Verify API keys are valid |
| `No results returned` | Ensure Qdrant collection has data |
| `Rate limit exceeded` | Add delays between requests or upgrade API tier |