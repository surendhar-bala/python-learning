from fastapi import FastAPI
from app.api.documents import router as documents_router

app = FastAPI(title="PDF Chatbot API")

app.include_router(documents_router, prefix="/documents")


@app.get("/")
def root():
    return {"message": "PDF Chatbot API is running"}