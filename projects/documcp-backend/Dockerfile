# DocuMCP Backend Dockerfile
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN pip install uv

# Set work directory
WORKDIR /app

# Copy workspace files
COPY pyproject.toml ./
COPY features/ ./features/
COPY projects/documcp-backend/ ./projects/documcp-backend/

# Install dependencies
RUN cd projects/documcp-backend && \
    uv sync --no-dev

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start command
CMD ["uv", "run", "--directory", "projects/documcp-backend", "uvicorn", "documcp.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
