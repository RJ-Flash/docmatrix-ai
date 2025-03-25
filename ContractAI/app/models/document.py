"""
Document model for ContractAI.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    JSON,
    Enum as SQLAlchemyEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from ContractAI.app.db.database import Base


class DocumentStatus(str, enum.Enum):
    """Document processing status enumeration."""
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class Document(Base):
    """Document model for contract files."""
    
    __tablename__ = "documents"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(128), nullable=False)
    status = Column(SQLAlchemyEnum(DocumentStatus), default=DocumentStatus.UPLOADED)
    text_content = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="documents")
    analyses = relationship("DocumentAnalysis", back_populates="document", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert document to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "original_filename": self.original_filename,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata
        }


class DocumentAnalysis(Base):
    """Document analysis model for storing contract analysis results."""
    
    __tablename__ = "document_analyses"
    
    id = Column(String(36), primary_key=True, index=True)
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    clauses = Column(JSON, nullable=True)
    risks = Column(JSON, nullable=True)
    recommendations = Column(JSON, nullable=True)
    summary = Column(JSON, nullable=True)
    llm_provider = Column(String(50), nullable=True)
    llm_model = Column(String(100), nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="analyses")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "clauses": self.clauses,
            "risks": self.risks,
            "recommendations": self.recommendations,
            "summary": self.summary,
            "llm_provider": self.llm_provider,
            "llm_model": self.llm_model,
            "processing_time_ms": self.processing_time_ms,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
