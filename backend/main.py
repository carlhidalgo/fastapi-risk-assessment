from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
from datetime import datetime, timedelta
import bcrypt
import uuid

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.company import Company
from app.models.request import Request

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models for request/response
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None

class CompanyResponse(BaseModel):
    id: str
    name: str
    industry: Optional[str]
    company_size: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class RiskAssessmentRequest(BaseModel):
    company_id: str
    risk_inputs: dict

class RiskAssessmentResponse(BaseModel):
    id: str
    user_id: str
    company_id: str
    risk_level: Optional[str]
    risk_score: Optional[float]
    risk_inputs: dict
    recommendations: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Utility functions
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Risk assessment logic
def calculate_risk_score(risk_inputs: dict) -> tuple[str, float, List[str]]:
    """
    Calculate risk score based on input parameters
    This is a simplified risk assessment algorithm
    """
    score = 0.0
    recommendations = []
    
    # Financial risk factors
    if "annual_revenue" in risk_inputs:
        revenue = risk_inputs["annual_revenue"]
        if revenue < 100000:
            score += 0.3
            recommendations.append("Consider improving revenue streams")
        elif revenue < 500000:
            score += 0.2
        elif revenue < 1000000:
            score += 0.1
    
    # Operational risk factors
    if "employee_count" in risk_inputs:
        employees = risk_inputs["employee_count"]
        if employees < 10:
            score += 0.2
            recommendations.append("Small team size may increase operational risk")
        elif employees > 500:
            score += 0.1
    
    # Market risk factors
    if "market_volatility" in risk_inputs:
        volatility = risk_inputs["market_volatility"]
        if volatility == "high":
            score += 0.3
            recommendations.append("High market volatility detected")
        elif volatility == "medium":
            score += 0.2
        elif volatility == "low":
            score += 0.1
    
    # Technology risk factors
    if "technology_adoption" in risk_inputs:
        tech = risk_inputs["technology_adoption"]
        if tech == "low":
            score += 0.2
            recommendations.append("Consider improving technology adoption")
        elif tech == "medium":
            score += 0.1
    
    # Determine risk level
    if score >= 0.7:
        risk_level = "HIGH"
        recommendations.append("Immediate risk mitigation required")
    elif score >= 0.4:
        risk_level = "MEDIUM"
        recommendations.append("Monitor risk factors closely")
    else:
        risk_level = "LOW"
        recommendations.append("Maintain current risk management practices")
    
    return risk_level, score, recommendations

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastAPI Risk Assessment API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at
    )

@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user and return JWT token"""
    # Find user
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return TokenResponse(access_token=access_token, token_type="bearer")

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )

@app.post("/api/v1/companies", response_model=CompanyResponse)
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new company"""
    company = Company(
        name=company_data.name,
        industry=company_data.industry,
        company_size=company_data.company_size
    )
    
    db.add(company)
    await db.commit()
    await db.refresh(company)
    
    return CompanyResponse(
        id=str(company.id),
        name=company.name,
        industry=company.industry,
        company_size=company.company_size,
        created_at=company.created_at
    )

@app.get("/api/v1/companies", response_model=List[CompanyResponse])
async def get_companies(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all companies"""
    result = await db.execute(select(Company))
    companies = result.scalars().all()
    
    return [
        CompanyResponse(
            id=str(company.id),
            name=company.name,
            industry=company.industry,
            company_size=company.company_size,
            created_at=company.created_at
        )
        for company in companies
    ]

@app.post("/api/v1/risk-assessment", response_model=RiskAssessmentResponse)
async def create_risk_assessment(
    assessment_data: RiskAssessmentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new risk assessment"""
    # Verify company exists
    result = await db.execute(select(Company).where(Company.id == uuid.UUID(assessment_data.company_id)))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Calculate risk score
    risk_level, risk_score, recommendations = calculate_risk_score(assessment_data.risk_inputs)
    
    # Create risk assessment request
    risk_request = Request(
        user_id=current_user.id,
        company_id=uuid.UUID(assessment_data.company_id),
        risk_level=risk_level,
        risk_score=risk_score,
        risk_inputs=assessment_data.risk_inputs,
        recommendations=recommendations
    )
    
    db.add(risk_request)
    await db.commit()
    await db.refresh(risk_request)
    
    return RiskAssessmentResponse(
        id=str(risk_request.id),
        user_id=str(risk_request.user_id),
        company_id=str(risk_request.company_id),
        risk_level=risk_request.risk_level,
        risk_score=risk_request.risk_score,
        risk_inputs=risk_request.risk_inputs,
        recommendations=risk_request.recommendations,
        created_at=risk_request.created_at
    )

@app.get("/api/v1/risk-assessments", response_model=List[RiskAssessmentResponse])
async def get_risk_assessments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all risk assessments for the current user"""
    result = await db.execute(
        select(Request).where(Request.user_id == current_user.id)
    )
    assessments = result.scalars().all()
    
    return [
        RiskAssessmentResponse(
            id=str(assessment.id),
            user_id=str(assessment.user_id),
            company_id=str(assessment.company_id),
            risk_level=assessment.risk_level,
            risk_score=assessment.risk_score,
            risk_inputs=assessment.risk_inputs,
            recommendations=assessment.recommendations,
            created_at=assessment.created_at
        )
        for assessment in assessments
    ]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
