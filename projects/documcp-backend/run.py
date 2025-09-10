#!/usr/bin/env python3
"""
DocuMCP Backend startup script.
"""

import os
import sys
from pathlib import Path

import uvicorn

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault("DOCUMCP_MODE", "development")

    # Run the application
    uvicorn.run(
        "documcp.backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )
