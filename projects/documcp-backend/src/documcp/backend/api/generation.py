"""Document generation API endpoints."""

from typing import Any, Dict

import structlog
from fastapi import APIRouter, Depends, HTTPException

from documcp.backend.domain.models import GenerationRequest, GenerationResponse, HealthResponse
from documcp.backend.services.document_service import DocumentGenerationService
from documcp.backend.services.llm_service import LMStudioService

logger = structlog.get_logger(__name__)

router = APIRouter()

# Global service instances (will be initialized in main.py)
llm_service: LMStudioService = None  # type: ignore
document_service: DocumentGenerationService = None  # type: ignore


def get_document_service() -> DocumentGenerationService:
    """Dependency to get document service."""
    if document_service is None:
        raise HTTPException(status_code=503, detail="Document service not initialized")
    return document_service


def get_llm_service() -> LMStudioService:
    """Dependency to get LLM service."""
    if llm_service is None:
        raise HTTPException(status_code=503, detail="LLM service not initialized")
    return llm_service


@router.post("/generate", response_model=GenerationResponse)
async def generate_documents(
    request: GenerationRequest, doc_service: DocumentGenerationService = Depends(get_document_service)
) -> GenerationResponse:
    """Generate documents based on input text."""

    try:
        logger.info(
            "Received generation request",
            document_types=[dt.value for dt in request.document_types],
            project_name=request.project_name,
            input_length=len(request.input_text),
        )

        # Validate input
        if not request.input_text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty")

        if len(request.input_text) > 10000:  # 10KB limit
            raise HTTPException(status_code=400, detail="Input text too long (max 10,000 characters)")

        # Generate documents
        response = await doc_service.generate_documents(request)

        logger.info(
            "Generation completed successfully",
            documents_generated=len(response.documents),
            generation_time=response.generation_time,
        )

        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error during generation", error=str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check(llm_svc: LMStudioService = Depends(get_llm_service)) -> HealthResponse:
    """Health check endpoint."""

    try:
        model_loaded = llm_svc.is_loaded
        memory_usage = llm_svc.get_memory_usage() if model_loaded else None

        status = "healthy" if model_loaded else "model_not_loaded"
        message = (
            "DocuMCP is running and model is loaded" if model_loaded else "DocuMCP is running but model is not loaded"
        )

        return HealthResponse(status=status, message=message, model_loaded=model_loaded, memory_usage=memory_usage)

    except Exception as e:
        logger.error("Error in health check", error=str(e))
        return HealthResponse(status="error", message=f"Health check failed: {str(e)}", model_loaded=False)


@router.get("/metrics")
async def metrics(llm_svc: LMStudioService = Depends(get_llm_service)) -> Dict[str, Any]:
    """Prometheus-style metrics endpoint."""

    try:
        model_info = llm_svc.get_model_info()
        memory_usage = llm_svc.get_memory_usage()

        metrics = {
            "model_loaded": 1 if llm_svc.is_loaded else 0,
            "model_info": model_info,
        }

        if memory_usage:
            metrics.update(
                {
                    "memory_allocated_gb": memory_usage.get("allocated_gb", 0),
                    "memory_reserved_gb": memory_usage.get("reserved_gb", 0),
                    "memory_max_allocated_gb": memory_usage.get("max_allocated_gb", 0),
                }
            )

        return metrics

    except Exception as e:
        logger.error("Error getting metrics", error=str(e))
        return {"error": str(e)}


async def initialize_services():
    """Initialize global services."""
    global llm_service, document_service

    logger.info("Initializing services...")

    # Initialize LLM service
    llm_service = LMStudioService()
    await llm_service.initialize()

    # Initialize document service
    document_service = DocumentGenerationService(llm_service)

    logger.info("Services initialized successfully")
