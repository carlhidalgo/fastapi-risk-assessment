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
        industry=company_data.industry,
        size=company_data.size,
        description=company_data.description,
        address=company_data.address,
        phone=company_data.phone,
        email=company_data.email,
        website=company_data.website,
        years_in_business=company_data.years_in_business,
        annual_revenue=company_data.annual_revenue,
        employee_count=company_data.employee_count
    )
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        industry=company.industry,
        size=company.size,
        description=company.description,
        address=company.address,
        phone=company.phone,
        email=company.email,
        website=company.website,
        years_in_business=company.years_in_business,
        annual_revenue=company.annual_revenue,
        employee_count=company.employee_count,
        created_at=company.created_at.isoformat()
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
            industry=company.industry,
            size=company.size,
            description=company.description,
            address=company.address,
            phone=company.phone,
            email=company.email,
            website=company.website,
            years_in_business=company.years_in_business,
            annual_revenue=company.annual_revenue,
            employee_count=company.employee_count,
            created_at=company.created_at.isoformat()
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
        industry=company.industry,
        size=company.size,
        description=company.description,
        address=company.address,
        phone=company.phone,
        email=company.email,
        website=company.website,
        years_in_business=company.years_in_business,
        annual_revenue=company.annual_revenue,
        employee_count=company.employee_count,
        created_at=company.created_at.isoformat()
    )
