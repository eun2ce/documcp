"""Document generation service."""

import asyncio
import time
from typing import Any, Dict, Optional

import structlog

from documcp.backend.domain.models import DocumentType, GeneratedDocument, GenerationRequest, GenerationResponse
from documcp.backend.services.llm_service import LMStudioService

logger = structlog.get_logger(__name__)


class DocumentGenerationService:
    """Service for generating documents using LLM."""

    def __init__(self, llm_service: LMStudioService):
        self.llm_service = llm_service

    async def generate_documents(self, request: GenerationRequest) -> GenerationResponse:
        """Generate multiple documents based on request."""
        start_time = time.time()

        logger.info(
            "Starting document generation",
            document_types=[dt.value for dt in request.document_types],
            project_name=request.project_name,
            input_length=len(request.input_text),
        )

        # Generate documents concurrently
        tasks = []
        for doc_type in request.document_types:
            task = self._generate_single_document(
                request.input_text, doc_type, request.project_name, request.additional_context
            )
            tasks.append(task)

        # Wait for all documents to be generated
        generated_docs = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and handle any exceptions
        successful_docs = []
        for i, result in enumerate(generated_docs):
            if isinstance(result, Exception):
                doc_type = request.document_types[i]
                logger.error("Failed to generate document", document_type=doc_type.value, error=str(result))
                # Create error document
                error_doc = GeneratedDocument(
                    document_type=doc_type,
                    content=f"# Error\n\nFailed to generate {doc_type.value}: {str(result)}",
                    metadata={"error": True, "error_message": str(result)},
                )
                successful_docs.append(error_doc)
            else:
                successful_docs.append(result)

        generation_time = time.time() - start_time

        logger.info(
            "Document generation completed", total_documents=len(successful_docs), generation_time=generation_time
        )

        return GenerationResponse(
            documents=successful_docs, generation_time=generation_time, model_info=self.llm_service.get_model_info()
        )

    async def _generate_single_document(
        self,
        input_text: str,
        document_type: DocumentType,
        project_name: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> GeneratedDocument:
        """Generate a single document."""

        logger.info("Generating document", document_type=document_type.value)

        try:
            # Generate content using LLM
            content = await self.llm_service.generate_document(
                input_text=input_text,
                document_type=document_type,
                project_name=project_name,
                max_length=self._get_max_length_for_type(document_type),
                temperature=self._get_temperature_for_type(document_type),
            )

            # Create metadata
            metadata = {
                "generated_at": time.time(),
                "project_name": project_name,
                "input_length": len(input_text),
                "output_length": len(content),
                "model": self.llm_service.model_name,
            }

            if additional_context:
                metadata.update(additional_context)

            return GeneratedDocument(document_type=document_type, content=content, metadata=metadata)

        except Exception as e:
            logger.error("Error generating document", document_type=document_type.value, error=str(e))
            raise

    def _get_max_length_for_type(self, document_type: DocumentType) -> int:
        """Get appropriate max length for document type."""
        length_map = {DocumentType.PRD: 3000, DocumentType.WHAT_IS_THIS: 2500, DocumentType.README: 2000}
        return length_map.get(document_type, 2048)

    def _get_temperature_for_type(self, document_type: DocumentType) -> float:
        """Get appropriate temperature for document type."""
        temp_map = {
            DocumentType.PRD: 0.3,  # More structured/factual
            DocumentType.WHAT_IS_THIS: 0.7,  # More creative
            DocumentType.README: 0.5,  # Balanced
        }
        return temp_map.get(document_type, 0.7)
