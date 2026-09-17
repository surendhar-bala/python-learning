from pydantic import BaseModel

class CompanyRequest(BaseModel):
    company_name: str

class CompanyInfo(BaseModel):
    legal_name: str | None = None
    website: str | None = None
    industry: str | None = None
    description: str | None = None
    headquarters: str | None = None