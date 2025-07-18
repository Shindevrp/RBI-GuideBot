# RBI GuideBot

A Retrieval-Augmented Generation (RAG) chatbot for NBFC professionals to query RBI guidelines and circulars. Features document ingestion, semantic search, chart generation, feedback loop, and audit mode.

## Project Structure
- `backend/`: FastAPI server, RAG pipeline, document ingestion, chart generation, models, db
- `frontend/`: React.js UI for chat and feedback
- `data/`: RBI circulars, PDFs, notifications

## Setup Instructions
1. Install Python 3.10+, Node.js, and Docker
2. Backend: `cd backend && pip install -r requirements.txt`
3. Frontend: `cd frontend && npm install`
4. Run backend: `uvicorn api.main:app --reload`
5. Run frontend: `npm start`

## Features
- Ingest RBI circulars (PDFs, URLs)
- Chunk, embed, and store in Pinecone
- RAG flow for contextual answers
- Chart generation for numeric queries
- Feedback loop and audit mode
- Search history stored in SQL database

## Technical Architecture

```
        ┌──────────────┐
        │   User       │
        │ (NBFC Staff) │
        └────┬─────────┘
             │
             ▼
 ┌─────────────────────┐
 │  Chatbot Frontend   │
 │ (React.js UI)       │
 └────┬────────────────┘
      ▼
 ┌────────────────────────────────────┐
 │ Backend API Server (FastAPI)       │
 └────┬────────────┬─────────────────┘
      ▼            ▼
┌────────────┐ ┌─────────────────────┐
│  RAG Flow  │ │  Chart Generator    │
│ (LLM + DB) │ │ (Matplotlib)        │
└────┬───────┘ └─────────────────────┘
     ▼
┌─────────────────────────────┐
│ Vector DB (Pinecone)        │
│  (Chunks + Embeddings)      │
└────────────┬────────────────┘
             ▼
   ┌──────────────────────┐
   │  Document Store      │
   │  (PDFs/Text)         │
   └──────────────────────┘
```

## Sequence Diagram

```
User → Frontend: Enter query
Frontend → Backend: Send query
Backend → Pinecone: Embed & search chunks
Backend → LLM: Generate answer
Backend → Chart Generator: (if numeric) Generate chart
Backend → SQL DB: Store search history/feedback
Backend → Frontend: Return answer, sources, chart
Frontend → User: Display results
```

## Development Phases
1. Data Collection
2. Text Extraction, Chunking, Embedding
3. RAG Integration
4. Chatbot Interface + Backend API
5. Chart Generator Integration
6. Feedback Loop + Logging
7. Dockerization + Deployment


