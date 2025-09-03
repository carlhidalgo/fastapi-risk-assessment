from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from app.models.base import Base, IDMixin, TimestampMixin


class User(Base, IDMixin, TimestampMixin):
    """User model for authentication"""
    
    __tablename__ = "users"
    
    # User fields
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
        doc="User email address (unique)"
    )
    
    hashed_password = Column(
        String(255),
        nullable=False,
        doc="Hashed password using bcrypt"
    )
    
    full_name = Column(
        String(255),
        nullable=True,
        doc="User full name"
    )
    
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        doc="Whether the user account is active"
    )
    
    is_superuser = Column(
        Boolean,
        default=False,
        nullable=False,
        doc="Whether the user has admin privileges"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}')>"
