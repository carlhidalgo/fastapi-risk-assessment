from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.schemas.schemas import CompanyCreate, CompanyResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    company = Company(
        name=company_data.name,
        email=company_data.email,
        phone=company_data.phone,
        industry=company_data.industry,
        annual_revenue=company_data.annual_revenue,
        company_size=company_data.company_size
    )
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        email=company.email,
        phone=company.phone,
        industry=company.industry,
        annual_revenue=company.annual_revenue,
        company_size=company.company_size,
        created_at=company.created_at
    )


@router.get("/", response_model=List[CompanyResponse])
def list_companies(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all companies"""
    companies = db.query(Company).all()
    
    return [
        CompanyResponse(
            id=str(company.id),
            name=company.name,
            email=company.email,
            phone=company.phone,
            industry=company.industry,
            annual_revenue=company.annual_revenue,
            company_size=company.company_size,
            created_at=company.created_at
        )
        for company in companies
    ]


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific company"""
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        email=company.email,
        phone=company.phone,
        industry=company.industry,
        annual_revenue=company.annual_revenue,
        company_size=company.company_size,
        created_at=company.created_at
    )
