# book-writing-hackathon-speckitplus- Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-17

## Active Technologies
- Python 3.10+ + qdrant-client, cohere, python-dotenv, requests, beautifulsoup4 (005-qdrant-retrieval-test)
- Qdrant vector database (external cloud service) (005-qdrant-retrieval-test)
- Python 3.10+ + groq, python-dotenv (001-rag-agent)
- Groq API integration (001-rag-agent)
- Python 3.10+ + fastapi, uvicorn (006-frontend-rag-integration)
- FastAPI web framework integration (006-frontend-rag-integration)
- TypeScript + React + Docusaurus (006-frontend-rag-integration)
- Frontend chat interface component (006-frontend-rag-integration)
- Python 3.10+ + FastAPI, OpenAI Agents SDK, Cohere, Qdrant-client, python-dotenv (001-rag-agent)

- Python 3.10+ + cohere, qdrant-client, requests, beautifulsoup4, python-dotenv (001-embedding-pipeline)

## Project Structure

```text
backend/
├── retrieving.py
├── agent.py
├── main.py
├── requirements.txt
└── .env
book-site/
├── src/
│   └── components/
│       └── ChatInterface/
│           ├── ChatButton.tsx
│           ├── ChatWindow.tsx
│           ├── ChatMessages.tsx
│           ├── index.tsx
│           └── ChatInterface.css
├── package.json
└── docusaurus.config.ts
src/
tests/
```

## Commands

cd backend; python agent.py
cd backend; uvicorn main:app --reload --port 8000
cd book-site; npm run start
cd src; pytest; ruff check .

## Code Style

Python 3.10+: Follow standard conventions

## Recent Changes
- 001-rag-agent: Added Python 3.10+ + FastAPI, OpenAI Agents SDK, Cohere, Qdrant-client, python-dotenv
- 001-rag-agent: Updated to use Python 3.10+ + groq instead of openai for LLM inference
- 006-frontend-rag-integration: Added Python 3.10+ + fastapi, uvicorn, TypeScript + React + Docusaurus integration with chat interface

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
