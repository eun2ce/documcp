#!/usr/bin/env python3
"""
DocuMCP MCP Server startup script.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from documcp.backend.mcp_server import main

if __name__ == "__main__":
    # Set environment variables
    os.environ.setdefault("DOCUMCP_MODE", "development")

    # Run the MCP server
    asyncio.run(main())
