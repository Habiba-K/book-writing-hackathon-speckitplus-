import os
import hashlib
import time
import logging
import argparse
from typing import List, Dict, Any
from dotenv import load_dotenv
import requests
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Configuration constants
SITEMAP_URL = "https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml"
COLLECTION_NAME = "rag_embedding"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
COHERE_MODEL = "embed-english-v3.0"
VECTOR_SIZE = 1024

def load_environment_variables():
    """Load and validate environment variables"""
    cohere_api_key = os.getenv("COHERE_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is required")
    if not qdrant_url:
        raise ValueError("QDRANT_URL environment variable is required")
    if not qdrant_api_key:
        raise ValueError("QDRANT_API_KEY environment variable is required")

    return cohere_api_key, qdrant_url, qdrant_api_key


def initialize_cohere_client():
    """Initialize Cohere client with error handling"""
    try:
        cohere_api_key, _, _ = load_environment_variables()
        co = cohere.Client(cohere_api_key)
        return co
    except Exception as e:
        logging.error(f"Failed to initialize Cohere client: {e}")
        raise


def initialize_qdrant_client():
    """Initialize Qdrant client with error handling"""
    try:
        _, qdrant_url, qdrant_api_key = load_environment_variables()
        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        return client
    except Exception as e:
        logging.error(f"Failed to initialize Qdrant client: {e}")
        raise


def generate_chunk_id(url: str, chunk_index: int) -> str:
    """Generate deterministic ID for upsert capability."""
    content = f"{url}:{chunk_index}"
    return hashlib.md5(content.encode()).hexdigest()


def retry_with_exponential_backoff(func, max_retries=3, base_delay=1):
    """Create retry mechanism with exponential backoff for API calls"""
    def wrapper(*args, **kwargs):
        delay = base_delay
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
        return None
    return wrapper


