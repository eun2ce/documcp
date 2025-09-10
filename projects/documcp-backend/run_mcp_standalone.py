#!/usr/bin/env python3
"""
DocuMCP Standalone MCP Server - 모든 종속성을 포함한 독립형 실행 파일
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# 환경 변수 설정
os.environ.setdefault("DOCUMCP_MODE", "development")
os.environ.setdefault("DOCUMCP_LM_STUDIO__BASE_URL", "http://localhost:1234")
os.environ.setdefault("DOCUMCP_LM_STUDIO__MODEL_NAME", "local-model")


# 종속성 검사 및 설치
def check_and_install_dependencies():
    """필요한 종속성을 확인하고 설치"""
    try:
        import httpx
        import mcp
        import structlog
    except ImportError as e:
        print(f"Error: Missing dependency {e.name}", file=sys.stderr)
        print("Please install dependencies with: pip install mcp httpx structlog", file=sys.stderr)
        sys.exit(1)


def main():
    """메인 함수"""
    check_and_install_dependencies()

    try:
        from documcp.backend.mcp_server import main as mcp_main

        asyncio.run(mcp_main())
    except ImportError as e:
        print(f"Error importing MCP server: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
