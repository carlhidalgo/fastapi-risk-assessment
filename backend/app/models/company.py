from sqlalchemy import Column, String, Text, Enum as SQLEnum
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
    
    industry = Column(
        SQLEnum(IndustryType),
        nullable=False,
        doc="Company industry type"
    )
    
    size = Column(
        SQLEnum(CompanySize),
        nullable=False,
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
    
    # Relationships
    requests = relationship(
        "Request",
        back_populates="company",
        cascade="all, delete-orphan",
        doc="Risk assessment requests for this company"
    )

    def __repr__(self) -> str:
        return f"<Company(id={self.id}, name='{self.name}', industry='{self.industry}')>"
