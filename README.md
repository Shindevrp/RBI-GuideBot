# RBI GuideBot

An autonomous, agentic email-based assistant for NBFC professionals. It automatically ingests, classifies, and responds to queries about RBI guidelines and internal lending processes. It also includes a traditional web-based RAG chatbot interface.

## Project Structure
- `backend/`: Contains the FastAPI server for the web chat and the complete agentic email workflow.
  - `agents/`: Houses the Classifier, Coordinator, and Retrieval agents.
  - `core/`: Core logic for orchestration, configuration, and the main agent service runner.
  - `db/`: Database models, session management, and CRUD operations for logging.
  - `services/`: Connectors for external services like Email (IMAP/SMTP).
  - `api/`: The FastAPI application for the web chat interface.
- `frontend/`: React.js UI for the web chat and feedback.
- `data/`: Source documents like RBI circulars, PDFs, etc.

## Setup Instructions
1. Install Python 3.10+ and Node.js.
2. Create a `.env` file in the `backend` directory. Populate it with your credentials. See `backend/core/config.py` for all required variables (OpenAI, Pinecone, IMAP, SMTP).
3. **Backend**: `cd backend && pip install -r requirements.txt`
4. **Frontend**: `cd frontend && npm install`
5. **Run Agentic Service**: `python -m backend.run_agent_service`
6. **Run Web Chat Backend**: `uvicorn backend.api.main:app --reload`
7. **Run Web Chat Frontend**: `cd frontend && npm start`

## Features
- **Agentic Email Workflow**:
  - **Email Ingestion Agent**: Automatically reads unread emails from a specified inbox (e.g., `compliance@nbfcbot.com`).
  - **Email Classifier Agent**: Uses an LLM to classify email intent (RBI Regulation, NBFC Lending, Combined, or Other).
  - **Coordinator & Retrieval Agents**: Routes the query to the correct RAG pipeline, retrieving context from separate vector databases (one for RBI rules, one for internal lending processes).
  - **Response Generation Agent**: Generates a contextual, natural-language answer with sources.
  - **Email Reply Agent**: Automatically sends the formatted response back to the customer.
- **Database Logging**: Every email interaction is logged in a database for auditing and review.
- **Web Chat Interface**: A traditional RAG chatbot interface is also available for direct queries.
- **Document Ingestion**: Scripts to ingest, chunk, embed, and store documents in Pinecone vector stores.

## Technical Architecture

### Architecture Add-on (Agentic Layer)
```plaintext
               ┌────────────┐
               │   Email    │
               │  Inbox     │
               └────┬───────┘
                    ▼
           ┌──────────────────┐
           │ Email Ingestion  │
           └────┬─────────────┘
                ▼
     ┌─────────────────────────────┐
     │ Email Classifier Agent      │
     │ (RBI / Lending / Other?)    │
     └────┬─────────────┬──────────┘
          ▼             ▼
   ┌────────────┐ ┌──────────────┐
   │ Regulation │ │   Lending    │
   │   Agent    │ │    Agent     │
   │ (RBI DB)   │ │ (NBFC DB)    │
   └────┬───────┘ └─────┬────────┘
        ▼               ▼
     ┌─────────────────────┐
     │ Coordinator Agent   │
     │ (Merge, Format)     │
     └────┬────────────────┘
          ▼
 ┌────────────────────┐
 │ Email Reply Agent  │
 └────────────────────┘
```

### Web Chatbot Architecture
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

### Web Chatbot Flow
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
