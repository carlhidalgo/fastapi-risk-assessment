from sqlalchemy import Column, String, Text, Float, Integer, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from app.models.base import Base, IDMixin, TimestampMixin


class CompanySize(str, Enum):
    """Company size categories"""
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class IndustryType(str, Enum):
    """Industry types"""
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    RETAIL = "retail"
    MANUFACTURING = "manufacturing"
    REAL_ESTATE = "real_estate"
    EDUCATION = "education"
    CONSULTING = "consulting"
    OTHER = "other"


class Company(Base, IDMixin, TimestampMixin):
    """Company model for risk assessment"""
    
    __tablename__ = "companies"
    
    # Company basic info
    name = Column(
        String(255),
        nullable=False,
        index=True,
        doc="Company name"
    )
    
    email = Column(
        String(255),
        nullable=False,
        doc="Company email"
    )
    
    phone = Column(
        String(50),
        nullable=False,
        doc="Company phone"
    )
    
    industry = Column(
        String(100),
        nullable=False,
        doc="Company industry"
    )
    
    annual_revenue = Column(
        Float,
        nullable=False,
        doc="Company annual revenue"
    )
    
    company_size = Column(
        Integer,
        nullable=False,
        doc="Number of employees"
    )
    
    size = Column(
        SQLEnum(CompanySize),
        nullable=True,
        doc="Company size category"
    )
    
    description = Column(
        Text,
        nullable=True,
        doc="Company description"
    )
    
    website = Column(
        String(255),
        nullable=True,
        doc="Company website URL"
    )
    
    # Location
    country = Column(
        String(100),
        nullable=True,
        doc="Company country"
    )
    
    city = Column(
        String(100),
        nullable=True,
        doc="Company city"
    )
    
    # User ownership - NUEVA RELACION
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="ID of the user who owns this company"
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="companies",
        doc="User who owns this company"
    )
    
    requests = relationship(
        "Request",
        back_populates="company",
        cascade="all, delete-orphan",
        doc="Risk assessment requests for this company"
    )

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.name}', industry='{self.industry}')>"