def setup_logging():
    """Add logging configuration for pipeline progress tracking"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pipeline.log'),
            logging.StreamHandler()
        ]
    )


def get_all_urls(sitemap_url: str) -> List[str]:
    """
    Parse sitemap.xml and extract all page URLs.

    Args:
        sitemap_url: Full URL to sitemap.xml
                     e.g., "https://book-writing-hackathon-speckitplus.vercel.app/sitemap.xml"

    Returns:
        List of page URLs found in sitemap

    Raises:
        requests.RequestException: If sitemap cannot be fetched
    """
    response = requests.get(sitemap_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'xml')
    urls = []

    # Look for both <url><loc> and <sitemap><loc> elements
    for loc in soup.find_all('loc'):
        url = loc.text.strip()
        # Only include URLs that are part of the main site, not sub-sitemaps
        if url and not url.endswith('.xml') and 'book-writing-hackathon-speckitplus.vercel.app' in url:
            urls.append(url)

    return urls


def extract_text_from_url(url: str) -> Dict[str, Any]:
    """
    Fetch page and extract clean text content.

    Args:
        url: Full URL of the page to extract

    Returns:
        Dictionary with keys:
        - "url": str - the source URL
        - "title": str - page title (from <title> or <h1>)
        - "text": str - cleaned text content

    Raises:
        requests.RequestException: If page cannot be fetched
    """
    response = retry_with_exponential_backoff(requests.get)(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove navigation, footer, and other non-content elements
    for element in soup.find_all(['nav', 'footer', 'aside', 'header']):
        element.decompose()

    # Remove sidebar elements (common in Docusaurus)
    for element in soup.find_all(class_=lambda x: x and ('sidebar' in x or 'navbar' in x or 'menu' in x)):
        element.decompose()

    # Find the main content - prioritize Docusaurus-specific selectors
    content = None
    for selector in ['article', 'main', '.main-wrapper', '.theme-doc-markdown', '.markdown']:
        content = soup.select_one(selector)
        if content:
            break

    # If no specific content found, use the body
    if not content:
        content = soup.find('body')

    if content:
        # Extract title
        title = ""
        title_elem = soup.find('title')
        if title_elem:
            title = title_elem.get_text().strip()
        else:
            h1_elem = soup.find('h1')
            if h1_elem:
                title = h1_elem.get_text().strip()

        # Get clean text content
        text = content.get_text(separator=' ', strip=True)

        # Clean up extra whitespace
        import re
        text = re.sub(r'\s+', ' ', text)

        return {
            "url": url,
            "title": title,
            "text": text
        }
    else:
        return {
            "url": url,
            "title": "No title found",
            "text": ""
        }


def normalize_url(url: str) -> str:
    """Implement URL normalization to handle duplicates"""
    from urllib.parse import urlparse, urlunparse

    parsed = urlparse(url)
    # Remove fragments and normalize
    normalized = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        parsed.query,  # Keep query params that might be meaningful
        ''  # Remove fragments
    ))

    # Remove trailing slash if present (except for root)
    if normalized.endswith('/') and normalized != f"{parsed.scheme}://{parsed.netloc}/":
        normalized = normalized[:-1]

    return normalized


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks for embedding.

    Args:
        text: Full text content to chunk
        chunk_size: Maximum characters per chunk (default: 1000)
        overlap: Characters to overlap between chunks (default: 200)

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        # If this isn't the last chunk, try to break at sentence or paragraph boundary
        if end < len(text):
            # Look for sentence endings near the end of the chunk
            for i in range(len(chunk) - 1, len(chunk) - overlap - 1, -1):
                if chunk[i] in '.!?':
                    chunk = chunk[:i+1]
                    end = start + i + 1
                    break

        chunks.append(chunk)

        # Move start position forward by chunk_size minus overlap
        start = end - overlap if end > start else start + chunk_size

        # If we're near the end, just take the remainder
        if start >= len(text):
            break

    return chunks


def embed(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for text chunks using Cohere.

    Args:
        texts: List of text strings to embed

    Returns:
        List of embedding vectors (each 1024 dimensions)

    Raises:
        cohere.CohereError: If API call fails

    Environment:
        Requires COHERE_API_KEY
    """
    co = initialize_cohere_client()

    # Use the embed-english-v3.0 model as specified
    response = co.embed(
        texts=texts,
        model=COHERE_MODEL,
        input_type="search_document"  # Using search_document for indexing
    )

    # Validate that embeddings have correct dimensions
    embeddings = response.embeddings
    for embedding in embeddings:
        if len(embedding) != VECTOR_SIZE:
            raise ValueError(f"Embedding has {len(embedding)} dimensions, expected {VECTOR_SIZE}")

    return embeddings


def create_collection(collection_name: str = "rag_embedding") -> None:
    """
    Create Qdrant collection if it doesn't exist.

    Args:
        collection_name: Name of the collection (default: "rag_embedding")

    Environment:
        Requires QDRANT_URL and QDRANT_API_KEY

    Notes:
        - Vector size: 1024 (Cohere embed-english-v3.0)
        - Distance: Cosine
        - Idempotent: Safe to call multiple times
    """
    client = initialize_qdrant_client()

    try:
        # Check if collection exists
        client.get_collection(collection_name)
        logging.info(f"Collection '{collection_name}' already exists")
    except:
        # Create collection with 1024-dimension vectors and cosine distance
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=VECTOR_SIZE,
                distance=models.Distance.COSINE
            )
        )
        logging.info(f"Created collection '{collection_name}' with {VECTOR_SIZE}-dimension vectors")


def save_chunk_to_qdrant(
    chunks: List[str],
    embeddings: List[List[float]],
    url: str,
    title: str,
    collection_name: str = "rag_embedding"
) -> None:
    """
    Upsert chunks with embeddings to Qdrant.

    Args:
        chunks: List of text chunks
        embeddings: Corresponding embedding vectors
        url: Source URL for metadata
        title: Source page title for metadata
        collection_name: Target collection (default: "rag_embedding")

    Notes:
        - Uses deterministic IDs for upsert behavior
        - Stores text, url, title, chunk_index in payload
    """
    client = initialize_qdrant_client()

    # Prepare points for upsert
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_id = generate_chunk_id(url, i)

        point = models.PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={
                "text": chunk,
                "url": url,
                "title": title,
                "chunk_index": i
            }
        )
        points.append(point)

    # Upsert points to Qdrant
    client.upsert(
        collection_name=collection_name,
        points=points
    )

    logging.info(f"Saved {len(chunks)} chunks from {url} to Qdrant collection '{collection_name}'")


