"""
Error handling module for ContractAI.

This module provides custom exception classes and error handlers.
"""

from typing import Dict, Any, Optional, List, Union
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

class AppError(Exception):
    """Base error class for application errors."""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
        
        # Log the error
        logger.error(
            f"{self.__class__.__name__}: {message}",
            extra={"details": self.details}
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for API response."""
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "details": self.details
        }
    
    def to_http_exception(self) -> HTTPException:
        """Convert to FastAPI HTTPException."""
        return HTTPException(
            status_code=self.status_code,
            detail=self.to_dict()
        )

class ValidationError(AppError):
    """Error raised when input validation fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )

class AuthenticationError(AppError):
    """Error raised when authentication fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            details=details
        )

class AuthorizationError(AppError):
    """Error raised when authorization fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            details=details
        )

class NotFoundError(AppError):
    """Error raised when a resource is not found."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details=details
        )

class LLMError(AppError):
    """Error raised when LLM API calls fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class DocumentProcessingError(AppError):
    """Error raised when document processing fails."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )

class DatabaseError(AppError):
    """Error raised when database operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )

class StorageError(AppError):
    """Error raised when storage operations fail."""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            details=details
        )
