"""MCP Server for DocuMCP - Document Generation Service."""

import asyncio
from typing import Any, Dict, List, Optional

import structlog
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
)

from documcp.backend.domain.models import DocumentType, GenerationRequest
from documcp.backend.services.document_service import DocumentGenerationService
from documcp.backend.services.llm_service import LMStudioService

logger = structlog.get_logger(__name__)

# Global services
llm_service: Optional[LMStudioService] = None
document_service: Optional[DocumentGenerationService] = None

# Create MCP server
server = Server("documcp")


@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_documents",
            description="Generate project documentation (PRD, What-is-this, README) from a project description",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_text": {"type": "string", "description": "Project description or requirements"},
                    "project_name": {"type": "string", "description": "Name of the project (optional)"},
                    "document_types": {
                        "type": "array",
                        "items": {"type": "string", "enum": ["prd", "what_is_this", "readme"]},
                        "description": "Types of documents to generate (default: all types)",
                        "default": ["prd", "what_is_this", "readme"],
                    },
                },
                "required": ["input_text"],
            },
        ),
        Tool(
            name="generate_prd",
            description="Generate a Product Requirements Document (PRD) from project description",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_text": {"type": "string", "description": "Project description or requirements"},
                    "project_name": {"type": "string", "description": "Name of the project (optional)"},
                },
                "required": ["input_text"],
            },
        ),
        Tool(
            name="generate_readme",
            description="Generate a README.md file from project description",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_text": {"type": "string", "description": "Project description or requirements"},
                    "project_name": {"type": "string", "description": "Name of the project (optional)"},
                },
                "required": ["input_text"],
            },
        ),
        Tool(
            name="generate_overview",
            description="Generate a project overview (What-is-this) document from project description",
            inputSchema={
                "type": "object",
                "properties": {
                    "input_text": {"type": "string", "description": "Project description or requirements"},
                    "project_name": {"type": "string", "description": "Name of the project (optional)"},
                },
                "required": ["input_text"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    if not document_service:
        return [TextContent(type="text", text="Error: Document service not initialized")]

    try:
        if name == "generate_documents":
            return await _handle_generate_documents(arguments)
        elif name == "generate_prd":
            return await _handle_generate_single_document(arguments, DocumentType.PRD)
        elif name == "generate_readme":
            return await _handle_generate_single_document(arguments, DocumentType.README)
        elif name == "generate_overview":
            return await _handle_generate_single_document(arguments, DocumentType.WHAT_IS_THIS)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except Exception as e:
        logger.error("Error in tool call", tool=name, error=str(e))
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def _handle_generate_documents(arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle generate_documents tool call."""
    input_text = arguments.get("input_text", "")
    project_name = arguments.get("project_name")
    doc_types_str = arguments.get("document_types", ["prd", "what_is_this", "readme"])

    # Convert string document types to enum
    doc_types = []
    for dt_str in doc_types_str:
        if dt_str == "prd":
            doc_types.append(DocumentType.PRD)
        elif dt_str == "what_is_this":
            doc_types.append(DocumentType.WHAT_IS_THIS)
        elif dt_str == "readme":
            doc_types.append(DocumentType.README)

    request = GenerationRequest(input_text=input_text, document_types=doc_types, project_name=project_name)

    response = await document_service.generate_documents(request)

    results = []
    for doc in response.documents:
        doc_type_name = doc.document_type.value.replace("_", " ").title()
        results.append(TextContent(type="text", text=f"## {doc_type_name}\n\n{doc.content}\n\n---\n"))

    summary = f"Generated {len(response.documents)} documents in {response.generation_time:.2f} seconds"
    results.insert(0, TextContent(type="text", text=f"# Document Generation Complete\n\n{summary}\n\n"))

    return results


async def _handle_generate_single_document(arguments: Dict[str, Any], doc_type: DocumentType) -> List[TextContent]:
    """Handle single document generation tool calls."""
    input_text = arguments.get("input_text", "")
    project_name = arguments.get("project_name")

    request = GenerationRequest(input_text=input_text, document_types=[doc_type], project_name=project_name)

    response = await document_service.generate_documents(request)

    if response.documents:
        doc = response.documents[0]
        return [TextContent(type="text", text=doc.content)]
    else:
        return [TextContent(type="text", text="No document generated")]


@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List available prompts."""
    return [
        Prompt(
            name="project_documentation",
            description="Generate comprehensive project documentation including PRD, overview, and README",
            arguments=[
                PromptArgument(
                    name="project_description", description="Brief description of your project", required=True
                ),
                PromptArgument(name="project_name", description="Name of your project", required=False),
            ],
        ),
        Prompt(
            name="prd_template",
            description="Generate a Product Requirements Document template",
            arguments=[
                PromptArgument(
                    name="project_description", description="Project requirements and description", required=True
                ),
                PromptArgument(name="project_name", description="Name of your project", required=False),
            ],
        ),
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> GetPromptResult:
    """Handle prompt requests."""
    if name == "project_documentation":
        project_desc = arguments.get("project_description", "")
        project_name = arguments.get("project_name", "My Project")

        return GetPromptResult(
            description="Generate comprehensive project documentation",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please generate comprehensive documentation for my project '{project_name}'. "
                        f"Here's the project description: {project_desc}\n\n"
                        f"I need a complete set of documentation including:\n"
                        f"1. Product Requirements Document (PRD)\n"
                        f"2. Project Overview (What-is-this)\n"
                        f"3. README.md file\n\n"
                        f"Use the generate_documents tool to create all three document types.",
                    ),
                )
            ],
        )

    elif name == "prd_template":
        project_desc = arguments.get("project_description", "")
        project_name = arguments.get("project_name", "My Project")

        return GetPromptResult(
            description="Generate a Product Requirements Document",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=f"Please generate a Product Requirements Document for '{project_name}'. "
                        f"Project description: {project_desc}\n\n"
                        f"Use the generate_prd tool to create a comprehensive PRD.",
                    ),
                )
            ],
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


async def initialize_services():
    """Initialize the LLM and document services."""
    global llm_service, document_service

    logger.info("Initializing DocuMCP services...")

    try:
        # Initialize LM Studio service
        llm_service = LMStudioService()
        await llm_service.initialize()

        # Initialize document service
        document_service = DocumentGenerationService(llm_service)

        logger.info("DocuMCP services initialized successfully")

    except Exception as e:
        logger.error("Failed to initialize services", error=str(e))
        raise


async def main():
    """Main entry point for MCP server."""
    # Configure structured logging for MCP
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Initialize services
    await initialize_services()

    # Run MCP server
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="documcp",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(), experimental_capabilities={}
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
