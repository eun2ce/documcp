"""LLM service for document generation using LM Studio."""

import time
from typing import Dict, Optional

import httpx
import structlog

from documcp.backend.domain.models import DocumentType

logger = structlog.get_logger(__name__)


class LMStudioService:
    """Service for handling LLM operations with LM Studio."""

    def __init__(self, base_url: str = "http://localhost:1234", model_name: str = "local-model"):
        self.base_url = base_url.rstrip("/")
        self.model_name = model_name
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 minute timeout
        self._model_loaded = False

    async def initialize(self) -> None:
        """Initialize connection to LM Studio."""
        logger.info("Initializing LM Studio connection", base_url=self.base_url)

        try:
            # Test connection to LM Studio
            response = await self.client.get(f"{self.base_url}/v1/models")

            if response.status_code == 200:
                models_data = response.json()
                available_models = [model["id"] for model in models_data.get("data", [])]

                if available_models:
                    # Use the first available model if our default isn't found
                    if self.model_name not in available_models:
                        self.model_name = available_models[0]
                        logger.info("Using available model", model_name=self.model_name)

                    self._model_loaded = True
                    logger.info("LM Studio connection established", available_models=available_models)
                else:
                    logger.error("No models loaded in LM Studio")
                    raise RuntimeError("No models loaded in LM Studio")
            else:
                logger.error("Failed to connect to LM Studio", status_code=response.status_code)
                raise RuntimeError(f"Failed to connect to LM Studio: {response.status_code}")

        except httpx.ConnectError:
            logger.error("Cannot connect to LM Studio. Make sure LM Studio is running on", url=self.base_url)
            raise RuntimeError(f"Cannot connect to LM Studio at {self.base_url}")
        except Exception as e:
            logger.error("Failed to initialize LM Studio connection", error=str(e))
            raise

    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model_loaded

    def get_model_info(self) -> Dict[str, str]:
        """Get model information."""
        return {
            "model_name": self.model_name,
            "loaded": str(self.is_loaded),
            "service": "LM Studio",
            "base_url": self.base_url,
        }

    def _get_generation_prompt(
        self, input_text: str, document_type: DocumentType, project_name: Optional[str] = None
    ) -> str:
        """Generate prompt for specific document type."""

        prompts = {
            DocumentType.PRD: self._get_prd_prompt,
            DocumentType.WHAT_IS_THIS: self._get_what_is_this_prompt,
            DocumentType.README: self._get_readme_prompt,
        }

        return prompts[document_type](input_text, project_name)

    def _get_prd_prompt(self, input_text: str, project_name: Optional[str] = None) -> str:
        """Generate PRD prompt."""
        project_context = f"for project '{project_name}'" if project_name else ""

        return f"""You are a senior product manager. Create a comprehensive Product Requirements Document (PRD) {project_context} based on the following description.

Project Description:
{input_text}

Create a well-structured PRD with the following sections:
1. Overview
2. Goals & Objectives
3. System Context
4. Functional Requirements
5. Non-Functional Requirements
6. Deployment
7. Extensibility
8. Risks & Mitigation

Use clear, professional language and include specific technical details where appropriate. Format the output as Markdown.

PRD:"""

    def _get_what_is_this_prompt(self, input_text: str, project_name: Optional[str] = None) -> str:
        """Generate What-is-this prompt."""
        project_context = f"called '{project_name}'" if project_name else ""

        return f"""You are a technical writer. Create an engaging "What is this" overview document {project_context} based on the following description.

Project Description:
{input_text}

Create a compelling overview with the following sections:
1. Vision (what this project aims to achieve)
2. Core Value (why it matters, what problems it solves)
3. Key Features (main capabilities)
4. Target Users (who will use this)
5. Tech Snapshot (high-level technical overview)
6. Roadmap (future plans)
7. Success Metrics

Use an engaging, accessible tone while maintaining technical accuracy. Format the output as Markdown.

What is this:"""

    def _get_readme_prompt(self, input_text: str, project_name: Optional[str] = None) -> str:
        """Generate README prompt."""
        project_context = f"# {project_name}\n\n" if project_name else ""

        return f"""You are a developer writing documentation. Create a comprehensive README.md {project_context}based on the following description.

Project Description:
{input_text}

Create a helpful README with the following sections:
1. Project title and brief description
2. Features
3. Installation instructions
4. Usage examples
5. API documentation (if applicable)
6. Configuration
7. Development setup
8. Contributing guidelines
9. License

Use clear, developer-friendly language with practical examples. Format the output as Markdown.

README:"""

    async def generate_document(
        self,
        input_text: str,
        document_type: DocumentType,
        project_name: Optional[str] = None,
        max_length: int = 2048,
        temperature: float = 0.7,
    ) -> str:
        """Generate a document using LM Studio."""
        if not self.is_loaded:
            raise RuntimeError("LM Studio not connected. Call initialize() first.")

        start_time = time.time()
        prompt = self._get_generation_prompt(input_text, document_type, project_name)

        try:
            # Call LM Studio API
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_length,
                    "temperature": temperature,
                    "stream": False,
                },
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                result_data = response.json()
                generated_text = result_data["choices"][0]["message"]["content"]

                generation_time = time.time() - start_time
                logger.info(
                    "Document generated successfully",
                    document_type=document_type.value,
                    generation_time=generation_time,
                    output_length=len(generated_text),
                )

                return generated_text.strip()
            else:
                error_msg = f"LM Studio API error: {response.status_code}"
                logger.error("Error during text generation", error=error_msg, response_text=response.text)
                raise RuntimeError(error_msg)

        except Exception as e:
            logger.error("Error during text generation", error=str(e))
            raise

    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage information."""
        return {"service": "LM Studio", "local_service": True, "memory_info": "Managed by LM Studio"}
