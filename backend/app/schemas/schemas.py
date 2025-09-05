from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    full_name: str
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
    email: str
    phone: str
    industry: str
    annual_revenue: float
    company_size: int

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    industry: Optional[str] = None
    annual_revenue: Optional[float] = None
    company_size: Optional[int] = None

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

class RequestUpdate(BaseModel):
    company_id: Optional[str] = None
    amount: Optional[float] = None
    purpose: Optional[str] = None
    risk_inputs: Optional[dict] = None
    status: Optional[str] = None

class RequestResponse(RequestBase):
    id: str
    risk_score: float
    status: str
    risk_level: Optional[str] = None
    recommendations: Optional[str] = None
    approved: Optional[bool] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class RequestListResponse(BaseModel):
    id: str
    company_id: str
    amount: float
    purpose: str
    risk_inputs: dict
    status: str
    risk_level: Optional[str] = None
    risk_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Pagination schemas
class PaginatedResponse(BaseModel):
    items: list
    page: int
    size: int
    total: int
    pages: int

class PaginatedRequestsResponse(BaseModel):
    items: List[RequestListResponse]
    page: int
    size: int
    total: int
    pages: int
