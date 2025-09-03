from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import jwt
from datetime import datetime, timedelta
import bcrypt
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.request import Request
from app.schemas.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    CompanyCreate, CompanyResponse,
    RiskRequest, RiskResponse
)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Authentication functions
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Risk assessment logic
def calculate_risk_score(risk_data: dict) -> tuple[str, float, List[str]]:
    """Calculate risk score based on input parameters"""
    score = 0.0
    recommendations = []
    
    # Financial risk factors
    annual_revenue = risk_data.get("annual_revenue", 0)
    if annual_revenue < 100000:
        score += 0.3
        recommendations.append("Consider improving revenue streams")
    elif annual_revenue < 500000:
        score += 0.2
    elif annual_revenue < 1000000:
        score += 0.1
    
    # Operational risk factors
    employee_count = risk_data.get("employee_count", 0)
    if employee_count < 5:
        score += 0.2
        recommendations.append("Consider expanding team for operational stability")
    elif employee_count < 20:
        score += 0.1
    
    # Business maturity
    years_in_business = risk_data.get("years_in_business", 0)
    if years_in_business < 2:
        score += 0.25
        recommendations.append("Business needs more operational history")
    elif years_in_business < 5:
        score += 0.15
    
    # Financial health
    debt_to_equity = risk_data.get("debt_to_equity_ratio", 0)
    if debt_to_equity > 2.0:
        score += 0.2
        recommendations.append("High debt-to-equity ratio requires attention")
    elif debt_to_equity > 1.0:
        score += 0.1
    
    # Credit score
    credit_score = risk_data.get("credit_score", 700)
    if credit_score < 600:
        score += 0.3
        recommendations.append("Improve credit score for better terms")
    elif credit_score < 700:
        score += 0.15
    
    # Normalize score to 0-1 range
    score = min(score, 1.0)
    
    # Determine risk level
    if score <= 0.3:
        risk_level = "LOW"
    elif score <= 0.6:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    
    if not recommendations:
        recommendations.append("Good financial standing")
    
    return risk_level, score, recommendations

# API Routes
@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "FastAPI Risk Assessment API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.post("/api/v1/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return UserResponse(
            id=str(user.id),
            email=user.email,
            name=user.full_name,
            created_at=user.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in register endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/v1/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    # Find user
    user = db.query(User).filter(User.email == user_data.email).first()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/api/v1/auth/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        created_at=current_user.created_at
    )

@app.post("/api/v1/companies", response_model=CompanyResponse)
def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new company"""
    company = Company(
        name=company_data.name,
        industry=company_data.industry,
        size=company_data.size
    )
    
    db.add(company)
    db.commit()
    db.refresh(company)
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        industry=company.industry,
        size=company.size,
        created_at=company.created_at
    )

@app.get("/api/v1/companies", response_model=List[CompanyResponse])
def get_companies(
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
            created_at=company.created_at
        )
        for company in companies
    ]

@app.post("/api/v1/risk-assessment", response_model=RiskResponse)
def create_risk_assessment(
    risk_data: RiskRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new risk assessment"""
    # Verify company exists
    company = db.query(Company).filter(Company.id == uuid.UUID(risk_data.company_id)).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Prepare risk inputs
    risk_inputs = {
        "annual_revenue": risk_data.annual_revenue,
        "employee_count": risk_data.employee_count,
        "years_in_business": risk_data.years_in_business,
        "debt_to_equity_ratio": risk_data.debt_to_equity_ratio,
        "credit_score": risk_data.credit_score
    }
    
    # Calculate risk score
    risk_level, risk_score, recommendations = calculate_risk_score(risk_inputs)
    
    # Create risk assessment request
    risk_request = Request(
        user_id=current_user.id,
        company_id=uuid.UUID(risk_data.company_id),
        amount=risk_data.amount,
        purpose=risk_data.purpose,
        risk_level=risk_level,
        risk_score=risk_score,
        status="completed",
        risk_inputs=risk_inputs,
        recommendations=recommendations
    )
    
    db.add(risk_request)
    db.commit()
    db.refresh(risk_request)
    
    # Determine approval (simplified logic)
    approved = risk_level in ["LOW", "MEDIUM"] and risk_score < 0.7
    
    return RiskResponse(
        risk_level=risk_level,
        risk_score=risk_score,
        recommendations=recommendations,
        approved=approved
    )

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
