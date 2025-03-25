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
import uuid

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
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
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
    """Document analysis model for storing analysis results."""
    
    __tablename__ = "document_analyses"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    analysis_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    document = relationship("Document", back_populates="analyses")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "analysis_type": self.analysis_type,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Clause(Base):
    """Clause model for storing extracted contract clauses."""
    
    __tablename__ = "clauses"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String(36), ForeignKey("documents.id"), nullable=False)
    clause_type = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)
    start_position = Column(Integer, nullable=True)
    end_position = Column(Integer, nullable=True)
    confidence = Column(Integer, nullable=True)  # 0-100 scale
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    document = relationship("Document")
    risks = relationship("ClauseRisk", back_populates="clause", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert clause to dictionary."""
        return {
            "id": self.id,
            "document_id": self.document_id,
            "clause_type": self.clause_type,
            "text": self.text,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "confidence": self.confidence,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class RiskLevel(str, enum.Enum):
    """Risk level enumeration."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NEGLIGIBLE = "negligible"


class ClauseRisk(Base):
    """Clause risk model for storing identified risks in clauses."""
    
    __tablename__ = "clause_risks"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    clause_id = Column(String(36), ForeignKey("clauses.id"), nullable=False)
    risk_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    level = Column(SQLAlchemyEnum(RiskLevel), nullable=False)
    impact = Column(Text, nullable=True)
    mitigation = Column(Text, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    clause = relationship("Clause", back_populates="risks")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert risk to dictionary."""
        return {
            "id": self.id,
            "clause_id": self.clause_id,
            "risk_type": self.risk_type,
            "description": self.description,
            "level": self.level,
            "impact": self.impact,
            "mitigation": self.mitigation,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
