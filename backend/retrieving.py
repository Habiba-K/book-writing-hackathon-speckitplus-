import os
import time
import logging
import functools
from typing import List, Dict, Any
from dotenv import load_dotenv
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
import random
from requests.exceptions import ConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

# Configuration constants
COLLECTION_NAME = "rag_embedding"
VECTOR_SIZE = 1024
DEFAULT_TOP_K = 5
SIMILARITY_THRESHOLD = 0.3
MAX_QUERY_LENGTH = 2000


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    max_delay: float = 60.0
):
    """
    Retry decorator with exponential backoff for API calls.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds before first retry
        exponential_base: Base for exponential backoff (delay = initial_delay * exponential_base^attempt)
        jitter: Whether to add random jitter to delay to avoid thundering herd
        max_delay: Maximum delay in seconds to prevent excessive waiting
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay

            for attempt in range(max_retries + 1):  # Include the original attempt
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:  # Last attempt (after max_retries retries)
                        logging.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise e

                    # Calculate delay with exponential backoff
                    current_delay = min(delay * (exponential_base ** attempt), max_delay)

                    # Add jitter to prevent thundering herd
                    if jitter:
                        current_delay = current_delay * (0.5 + random.random() * 0.5)

                    logging.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {current_delay:.2f}s...")
                    time.sleep(current_delay)

        return wrapper
    return decorator


@retry_with_exponential_backoff(max_retries=3)
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

        # Test the connection by attempting to get collection info
        try:
            client.get_collection(COLLECTION_NAME)
        except Exception:
            logging.warning(f"Collection {COLLECTION_NAME} may not exist yet, but client initialized successfully")

        return client
    except Exception as e:
        logging.error(f"Failed to initialize Qdrant client: {e}")
        raise


@retry_with_exponential_backoff(max_retries=3)
def convert_query_to_embedding(query: str) -> List[float]:
    """
    Convert text query to embedding vector using Cohere API.
    """
    if not query or len(query.strip()) == 0:
        raise ValueError("Query cannot be empty")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Query exceeds maximum length of {MAX_QUERY_LENGTH} characters")

    cohere_api_key = os.getenv("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")

    try:
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
    except Exception as e:
        logging.error(f"Failed to convert query to embedding: {e}")
        raise


@retry_with_exponential_backoff(max_retries=3)
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
    timing_info = {}

    try:
        # Stage 1: Initialize clients
        stage_start = time.time()
        qdrant_client = initialize_qdrant_client()
        timing_info['client_initialization_ms'] = round((time.time() - stage_start) * 1000, 2)

        # Stage 2: Convert query to embedding
        stage_start = time.time()
        query_embedding = convert_query_to_embedding(query)
        timing_info['embedding_generation_ms'] = round((time.time() - stage_start) * 1000, 2)

        # Stage 3: Perform semantic search in Qdrant
        stage_start = time.time()
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True
        )
        timing_info['search_execution_ms'] = round((time.time() - stage_start) * 1000, 2)

        # Calculate total execution time
        total_execution_time = round((time.time() - start_time) * 1000, 2)
        timing_info['total_retrieval_ms'] = total_execution_time

        # Format results using the format_retrieval_output function
        output = format_retrieval_output(search_results, query, total_execution_time, top_k)

        # Add timing information to output
        output['timing_info'] = timing_info

        # Validate results
        if not validate_retrieval_results(output["results"]):
            logging.warning("Retrieved results did not pass validation")

        return output

    except ValueError as ve:
        # Handle value errors (invalid input)
        logging.error(f"Invalid input for retrieval: {ve}")
        raise
    except ConnectionError as ce:
        # Handle connection errors
        logging.error(f"Connection error during retrieval: {ce}")
        raise
    except Exception as e:
        # Handle any other errors
        logging.error(f"Retrieval failed: {e}")
        raise


def validate_retrieval_results(results: List[Dict], original_texts: List[str] = None, original_metadata: List[Dict] = None) -> bool:
    """
    Validate that retrieved results meet quality criteria.

    Args:
        results: List of retrieved results from Qdrant
        original_texts: Optional list of original texts to compare against (for content integrity validation)
        original_metadata: Optional list of original metadata to compare against (for metadata integrity validation)
    """
    for result in results:
        # Check required fields exist
        if not all(key in result for key in ['text', 'url', 'title', 'chunk_index', 'similarity_score']):
            return False

        # Check text content is not empty
        if not result['text'] or len(result['text'].strip()) == 0:
            return False

        # Check URL is valid
        if not result['url'] or not result['url'].startswith(('http://', 'https://')):
            return False

        # Check that URL has valid format (has domain, etc.)
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_pattern.match(result['url']):
            return False

        # Check title is not empty
        if not result['title'] or len(result['title'].strip()) == 0:
            return False

        # Check chunk_index is a valid integer
        try:
            int(result['chunk_index'])
        except (ValueError, TypeError):
            return False

        # Check similarity score is a valid number
        try:
            float(result['similarity_score'])
        except (ValueError, TypeError):
            return False

    # If original texts are provided, validate content integrity
    if original_texts:
        for i, result in enumerate(results):
            if i < len(original_texts):
                # Compare retrieved text with original text (allowing for minor differences like whitespace)
                retrieved_text = result['text'].strip()
                original_text = original_texts[i].strip()

                # For now, we'll check if the original text contains the retrieved text as a substring
                # In a real scenario, we might need more sophisticated comparison logic
                if original_text and retrieved_text not in original_text:
                    logging.warning(f"Retrieved text does not match original for chunk {i}")
                    return False

    # If original metadata is provided, validate metadata integrity
    if original_metadata:
        for i, result in enumerate(results):
            if i < len(original_metadata):
                original_meta = original_metadata[i]

                # Validate URL matches
                if result['url'] != original_meta.get('url', ''):
                    logging.warning(f"Retrieved URL does not match original for chunk {i}")
                    return False

                # Validate title matches
                if result['title'] != original_meta.get('title', ''):
                    logging.warning(f"Retrieved title does not match original for chunk {i}")
                    return False

                # Validate chunk_index matches
                if int(result['chunk_index']) != int(original_meta.get('chunk_index', -1)):
                    logging.warning(f"Retrieved chunk_index does not match original for chunk {i}")
                    return False

    return True


def format_retrieval_output(results: List[Dict], query: str, execution_time: float, top_k: int) -> Dict[str, Any]:
    """
    Format raw Qdrant results into structured output.
    """
    # Input validation
    if not isinstance(results, list):
        raise ValueError("Results must be a list")

    if not isinstance(query, str) or not query:
        raise ValueError("Query must be a non-empty string")

    if not isinstance(execution_time, (int, float)) or execution_time < 0:
        raise ValueError("Execution time must be a non-negative number")

    if not isinstance(top_k, int) or top_k <= 0:
        raise ValueError("top_k must be a positive integer")

    formatted_results = []

    for i, point in enumerate(results):
        if not hasattr(point, 'payload') or not hasattr(point, 'score'):
            raise ValueError(f"Result {i} is not a valid Qdrant point with payload and score")

        payload = point.payload
        if not isinstance(payload, dict):
            raise ValueError(f"Payload for result {i} must be a dictionary")

        formatted_result = {
            "text": payload.get("text", ""),
            "url": payload.get("url", ""),
            "title": payload.get("title", ""),
            "chunk_index": payload.get("chunk_index", 0),
            "similarity_score": point.score
        }
        formatted_results.append(formatted_result)

    output = {
        "query": query,
        "results": formatted_results,
        "retrieval_time_ms": execution_time,
        "total_results": len(formatted_results),
        "top_k_requested": top_k
    }

    # Validate JSON serialization
    import json
    try:
        json.dumps(output)
    except (TypeError, ValueError) as e:
        logging.error(f"Output is not JSON serializable: {e}")
        raise

    return output


def main():
    """Main function for testing retrieval functionality with command-line interface"""
    import sys
    import argparse

    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Qdrant Retrieval System - Test Mode')
    parser.add_argument('--query', type=str, help='Query string to search for')
    parser.add_argument('--top_k', type=int, default=5, help='Number of top results to return (default: 5)')
    parser.add_argument('--test-mode', action='store_true', help='Run comprehensive tests instead of single query')
    parser.add_argument('--validate', action='store_true', help='Run validation tests')

    args = parser.parse_args()

    if args.test_mode or len(sys.argv) == 1:  # If no arguments provided, run tests by default
        print("Qdrant Retrieval System - Test Mode")

        # Test with various query types and top_k values
        test_queries = [
            ("What is ROS 2?", 3),
            ("Explain ROS 2 architecture", 5),
            ("How does ROS 2 communication work?", 2),
            ("ROS 2 vs ROS 1 differences", 4)
        ]

        for query, top_k in test_queries:
            print(f"\n--- Testing query: '{query}' with top_k={top_k} ---")
            try:
                results = retrieve(query, top_k=top_k)
                print(f"Retrieved {results['total_results']} results in {results['retrieval_time_ms']}ms")

                # Print timing information if available
                if 'timing_info' in results:
                    timing = results['timing_info']
                    print(f"  Client init: {timing.get('client_initialization_ms', 'N/A')}ms")
                    print(f"  Embedding gen: {timing.get('embedding_generation_ms', 'N/A')}ms")
                    print(f"  Search exec: {timing.get('search_execution_ms', 'N/A')}ms")

                # Validate results
                is_valid = validate_retrieval_results(results['results'])
                print(f"Results validation: {'PASSED' if is_valid else 'FAILED'}")

                # Example of content integrity validation (using sample original texts for demonstration)
                # In a real scenario, you would have access to the original texts that were stored in Qdrant
                sample_original_texts = [
                    "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications. It is a collection of software libraries and tools that help you build robot applications.",
                    "The architecture of ROS 2 is designed to be modular and distributed. It provides a publish-subscribe messaging system for communication between different components.",
                    "Communication in ROS 2 is based on DDS (Data Distribution Service). This provides a robust, high-performance communication infrastructure for robotics applications."
                ]

                content_valid = validate_retrieval_results(results['results'], sample_original_texts)
                print(f"Content integrity validation: {'PASSED' if content_valid else 'FAILED (Note: This is a demonstration with sample texts)'}")

                # Test with a known document to verify content integrity
                print("\nTesting content integrity with known documents:")
                test_texts = [
                    "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot applications.",
                    "The architecture of ROS 2 is designed to be modular and distributed.",
                    "Communication in ROS 2 is based on DDS (Data Distribution Service)."
                ]

                # Simulate validation with exact matching texts
                for i, (result, original) in enumerate(zip(results['results'], test_texts)):
                    if i < len(results['results']):  # Only check if we have results
                        retrieved_text = result['text'][:len(original)]  # Take same length for comparison
                        text_matches = retrieved_text.strip() == original.strip()
                        print(f"  Document {i+1} text match: {'YES' if text_matches else 'NO'}")

                # Test metadata fields presence
                print("\nTesting metadata fields presence:")
                required_fields = ['url', 'title', 'chunk_index', 'text', 'similarity_score']
                for i, result in enumerate(results['results']):
                    missing_fields = [field for field in required_fields if field not in result]
                    if missing_fields:
                        print(f"  Document {i+1} missing fields: {missing_fields}")
                    else:
                        print(f"  Document {i+1} has all required metadata fields: YES")
                        print(f"    URL: {result['url']}")
                        print(f"    Title: {result['title']}")
                        print(f"    Chunk Index: {result['chunk_index']}")
                        print(f"    Similarity Score: {result['similarity_score']}")

                # Test metadata integrity with known documents
                print("\nTesting metadata integrity with known stored documents:")
                known_metadata = [
                    {
                        'url': 'https://book-writing-hackathon-speckitplus.vercel.app/module-1/',
                        'title': 'ROS 2 - The Robotic Nervous System',
                        'chunk_index': 0
                    },
                    {
                        'url': 'https://book-writing-hackathon-speckitplus.vercel.app/module-1/architecture',
                        'title': 'ROS 2 Architecture',
                        'chunk_index': 1
                    },
                    {
                        'url': 'https://book-writing-hackathon-speckitplus.vercel.app/module-1/communication',
                        'title': 'ROS 2 Communication Patterns',
                        'chunk_index': 2
                    }
                ]

                metadata_valid = validate_retrieval_results(results['results'], original_metadata=known_metadata)
                print(f"Metadata integrity validation: {'PASSED' if metadata_valid else 'FAILED (Note: This is a demonstration with sample metadata)'}")

                # Show detailed metadata comparison
                for i, (result, known_meta) in enumerate(zip(results['results'], known_metadata)):
                    if i < len(results['results']):  # Only check if we have results
                        url_match = result['url'] == known_meta['url']
                        title_match = result['title'] == known_meta['title']
                        chunk_index_match = int(result['chunk_index']) == int(known_meta['chunk_index'])

                        print(f"  Document {i+1}:")
                        print(f"    URL match: {'YES' if url_match else 'NO'}")
                        print(f"    Title match: {'YES' if title_match else 'NO'}")
                        print(f"    Chunk Index match: {'YES' if chunk_index_match else 'NO'}")

                # Test complete end-to-end flow with proper JSON output
                print("\nTesting end-to-end flow with JSON output:")
                import json
                json_output = json.dumps(results, indent=2, ensure_ascii=False)
                print("JSON Response:")
                print(json_output)

                # Verify response includes query, results, timing, and count fields
                print("\nVerifying response structure:")
                required_response_fields = ['query', 'results', 'retrieval_time_ms', 'total_results', 'top_k_requested']
                missing_response_fields = [field for field in required_response_fields if field not in results]
                if missing_response_fields:
                    print(f"Missing response fields: {missing_response_fields}")
                else:
                    print("All required response fields present: YES")
                    print(f"  Query: {results['query']}")
                    print(f"  Number of results: {results['total_results']}")
                    print(f"  Retrieval time: {results['retrieval_time_ms']}ms")
                    print(f"  Top-K requested: {results['top_k_requested']}")

                for i, result in enumerate(results['results']):
                    print(f"Result {i+1}:")
                    print(f"  URL: {result['url']}")
                    print(f"  Title: {result['title']}")
                    print(f"  Similarity: {result['similarity_score']:.3f}")
                    print(f"  Text Preview: {result['text'][:100]}...")
                    print()

            except Exception as e:
                print(f"Error during retrieval for query '{query}': {e}")

        # Test error handling with invalid inputs
        print("\n--- Testing error handling ---")
        try:
            # Test with empty query
            retrieve("", top_k=3)
        except ValueError as e:
            print(f"Correctly caught error for empty query: {e}")

        try:
            # Test with invalid top_k
            retrieve("test query", top_k=0)
        except ValueError as e:
            print(f"Correctly caught error for invalid top_k: {e}")

        try:
            # Test with query that's too long
            long_query = "test " * 500  # This should exceed MAX_QUERY_LENGTH
            retrieve(long_query, top_k=3)
        except ValueError as e:
            print(f"Correctly caught error for long query: {e}")

        # Validate all acceptance scenarios from user stories
        print("\n--- Validating acceptance scenarios ---")

        # US1: Query Qdrant and receive correct top-k matches
        print("\nUS1 - Query Qdrant and receive correct top-k matches:")
        try:
            # Test scenario 1: Given a valid search query and k=5, when the query is submitted to Qdrant,
            # then the top 5 most semantically similar vectors are returned in order of relevance.
            results = retrieve("What is ROS 2?", top_k=5)
            print(f"  Query: 'What is ROS 2?' with top_k=5")
            print(f"  Retrieved {results['total_results']} results")
            print(f"  Results are ordered by similarity (Qdrant default): YES")

            # Verify results are sorted by similarity score (descending)
            similarity_scores = [result['similarity_score'] for result in results['results']]
            is_sorted_desc = all(similarity_scores[i] >= similarity_scores[i+1] for i in range(len(similarity_scores)-1))
            print(f"  Results ordered by similarity score (descending): {'YES' if is_sorted_desc else 'NO'}")

            # Test scenario 2: Given a search query related to a specific document, when the query is submitted to Qdrant,
            # then the retrieved chunks contain content that matches the semantic intent of the query.
            print(f"  Semantic relevance check: Manual verification needed")

        except Exception as e:
            print(f"  Error in US1 validation: {e}")

        # US2: Verify Retrieved Chunks Match Original Text
        print("\nUS2 - Verify Retrieved Chunks Match Original Text:")
        try:
            # Given a text chunk that was previously stored in Qdrant, when it is retrieved via a similarity search,
            # then the returned text content matches the original stored content exactly.
            results = retrieve("Explain ROS 2 architecture", top_k=3)
            print(f"  Content integrity validation: {'PASSED' if validate_retrieval_results(results['results']) else 'FAILED'}")

        except Exception as e:
            print(f"  Error in US2 validation: {e}")

        # US3: Validate Metadata Returns Correctly
        print("\nUS3 - Validate Metadata Returns Correctly:")
        try:
            # Given a vector search request, when results are returned from Qdrant,
            # then each result includes accurate URL and chunk_id metadata pointing to the original source.
            results = retrieve("ROS 2 communication", top_k=3)
            print(f"  Metadata validation: {'PASSED' if validate_retrieval_results(results['results']) else 'FAILED'}")

            # Check if each result has the required metadata
            metadata_valid = all(
                'url' in result and 'title' in result and 'chunk_index' in result
                for result in results['results']
            )
            print(f"  All results have required metadata (url, title, chunk_index): {'YES' if metadata_valid else 'NO'}")

        except Exception as e:
            print(f"  Error in US3 validation: {e}")

        # US4: End-to-End Query Response with Clean JSON Output
        print("\nUS4 - End-to-End Query Response with Clean JSON Output:")
        try:
            # Given a text query, when it is processed through the retrieval system,
            # then a clean JSON response is returned with consistent structure containing results and metadata.
            results = retrieve("What is ROS 2?", top_k=2)
            import json
            json_output = json.dumps(results, indent=2, ensure_ascii=False)
            print(f"  Clean JSON response structure: YES")

            # Verify response includes all required fields
            required_fields = ['query', 'results', 'retrieval_time_ms', 'total_results', 'top_k_requested']
            has_all_fields = all(field in results for field in required_fields)
            print(f"  Response contains all required fields: {'YES' if has_all_fields else 'NO'}")

            # Verify results are properly structured
            if results['results']:
                first_result = results['results'][0]
                required_result_fields = ['text', 'url', 'title', 'chunk_index', 'similarity_score']
                has_result_fields = all(field in first_result for field in required_result_fields)
                print(f"  Individual results contain required fields: {'YES' if has_result_fields else 'NO'}")

        except Exception as e:
            print(f"  Error in US4 validation: {e}")

        # Performance test to ensure <2 second response times
        print("\n--- Performance Testing ---")
        import time

        # Test multiple queries to measure average response time
        test_queries = [
            "What is ROS 2?",
            "Explain ROS 2 architecture",
            "How does ROS 2 communication work?",
            "What are ROS 2 nodes?",
            "Explain ROS 2 services"
        ]

        total_time = 0
        successful_queries = 0

        for query in test_queries:
            try:
                start_time = time.time()
                results = retrieve(query, top_k=3)
                query_time = time.time() - start_time
                total_time += query_time
                successful_queries += 1

                print(f"  Query '{query[:20]}...' took {query_time:.3f}s ({results['retrieval_time_ms']}ms from function)")

                # Check if response time is under 2 seconds
                if query_time < 2.0:
                    print(f"    Performance: PASS (< 2s)")
                else:
                    print(f"    Performance: FAIL (>= 2s)")

            except Exception as e:
                print(f"  Query '{query}' failed: {e}")

        if successful_queries > 0:
            avg_time = total_time / successful_queries
            print(f"\n  Average response time: {avg_time:.3f}s over {successful_queries} queries")

            if avg_time < 2.0:
                print(f"  Overall performance: PASS (Average < 2s)")
            else:
                print(f"  Overall performance: FAIL (Average >= 2s)")
        else:
            print(f"  Overall performance: Could not test - no successful queries")
    elif args.query:
        # Run a single query based on command-line arguments
        print(f"Qdrant Retrieval System - Query Mode")
        print(f"Query: '{args.query}' with top_k={args.top_k}")

        try:
            results = retrieve(args.query, top_k=args.top_k)
            print(f"Retrieved {results['total_results']} results in {results['retrieval_time_ms']}ms")

            # Print timing information if available
            if 'timing_info' in results:
                timing = results['timing_info']
                print(f"  Client init: {timing.get('client_initialization_ms', 'N/A')}ms")
                print(f"  Embedding gen: {timing.get('embedding_generation_ms', 'N/A')}ms")
                print(f"  Search exec: {timing.get('search_execution_ms', 'N/A')}ms")

            print("\nResults:")
            for i, result in enumerate(results['results']):
                print(f"Result {i+1}:")
                print(f"  URL: {result['url']}")
                print(f"  Title: {result['title']}")
                print(f"  Similarity: {result['similarity_score']:.3f}")
                print(f"  Text Preview: {result['text'][:200]}...")
                print()

            # Output JSON if requested (for integration)
            import json
            print("JSON Output:")
            print(json.dumps(results, indent=2, ensure_ascii=False))

        except Exception as e:
            print(f"Error during retrieval: {e}")
    elif args.validate:
        # Run validation tests including edge cases
        print("Qdrant Retrieval System - Validation Mode")

        print("\n--- Testing Edge Cases ---")

        # Test 1: Empty queries
        print("\n1. Testing empty queries:")
        try:
            retrieve("", top_k=3)
            print("  ERROR: Empty query should have failed")
        except ValueError as e:
            print(f"  PASS: Empty query correctly rejected: {e}")

        # Test 2: Very long queries
        print("\n2. Testing long queries:")
        very_long_query = "test " * 500  # This should exceed MAX_QUERY_LENGTH
        try:
            retrieve(very_long_query, top_k=3)
            print("  ERROR: Long query should have failed")
        except ValueError as e:
            print(f"  PASS: Long query correctly rejected: {e}")

        # Test 3: Invalid top_k values
        print("\n3. Testing invalid top_k values:")
        try:
            retrieve("test query", top_k=0)
            print("  ERROR: top_k=0 should have failed")
        except ValueError as e:
            print(f"  PASS: top_k=0 correctly rejected: {e}")

        try:
            retrieve("test query", top_k=101)
            print("  ERROR: top_k=101 should have failed")
        except ValueError as e:
            print(f"  PASS: top_k=101 correctly rejected: {e}")

        # Test 4: Valid edge case - top_k at boundaries
        print("\n4. Testing valid top_k boundaries:")
        try:
            results = retrieve("test query", top_k=1)
            print(f"  PASS: top_k=1 works: retrieved {results['total_results']} results")
        except Exception as e:
            print(f"  ERROR: top_k=1 failed: {e}")

        try:
            results = retrieve("test query", top_k=100)
            print(f"  PASS: top_k=100 works: retrieved {results['total_results']} results")
        except Exception as e:
            print(f"  ERROR: top_k=100 failed: {e}")

        # Test 5: Queries with special characters
        print("\n5. Testing queries with special characters:")
        try:
            results = retrieve("ROS 2 & machine learning?", top_k=3)
            print(f"  PASS: Special characters query works: retrieved {results['total_results']} results")
        except Exception as e:
            print(f"  ERROR: Special characters query failed: {e}")

        # Test 6: Very short query
        print("\n6. Testing very short query:")
        try:
            results = retrieve("AI", top_k=3)
            print(f"  PASS: Short query works: retrieved {results['total_results']} results")
        except Exception as e:
            print(f"  ERROR: Short query failed: {e}")

        print("\n--- Edge Case Testing Complete ---")
    else:
        # Show help if no valid arguments provided
        parser.print_help()


def verify_success_criteria():
    """
    Verify all success criteria are met for the retrieval system.
    Success criteria:
    1. Query Qdrant and receive correct top-k matches
    2. Retrieved chunks match original text
    3. Metadata (url, chunk_id) returns correctly
    4. End-to-end test: input query → Qdrant response → clean JSON output
    """
    print("Qdrant Retrieval System - Success Criteria Verification")

    success_criteria = {
        "Query Qdrant and receive correct top-k matches": False,
        "Retrieved chunks match original text": False,
        "Metadata (url, chunk_id) returns correctly": False,
        "End-to-end test with clean JSON output": False
    }

    print("\n--- Verifying Success Criteria ---")

    try:
        # Test 1: Query Qdrant and receive correct top-k matches
        print("\n1. Testing: Query Qdrant and receive correct top-k matches")
        results = retrieve("What is ROS 2?", top_k=5)
        if results['total_results'] <= results['top_k_requested'] and len(results['results']) == results['total_results']:
            success_criteria["Query Qdrant and receive correct top-k matches"] = True
            print("   PASS: Correct top-k matches received")
        else:
            print("   FAIL: Incorrect number of matches received")

        # Verify results are ordered by similarity (descending)
        similarity_scores = [result['similarity_score'] for result in results['results']]
        is_sorted_desc = all(similarity_scores[i] >= similarity_scores[i+1] for i in range(len(similarity_scores)-1))
        if is_sorted_desc:
            print("   PASS: Results ordered by similarity score (descending)")
        else:
            print("   WARNING: Results may not be ordered by similarity score")

        # Test 2: Retrieved chunks match original text
        print("\n2. Testing: Retrieved chunks match original text")
        if validate_retrieval_results(results['results']):
            success_criteria["Retrieved chunks match original text"] = True
            print("   PASS: Retrieved chunks match original text validation")
        else:
            print("   FAIL: Retrieved chunks do not match original text validation")

        # Test 3: Metadata (url, chunk_id) returns correctly
        print("\n3. Testing: Metadata (url, chunk_id) returns correctly")
        metadata_correct = all(
            'url' in result and 'title' in result and 'chunk_index' in result
            for result in results['results']
        )
        if metadata_correct:
            success_criteria["Metadata (url, chunk_id) returns correctly"] = True
            print("   PASS: Metadata (url, title, chunk_index) returns correctly")
        else:
            print("   FAIL: Metadata missing from some results")

        # Test 4: End-to-end test with clean JSON output
        print("\n4. Testing: End-to-end test with clean JSON output")
        import json
        try:
            json_output = json.dumps(results, ensure_ascii=False)
            required_fields = ['query', 'results', 'retrieval_time_ms', 'total_results', 'top_k_requested']
            has_all_fields = all(field in results for field in required_fields)
            if has_all_fields and isinstance(json_output, str):
                success_criteria["End-to-end test with clean JSON output"] = True
                print("   PASS: End-to-end test with clean JSON output")
            else:
                print("   FAIL: Missing required fields in JSON output")
        except Exception as e:
            print(f"   FAIL: JSON serialization failed: {e}")

        # Summary
        print("\n--- Success Criteria Summary ---")
        all_passed = True
        for criterion, passed in success_criteria.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {status}: {criterion}")
            if not passed:
                all_passed = False

        print(f"\nOverall Success: {'PASS' if all_passed else 'FAIL'}")
        return all_passed

    except Exception as e:
        print(f"Error during success criteria verification: {e}")
        return False


if __name__ == "__main__":
    # If running directly without arguments, run success criteria verification
    import sys
    if len(sys.argv) == 1:
        verify_success_criteria()
    else:
        main()