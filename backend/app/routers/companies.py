from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.schemas.schemas import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.auth import get_current_user

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company for the current user"""
    company = Company(
        name=company_data.name,
        email=company_data.email,
        phone=company_data.phone,
        industry=company_data.industry,
        annual_revenue=company_data.annual_revenue,
        company_size=company_data.company_size,
        user_id=current_user.id  # Asignar al usuario actual
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
    """Get companies for the current user only"""
    companies = db.query(Company).filter(Company.user_id == current_user.id).all()
    
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


@router.get("/test/no-auth", response_model=List[CompanyResponse])
def list_companies_no_auth(db: Session = Depends(get_db)):
    """Test endpoint - Get all companies without authentication"""
    companies = db.query(Company).limit(5).all()  # Solo 5 para testing
    
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
    """Get a specific company (only if owned by current user)"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id  # Solo empresas del usuario actual
    ).first()
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


@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a company (only if owned by current user)"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Update only provided fields
    update_data = company_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    
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


@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a company (only if owned by current user)"""
    company = db.query(Company).filter(
        Company.id == company_id,
        Company.user_id == current_user.id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    
    return {"message": "Company deleted successfully"}
