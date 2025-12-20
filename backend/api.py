from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from agent import RAGAgent

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="API for the RAG (Retrieval-Augmented Generation) Agent",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class Source(BaseModel):
    url: str
    title: str
    chunk_index: int

class Chunk(BaseModel):
    text: str
    similarity_score: float
    source: Source

class QueryResponse(BaseModel):
    answer: str
    primary_source: Optional[Source] = None
    sources: List[Source]
    matched_chunks: List[Chunk]
    query_time: float
    success: bool
    is_out_of_scope: bool = False
    error: Optional[str] = None

# Initialize RAG Agent
rag_agent = RAGAgent()

@app.post("/ask", response_model=QueryResponse)
async def ask_endpoint(request: QueryRequest):
    """
    Process a user query through the RAG agent.
    """
    try:
        # Validate query length
        if not request.query or len(request.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(request.query) > 2000:  # MAX_QUERY_LENGTH
            raise HTTPException(status_code=400, detail="Query exceeds maximum length of 2000 characters")

        # Process query using existing RAG agent
        response = rag_agent.process_query(request.query)

        # Return response in expected format
        return QueryResponse(**response)

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        # Check if it's an API key error
        if "invalid_api_key" in error_msg.lower() or "incorrect api key" in error_msg.lower():
            raise HTTPException(status_code=401, detail=f"Invalid API key configuration: {error_msg}")
        elif "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            raise HTTPException(status_code=504, detail=f"Connection error to external service: {error_msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Error processing query: {error_msg}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "healthy", "service": "RAG Agent API"}