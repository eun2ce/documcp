"""Domain models for document generation."""

from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    """Supported document types."""

    PRD = "prd"
    WHAT_IS_THIS = "what_is_this"
    README = "readme"


class GenerationRequest(BaseModel):
    """Request model for document generation."""

    input_text: str = Field(..., description="Input project description")
    document_types: list[DocumentType] = Field(
        default=[DocumentType.PRD, DocumentType.WHAT_IS_THIS, DocumentType.README],
        description="Types of documents to generate",
    )
    project_name: Optional[str] = Field(None, description="Project name for context")
    additional_context: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional context for generation"
    )


class GeneratedDocument(BaseModel):
    """A single generated document."""

    document_type: DocumentType
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class GenerationResponse(BaseModel):
    """Response model for document generation."""

    documents: list[GeneratedDocument]
    generation_time: float = Field(..., description="Generation time in seconds")
    model_info: Dict[str, str] = Field(default_factory=dict)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    message: str
    model_loaded: bool = False
    memory_usage: Optional[Dict[str, float]] = None
