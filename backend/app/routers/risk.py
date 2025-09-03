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
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id_int).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Prepare risk inputs
    risk_inputs = {
        'amount': risk_data.amount,
        'purpose': risk_data.purpose,
        'company_size': company.size,
        'industry': company.industry,
        'years_in_business': company.years_in_business,
        'annual_revenue': company.annual_revenue,
        'credit_score': risk_data.credit_score
    }
    
    # Calculate risk
    risk_level, risk_score, recommendations = calculate_risk_score(risk_inputs)
    
    # Determine approval status
    approved = risk_level in ["LOW", "MEDIUM"]
    
    # Create risk assessment request
    risk_request = Request(
        user_id=current_user.id,
        company_id=company_id_int,
        amount=risk_data.amount,
        purpose=risk_data.purpose,
        risk_level=risk_level,
        risk_score=risk_score,
        status="completed",
        risk_inputs=risk_inputs,
        recommendations=recommendations,
        approved=approved
    )
    
    db.add(risk_request)
    db.commit()
    db.refresh(risk_request)
    
    return RiskResponse(
        request_id=str(risk_request.id),
        risk_level=risk_level,
        risk_score=risk_score,
        recommendations=recommendations,
        approved=approved
    )
