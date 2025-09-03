from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCompany(BaseModel):
    id: str
    name: str
    industry: str
    size: str

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Company schemas
class CompanyBase(BaseModel):
    name: str
    industry: str
    size: str

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Risk Assessment schemas
class RiskRequest(BaseModel):
    company_id: str
    amount: float
    purpose: str
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    years_in_business: Optional[int] = None
    debt_to_equity_ratio: Optional[float] = None
    credit_score: Optional[int] = None

class RiskResponse(BaseModel):
    risk_level: str
    risk_score: float
    recommendations: List[str]
    approved: bool

# Request schemas
class RequestBase(BaseModel):
    company_id: str
    amount: float
    purpose: str
    risk_inputs: dict

class RequestCreate(RequestBase):
    pass

class RequestResponse(RequestBase):
    id: str
    risk_score: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Pagination schemas
class PaginatedResponse(BaseModel):
    items: list
    page: int
    size: int
    total: int
    pages: int
