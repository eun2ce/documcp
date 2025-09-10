# DocuMCP

![Image](https://github.com/user-attachments/assets/54276f4d-7836-4995-a29a-035fbe5ae97a)

> **Intelligent Document Generation with Model Context Protocol (MCP)**

DocuMCP is a powerful FastAPI-based document generation service that integrates seamlessly with Claude Desktop through the Model Context Protocol (MCP). Generate comprehensive project documentation including Product Requirements Documents (PRDs), project overviews, and README files using local LLM models via LM Studio.

## 🌟 Features

- **🤖 AI-Powered Document Generation**: Generate PRDs, project overviews, and README files from simple project descriptions
- **🔌 MCP Integration**: Native support for Claude Desktop through Model Context Protocol
- **🏠 Local LLM Support**: Works with LM Studio for privacy-focused, offline document generation
- **⚡ FastAPI Backend**: Modern, async Python backend with clean architecture
- **🛠️ Multiple Document Types**: Support for various documentation formats
- **📋 Template-Based Generation**: Consistent, professional document structure

## 🚀 Quick Start

### Prerequisites

Before getting started, ensure you have:

- **Python 3.12+**: Required for running DocuMCP
- **UV Package Manager**: Recommended for dependency management
- **LM Studio**: For local LLM model execution
- **Claude Desktop**: MCP client for seamless integration

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd DocuMCP

# Install dependencies
cd projects/documcp-backend
uv sync
```

### 2. LM Studio Setup

1. **Download and Install LM Studio**
   - Visit [LM Studio](https://lmstudio.ai/) and download for your platform

2. **Download a Compatible Model**
   - Recommended models: Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct
   - Choose based on your hardware capabilities

3. **Start Local Server**
   - Load your chosen model in LM Studio
   - Start the local server (default: `localhost:1234`)

### 3. Claude Desktop MCP Configuration

#### Configuration File Location

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

#### Configuration Content

```json
{
  "mcpServers": {
    "documcp": {
      "command": "/Users/yourusername/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/path/to/DocuMCP/projects/documcp-backend",
        "python",
        "run_mcp.py"
      ],
      "env": {
        "DOCUMCP_MODE": "development",
        "DOCUMCP_LM_STUDIO__BASE_URL": "http://localhost:1234",
        "DOCUMCP_LM_STUDIO__MODEL_NAME": "local-model"
      }
    }
  }
}
```

**Important**: Replace `/path/to/DocuMCP` with your actual project path.

### 4. Start Using DocuMCP

1. **Restart Claude Desktop** completely after saving the configuration
2. **Verify Connection** by checking if DocuMCP tools appear in Claude Desktop
3. **Generate Documents** using natural language requests

## 📖 Usage Guide

### Basic Document Generation

Ask Claude to generate comprehensive documentation:

```
Generate project documentation for:

Project Name: "TaskMaster"
Description: "A React web application for task management featuring drag-and-drop functionality, priority settings, and team collaboration features."

Please use the generate_documents tool to create PRD, project overview, and README files.
```

### Single Document Generation

For specific document types:

```
Create a README.md file for an "AI-powered image analysis service" using the generate_readme tool.
```

### Available Tools

- **`generate_documents`**: Creates all document types (PRD + Overview + README)
- **`generate_prd`**: Generates Product Requirements Document only
- **`generate_readme`**: Creates README.md file only
- **`generate_overview`**: Generates project overview (What-is-this) document only

## 🔧 Advanced Configuration

### Environment Variables

Customize DocuMCP behavior with environment variables:

```json
{
  "mcpServers": {
    "documcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/documcp", "python", "run_mcp.py"],
      "env": {
        "DOCUMCP_MODE": "production",
        "DOCUMCP_LM_STUDIO__BASE_URL": "http://192.168.1.100:1234",
        "DOCUMCP_LM_STUDIO__MODEL_NAME": "my-custom-model",
        "DOCUMCP_LM_STUDIO__TIMEOUT": "600"
      }
    }
  }
}
```

### Custom LM Studio Port

If LM Studio runs on a different port:

```json
"DOCUMCP_LM_STUDIO__BASE_URL": "http://localhost:8080"
```

### Development Mode

For development and testing, run the FastAPI server directly:

```bash
cd projects/documcp-backend
uvicorn documcp.backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

```
DocuMCP/
├── features/                           # Shared kernel modules
│   ├── documcp-shared_kernel/
│   ├── documcp-shared_kernel-infra-fastapi/
│   └── documcp-shared-kernel-infra-database-sqla/
├── projects/                           # Main applications
│   └── documcp-backend/               # FastAPI backend service
│       ├── src/documcp/backend/       # Source code
│       │   ├── api/                   # FastAPI routes
│       │   ├── services/              # Business logic
│       │   ├── domain/                # Domain models
│       │   └── mcp_server.py          # MCP server implementation
│       ├── run_mcp.py                 # MCP server entry point
│       └── run.py                     # FastAPI server entry point
├── mcp_config.json                    # Sample MCP configuration
└── README.md                          # This file
```

## 🐛 Troubleshooting

### Common Issues

#### "Document service not initialized" Error
- **Check LM Studio**: Ensure LM Studio is running and model is loaded
- **Verify Connection**: Test connection to `http://localhost:1234`
- **Check Network**: Ensure no firewall blocking local connections

#### Tools Not Visible in Claude Desktop
- **Restart Claude Desktop**: Completely quit and reopen the application
- **Verify Configuration**: Check file path and JSON syntax
- **Check Permissions**: Ensure UV and Python are accessible

#### Python Path Errors
- **Install UV**: Ensure UV package manager is installed
- **Verify Paths**: Double-check all paths in configuration file
- **Check Permissions**: Ensure execution permissions are set

### Debug Mode

Run MCP server manually to check for errors:

```bash
cd projects/documcp-backend
python run_mcp.py
```

### Manual Testing

Test the REST API before MCP integration:

```bash
# Start FastAPI server
python run.py

# Test document generation
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{"input_text": "Test project description", "project_name": "TestApp"}'
```

## 💡 Best Practices

### Effective Prompts

1. **Be Specific**: Instead of "mobile app", use "iOS/Android food delivery app with real-time order tracking and payment integration"

2. **Include Tech Stack**: "React, Node.js, MongoDB-based real-time chat application"

3. **Define Target Users**: "Task management tool for small business teams"

### Document Quality Tips

- Provide clear project names
- Emphasize key features and differentiators  
- Separate business goals from technical requirements
- Include relevant constraints and assumptions

## 🔗 Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [LM Studio Download](https://lmstudio.ai/)
- [Claude Desktop](https://claude.ai/desktop)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

If you encounter any issues, please report them on GitHub Issues with the following information:

- Operating system and version
- Python version
- LM Studio version
- Error messages
- Configuration file content (excluding sensitive information)

---

**Created with ❤️ by eun2ce | 2025-09-10**
