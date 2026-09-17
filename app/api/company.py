from fastapi import APIRouter
from pydantic import BaseModel

from app.services.web_search import search_company
from app.services.ollama_service import extract_company_info

router = APIRouter(prefix="/api/v1/clients", tags=["Clients"])

class CompanyRequest(BaseModel):
    company_name: str

@router.post("/search")
def search_client(request: CompanyRequest):

    web_content = search_company(request.company_name)

    company = extract_company_info(web_content)

    return {
        "success": True,
        "company": company
    }