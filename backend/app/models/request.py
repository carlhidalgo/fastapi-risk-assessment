from sqlalchemy import Column, String, Text, Integer, Float, JSON, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from enum import Enum

from app.models.base import Base, IDMixin, TimestampMixin


class RequestStatus(str, Enum):
    """Request status options"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"
    CANCELLED = "cancelled"


class RequestPurpose(str, Enum):
    """Purpose of the risk assessment request"""
    LOAN = "loan"
    INVESTMENT = "investment"
    PARTNERSHIP = "partnership"
    ACQUISITION = "acquisition"
    EXPANSION = "expansion"
    OTHER = "other"


class Request(Base, IDMixin, TimestampMixin):
    """Risk assessment request model"""
    
    __tablename__ = "requests"
    
    # Foreign key to company
    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID of the company being assessed"
    )
    
    # Foreign key to user
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc="ID of the user who created this request"
    )
    
    # Request details
    amount = Column(
        Float,
        nullable=False,
        doc="Requested amount in USD"
    )
    
    purpose = Column(
        String(255),
        nullable=False,
        doc="Purpose of the request"
    )
    
    description = Column(
        Text,
        nullable=True,
        doc="Additional description of the request"
    )
    
    # Risk assessment data
    risk_inputs = Column(
        JSON,
        nullable=True,
        default={},
        doc="JSON object containing risk assessment inputs"
    )
    
    risk_score = Column(
        Float,
        nullable=True,
        doc="Calculated risk score (0-100)"
    )
    
    risk_level = Column(
        String(50),
        nullable=True,
        doc="Risk level: LOW, MEDIUM, HIGH"
    )
    
    approved = Column(
        Boolean,
        nullable=True,
        default=False,
        doc="Whether the request is approved based on risk assessment"
    )
    
    recommendations = Column(
        Text,
        nullable=True,
        doc="Risk assessment recommendations"
    )
    
    # Status and workflow
    status = Column(
        SQLEnum(RequestStatus),
        default=RequestStatus.PENDING,
        nullable=False,
        index=True,
        doc="Current status of the request"
    )
    
    notes = Column(
        Text,
        nullable=True,
        doc="Internal notes about the request"
    )
    
    # Relationships
    company = relationship(
        "Company",
        back_populates="requests",
        doc="Company associated with this request"
    )
    
    user = relationship(
        "User",
        doc="User who created this request"
    )

    def __repr__(self) -> str:
        return f"<Request(id={self.id}, company_id={self.company_id}, amount=${self.amount}, status='{self.status}')>"
    
    def calculate_risk_score(self) -> float:
        """
        Calculate risk score based on amount, company info, and risk inputs
        Returns a score between 0-100 (higher = more risky)
        """
        if not self.company:
            return 50.0  # Default medium risk if no company data
            
        base_score = 0.0
        
        # Factor 1: Amount-based risk (0-30 points)
        if self.amount >= 100_000:
            base_score += 30
        elif self.amount >= 50_000:
            base_score += 20
        elif self.amount >= 25_000:
            base_score += 15
        else:
            base_score += 10
            
        # Factor 2: Company size risk (0-25 points)
        size_risk = {
            "startup": 25,
            "small": 20,
            "medium": 15,
            "large": 10,
            "enterprise": 5
        }
        base_score += size_risk.get(self.company.size, 15)
        
        # Factor 3: Industry risk (0-25 points)
        industry_risk = {
            "technology": 20,
            "finance": 15,
            "healthcare": 10,
            "retail": 15,
            "manufacturing": 10,
            "real_estate": 25,
            "education": 5,
            "consulting": 15,
            "other": 20
        }
        base_score += industry_risk.get(self.company.industry, 15)
        
        # Factor 4: Purpose risk (0-20 points)
        purpose_risk = {
            "loan": 15,
            "investment": 20,
            "partnership": 10,
            "acquisition": 25,
            "expansion": 15,
            "other": 20
        }
        base_score += purpose_risk.get(self.purpose, 15)
        
        # Factor 5: Risk inputs adjustment (-20 to +20 points)
        if self.risk_inputs:
            # Good factors (reduce risk)
            if self.risk_inputs.get("good_credit_history"):
                base_score -= 10
            if self.risk_inputs.get("stable_revenue"):
                base_score -= 10
            if self.risk_inputs.get("experienced_management"):
                base_score -= 5
                
            # Bad factors (increase risk)
            if self.risk_inputs.get("high_debt_ratio"):
                base_score += 15
            if self.risk_inputs.get("volatile_market"):
                base_score += 10
            if self.risk_inputs.get("regulatory_issues"):
                base_score += 20
        
        # Ensure score is between 0-100
        return max(0.0, min(100.0, base_score))
