from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.company import router as company_router

load_dotenv()

app = FastAPI()

app.include_router(company_router)


@app.get("/")
def root():
    return {"message": "API is running"}