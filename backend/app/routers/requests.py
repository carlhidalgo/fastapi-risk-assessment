from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional
from datetime import datetime, timezone
import math

from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.request import Request
from app.schemas.schemas import (
    RequestCreate, 
    RequestUpdate, 
    RequestResponse, 
    RequestListResponse,
    PaginatedRequestsResponse,
    RiskRequest
)
from app.services.auth import get_current_user
from app.services.risk_calculator import calculate_risk_score

router = APIRouter(prefix="/requests", tags=["requests"])


@router.get("/", response_model=PaginatedRequestsResponse)
def get_requests(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    search: Optional[str] = Query(None, description="Search in purpose or company name"),
    company_id: Optional[str] = Query(None, description="Filter by company ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    min_amount: Optional[float] = Query(None, description="Minimum amount"),
    max_amount: Optional[float] = Query(None, description="Maximum amount"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get paginated requests for current user with filters"""
    
    # Base query - only user's requests
    query = db.query(Request).filter(Request.user_id == current_user.id)
    
    # Apply filters
    if company_id:
        query = query.filter(Request.company_id == company_id)
    
    if status:
        query = query.filter(Request.status == status)
    
    if risk_level:
        query = query.filter(Request.risk_level == risk_level)
    
    if min_amount is not None:
        query = query.filter(Request.amount >= min_amount)
    
    if max_amount is not None:
        query = query.filter(Request.amount <= max_amount)
    
    # Search in purpose or company name
    if search:
        # Join with companies table for search
        query = query.join(Company, Request.company_id == Company.id)
        query = query.filter(
            or_(
                Request.purpose.ilike(f"%{search}%"),
                Company.name.ilike(f"%{search}%")
            )
        )
    
    # Get total count for pagination
    total = query.count()
    
    # Calculate pagination
    offset = (page - 1) * size
    pages = math.ceil(total / size)
    
    # Get paginated results
    requests = query.offset(offset).limit(size).all()
    
    # Convert to response format
    items = [
        RequestListResponse(
            id=str(req.id),
            company_id=str(req.company_id),
            amount=req.amount,
            purpose=req.purpose,
            risk_inputs=req.risk_inputs,
            status=req.status,
            risk_level=req.risk_level,
            risk_score=req.risk_score,
            created_at=req.created_at
        )
        for req in requests
    ]
    
    return PaginatedRequestsResponse(
        items=items,
        page=page,
        size=size,
        total=total,
        pages=pages
    )


@router.post("/", response_model=RequestResponse)
def create_request(
    request_data: RequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new request"""
    
    # Verify company exists and belongs to user
    try:
        company_id_int = int(request_data.company_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid company ID format")
    
    company = db.query(Company).filter(
        Company.id == company_id_int,
        Company.user_id == current_user.id
    ).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Create risk assessment data for calculation
    risk_data = RiskRequest(
        company_id=request_data.company_id,
        amount=request_data.amount,
        purpose=request_data.purpose,
        annual_revenue=request_data.risk_inputs.get('annual_revenue', company.annual_revenue),
        employee_count=request_data.risk_inputs.get('employee_count', company.company_size),
        years_in_business=request_data.risk_inputs.get('years_in_business'),
        debt_to_equity_ratio=request_data.risk_inputs.get('debt_to_equity_ratio'),
        credit_score=request_data.risk_inputs.get('credit_score')
    )
    
    # Calculate risk score
    risk_result = calculate_risk_score(risk_data)

    # Create request
    new_request = Request(
        user_id=current_user.id,
        company_id=company_id_int,
        amount=request_data.amount,
        purpose=request_data.purpose,
        risk_inputs=request_data.risk_inputs,
        risk_score=risk_result.risk_score,
        risk_level=risk_result.risk_level,
        status="pending",  # Start as pending, can be updated later
        approved=False     # Will be determined when status is updated
    )
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return RequestResponse(
        id=str(new_request.id),
        company_id=str(new_request.company_id),
        amount=new_request.amount,
        purpose=new_request.purpose,
        risk_inputs=new_request.risk_inputs,
        risk_score=new_request.risk_score,
        status=new_request.status,
        risk_level=new_request.risk_level,
        recommendations=new_request.recommendations,
        approved=new_request.approved,
        created_at=new_request.created_at,
        updated_at=new_request.updated_at
    )


@router.get("/{request_id}", response_model=RequestResponse)
def get_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific request by ID"""
    
    try:
        request_id_int = int(request_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request ID format")
    
    request = db.query(Request).filter(
        Request.id == request_id_int,
        Request.user_id == current_user.id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return RequestResponse(
        id=str(request.id),
        company_id=str(request.company_id),
        amount=request.amount,
        purpose=request.purpose,
        risk_inputs=request.risk_inputs,
        risk_score=request.risk_score,
        status=request.status,
        risk_level=request.risk_level,
        recommendations=request.recommendations,
        approved=request.approved,
        created_at=request.created_at,
        updated_at=request.updated_at
    )


@router.put("/{request_id}", response_model=RequestResponse)
def update_request(
    request_id: str,
    request_data: RequestUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a specific request"""
    
    try:
        request_id_int = int(request_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request ID format")
    
    request = db.query(Request).filter(
        Request.id == request_id_int,
        Request.user_id == current_user.id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Update fields if provided
    update_data = request_data.dict(exclude_unset=True)
    
    if "company_id" in update_data:
        # Verify new company belongs to user
        try:
            company_id_int = int(update_data["company_id"])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid company ID format")
        
        company = db.query(Company).filter(
            Company.id == company_id_int,
            Company.user_id == current_user.id
        ).first()
        
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        request.company_id = company_id_int
    
    # Update other fields
    for field, value in update_data.items():
        if field != "company_id" and hasattr(request, field):
            setattr(request, field, value)
    
    # Get company for risk calculation
    company = db.query(Company).filter(
        Company.id == request.company_id,
        Company.user_id == current_user.id
    ).first()
    
    # Recalculate risk score only if relevant fields were updated
    if any(field in update_data for field in ["amount", "purpose", "risk_inputs"]):
        risk_data = RiskRequest(
            company_id=str(request.company_id),
            amount=request.amount,
            purpose=request.purpose,
            annual_revenue=request.risk_inputs.get('annual_revenue', company.annual_revenue if company else None),
            employee_count=request.risk_inputs.get('employee_count', company.company_size if company else None),
            years_in_business=request.risk_inputs.get('years_in_business'),
            debt_to_equity_ratio=request.risk_inputs.get('debt_to_equity_ratio'),
            credit_score=request.risk_inputs.get('credit_score')
        )
        
        risk_result = calculate_risk_score(risk_data)
        request.risk_score = risk_result.risk_score
        request.risk_level = risk_result.risk_level
        # Only update status if not manually specified
        if "status" not in update_data:
            request.status = "approved" if risk_result.approved else "rejected"
            request.approved = risk_result.approved

    request.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(request)
    
    return RequestResponse(
        id=str(request.id),
        company_id=str(request.company_id),
        amount=request.amount,
        purpose=request.purpose,
        risk_inputs=request.risk_inputs,
        risk_score=request.risk_score,
        status=request.status,
        risk_level=request.risk_level,
        recommendations=request.recommendations,
        approved=request.approved,
        created_at=request.created_at,
        updated_at=request.updated_at
    )


@router.delete("/{request_id}")
def delete_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a specific request"""
    
    try:
        request_id_int = int(request_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid request ID format")
    
    request = db.query(Request).filter(
        Request.id == request_id_int,
        Request.user_id == current_user.id
    ).first()
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    db.delete(request)
    db.commit()
    
    return {"message": "Request deleted successfully"}


@router.get("/stats/summary")
def get_requests_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary statistics for user's requests"""
    
    total_requests = db.query(Request).filter(Request.user_id == current_user.id).count()
    
    approved_requests = db.query(Request).filter(
        Request.user_id == current_user.id,
        Request.status == "approved"
    ).count()
    
    rejected_requests = db.query(Request).filter(
        Request.user_id == current_user.id,
        Request.status == "rejected"
    ).count()
    
    pending_requests = db.query(Request).filter(
        Request.user_id == current_user.id,
        Request.status == "pending"
    ).count()
    
    # Calculate total amount requested
    total_amount = db.query(Request).filter(
        Request.user_id == current_user.id
    ).with_entities(Request.amount).all()
    
    total_amount_sum = sum([req.amount for req in total_amount]) if total_amount else 0
    
    return {
        "total_requests": total_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests,
        "pending_requests": pending_requests,
        "total_amount_requested": total_amount_sum,
        "approval_rate": round((approved_requests / total_requests * 100), 2) if total_requests > 0 else 0
    }
