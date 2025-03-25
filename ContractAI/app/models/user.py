"""
User model for ContractAI.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    JSON
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from ContractAI.app.db.database import Base


class User(Base):
    """User model for system users."""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # Additional user information
    company = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    avatar_url = Column(String(512), nullable=True)
    preferences = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # API key for programmatic access
    api_key = Column(String(64), unique=True, index=True, nullable=True)
    api_key_expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "company": self.company,
            "job_title": self.job_title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None
        }
    
    def to_admin_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary with admin fields."""
        return {
            **self.to_dict(),
            "preferences": self.preferences,
            "phone": self.phone,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "api_key_expires_at": self.api_key_expires_at.isoformat() if self.api_key_expires_at else None
        }
