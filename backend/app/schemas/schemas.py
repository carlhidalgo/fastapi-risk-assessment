from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

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