def validate_parameters(sitemap_url: str, chunk_size: int, chunk_overlap: int) -> None:
    """Add input validation for all function parameters"""
    if not sitemap_url or not sitemap_url.startswith(('http://', 'https://')):
        raise ValueError(f"Invalid sitemap URL: {sitemap_url}")

    if chunk_size <= 0:
        raise ValueError(f"Chunk size must be positive, got: {chunk_size}")

    if chunk_overlap < 0:
        raise ValueError(f"Chunk overlap cannot be negative, got: {chunk_overlap}")

    if chunk_overlap >= chunk_size:
        raise ValueError(f"Chunk overlap ({chunk_overlap}) must be less than chunk size ({chunk_size})")


def main():
    """Execute the complete embedding pipeline."""
    parser = argparse.ArgumentParser(description='Embedding Pipeline: Extract text from Docusaurus sites, generate embeddings, and store in Qdrant')
    parser.add_argument('--sitemap-url', default=SITEMAP_URL, help='Sitemap URL to process (default: %(default)s)')
    parser.add_argument('--collection-name', default=COLLECTION_NAME, help='Qdrant collection name (default: %(default)s)')
    parser.add_argument('--chunk-size', type=int, default=CHUNK_SIZE, help='Text chunk size (default: %(default)s)')
    parser.add_argument('--chunk-overlap', type=int, default=CHUNK_OVERLAP, help='Overlap between chunks (default: %(default)s)')

    args = parser.parse_args()

    # Validate parameters
    validate_parameters(args.sitemap_url, args.chunk_size, args.chunk_overlap)

    setup_logging()
    logging.info("Starting embedding pipeline...")
    start_time = time.time()

    try:
        # Load environment variables
        load_environment_variables()

        # Create Qdrant collection
        logging.info("Creating/verifying Qdrant collection...")
        create_collection(args.collection_name)

        # Fetch all URLs from sitemap
        logging.info(f"Fetching sitemap: {args.sitemap_url}")
        urls = get_all_urls(args.sitemap_url)
        logging.info(f"Found {len(urls)} URLs")

        # Process each URL
        total_chunks = 0
        processed_urls = 0

        for i, url in enumerate(urls):
            logging.info(f"Processing ({i+1}/{len(urls)}): {url}")

            url_start_time = time.time()

            try:
                # Extract text from URL
                doc = extract_text_from_url(url)
                logging.info(f"  - Extracted {len(doc['text'])} characters")

                # Chunk text
                chunks = chunk_text(doc['text'], args.chunk_size, args.chunk_overlap)
                logging.info(f"  - Created {len(chunks)} chunks")

                if chunks:  # Only process if there are chunks to embed
                    # Generate embeddings
                    embeddings = embed(chunks)
                    logging.info(f"  - Generated embeddings")

                    # Save to Qdrant
                    save_chunk_to_qdrant(chunks, embeddings, doc['url'], doc['title'], args.collection_name)
                    total_chunks += len(chunks)
                    processed_urls += 1

            except Exception as e:
                logging.error(f"Error processing {url}: {e}")
                continue  # Continue with next URL even if one fails

            url_duration = time.time() - url_start_time
            logging.info(f"  - Completed in {url_duration:.2f}s")

        total_duration = time.time() - start_time
        logging.info(f"Pipeline complete! Processed {processed_urls}/{len(urls)} pages and saved {total_chunks} chunks.")
        logging.info(f"Total execution time: {total_duration:.2f}s")

        # Performance goal check
        if total_duration > 300:  # 5 minutes = 300 seconds
            logging.warning(f"Performance goal exceeded: {total_duration:.2f}s > 300s (5 minutes)")
        else:
            logging.info(f"Performance goal met: {total_duration:.2f}s <= 300s (5 minutes)")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise


# Import the API app to make it available
from api import app

if __name__ == "__main__":
    main()
