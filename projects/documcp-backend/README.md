# DocuMCP Backend

Document generation API using Qwen3-4B-Instruct for creating PRD, What-is-this, and README documents from project descriptions.

## Features

- 🚀 **Fast Document Generation**: Generate multiple document types in ≤ 5 seconds
- 🤖 **Qwen3-4B-Instruct**: Powered by state-of-the-art language model
- 📝 **Multiple Templates**: PRD, What-is-this, README document types
- 🔄 **Concurrent Generation**: Generate multiple documents simultaneously
- 📊 **Monitoring**: Built-in health checks and Prometheus metrics
- 🐳 **Docker Ready**: Complete containerization support

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager (recommended) or pip
- 8GB+ RAM (for model loading)
- CUDA-compatible GPU (optional, for faster inference)

### Installation

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd DocuMCP/projects/documcp-backend
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Set environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**:
   ```bash
   python run.py
   ```

   Or with UV:
   ```bash
   uv run uvicorn documcp.backend.main:app --reload
   ```

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**:
   ```bash
   docker build -t documcp-backend .
   docker run -p 8000:8000 documcp-backend
   ```

## Usage

### MCP Server (Recommended)

DocuMCP can be used as an MCP (Model Context Protocol) server with Claude Desktop or other MCP clients:

1. **Start LM Studio** with a loaded model on `localhost:1234`

2. **Configure Claude Desktop**:
   - Copy the MCP configuration from `mcp_config.json`
   - Update the path to match your installation directory
   - Add to your Claude Desktop MCP settings

3. **Use in Claude**:
   ```
   Use the generate_documents tool to create documentation for my React app project
   ```

### Available MCP Tools

- `generate_documents` - Generate all document types (PRD, overview, README)
- `generate_prd` - Generate only Product Requirements Document
- `generate_readme` - Generate only README.md
- `generate_overview` - Generate only project overview

### REST API Usage

#### Generate Documents

```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "A web application for managing project documentation with AI-powered generation",
    "document_types": ["prd", "what_is_this", "readme"],
    "project_name": "DocuMCP"
  }'
```

#### Health Check

```bash
curl "http://localhost:8000/api/v1/health"
```

#### Metrics

```bash
curl "http://localhost:8000/api/v1/metrics"
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Document Types

### PRD (Product Requirements Document)
- Comprehensive project requirements
- Technical specifications
- System architecture overview
- Risk assessment

### What-is-this
- Project vision and overview
- Core value proposition  
- Target users and use cases
- Success metrics

### README
- Installation instructions
- Usage examples
- API documentation
- Development setup

## Configuration

Key environment variables:

```bash
# Application
DOCUMCP_MODE=development|production

# Model settings
QWEN_MODEL_NAME=Qwen/Qwen2.5-4B-Instruct
QWEN_DEVICE_MAP=auto
QWEN_TORCH_DTYPE=float16

# API settings
DOCUMCP_FASTAPI__TITLE="DocuMCP API"
DOCUMCP_CORS__ALLOW_ORIGINS=["http://localhost:3000"]
```

## Development

### Project Structure

```
src/documcp/backend/
├── api/                 # API endpoints
│   └── generation.py   # Document generation routes  
├── domain/             # Domain models
│   └── models.py      # Request/response models
├── services/          # Business logic
│   ├── llm_service.py      # Qwen model integration
│   └── document_service.py # Document generation
├── main.py           # FastAPI application
└── settings.py       # Configuration
```

### Running Tests

```bash
uv run pytest
```

### Code Quality

```bash
# Linting
uv run ruff check

# Formatting  
uv run ruff format
```

## Performance

- **Latency**: ≤ 5s p95 for document generation
- **Memory**: 4-8GB RAM required for model
- **Concurrency**: Supports multiple concurrent requests
- **GPU**: Optional CUDA acceleration for faster inference

## Monitoring

- **Health endpoint**: `/api/v1/health`
- **Metrics endpoint**: `/api/v1/metrics`
- **Structured logging**: JSON format with correlation IDs
- **Prometheus**: Built-in metrics export

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.