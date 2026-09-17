from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from app.services.embedding_service import create_embeddings

from app.services.pdf_service import (
    extract_text_from_pdf,
    split_text,
)
from app.services.query_service import search_documents
from app.services.vector_service import store_embeddings


router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class QueryRequest(BaseModel):
    question: str


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed",
        )

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        while chunk := await file.read(1024 * 1024):
            buffer.write(chunk)

    # Step 2: Extract text
    text = extract_text_from_pdf(file_path)

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from PDF",
        )

    # Step 3: Split text into chunks
    chunks = split_text(text)

      # Create embeddings
    embeddings = create_embeddings(chunks)

    total_stored = store_embeddings(
    chunks,
    embeddings,
    file.filename
)

    return {
        "message": "PDF processed successfully",
        "filename": file.filename,
        "total_characters": len(text),
        "total_chunks": len(chunks),
        "embedding_dimensions": len(embeddings[0]),
    "stored_chunks": total_stored

    }


@router.post("/query")
def query_pdf(request: QueryRequest):
    results = search_documents(request.question)

    return {
        "question": request.question,
        "results": results
    }