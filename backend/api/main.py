from fastapi import FastAPI, UploadFile, File, Form
from backend.ingest.extract_and_chunk import process_pdf
from backend.rag.query_rag import rag_query
from backend.charts.generate_chart import generate_chart
from typing import List, Optional

app = FastAPI(title="RBI GuideBot API")

@app.post("/ingest")
def ingest_pdf(file: UploadFile = File(...)):
    """Ingest a PDF and process it into chunks and embeddings."""
    result = process_pdf(file)
    return {"status": "success", "chunks": result}

@app.post("/ask")
def ask_query(query: str = Form(...)):
    """Answer user query using RAG pipeline."""
    answer, sources, chart_data = rag_query(query)
    chart_url = None
    if chart_data:
        chart_url = generate_chart(chart_data)
    return {"answer": answer, "sources": sources, "chart": chart_url}

@app.post("/feedback")
def feedback(query: str = Form(...), answer_id: str = Form(...), helpful: bool = Form(...)):
    # Store feedback in DB (to be implemented)
    return {"status": "received"}

@app.post("/download")
def download_pdfs():
    """Download RBI PDFs."""
    from backend.ingest.download_rbi_pdfs import download_pdfs
    download_pdfs()
    return {"status": "PDFs downloaded"}
