from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.request import Request
from app.schemas.schemas import RiskRequest, RiskResponse
from app.services.auth import get_current_user
from app.services.risk_calculator import calculate_risk_score

router = APIRouter(prefix="/risk", tags=["risk assessment"])


@router.post("/assess", response_model=RiskResponse)
def assess_risk(
    risk_data: RiskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new risk assessment"""
    try:
        company_id_int = int(risk_data.company_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")
    
    # Verify company exists and belongs to user
    company = db.query(Company).filter(
        Company.id == company_id_int,
        Company.user_id == current_user.id
    ).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Use the new calculation method
    result = calculate_risk_score(risk_data)
    
    # Create risk assessment request in database
    risk_request = Request(
        user_id=current_user.id,
        company_id=company_id_int,
        amount=risk_data.amount,
        purpose=risk_data.purpose,
        risk_level=result.risk_level,
        risk_score=result.risk_score,
        status="approved" if result.approved else "rejected",
        risk_inputs={
            'amount': risk_data.amount,
            'purpose': risk_data.purpose,
            'company_size': company.company_size,
            'industry': company.industry,
            'annual_revenue': risk_data.annual_revenue or company.annual_revenue,
            'employee_count': risk_data.employee_count,
            'years_in_business': risk_data.years_in_business,
            'debt_to_equity_ratio': risk_data.debt_to_equity_ratio,
            'credit_score': risk_data.credit_score
        },
        recommendations="; ".join(result.recommendations),
        approved=result.approved
    )
    
    db.add(risk_request)
    db.commit()
    db.refresh(risk_request)
    
    return RiskResponse(
        risk_level=result.risk_level,
        risk_score=result.risk_score,
        recommendations=result.recommendations,
        approved=result.approved
    )
