FROM python:3.11-slim

LABEL maintainer="jozrftamson"
LABEL description="Figma MCP Server - Model Context Protocol integration for Figma API"
LABEL version="1.0.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml README.md LICENSE ./
COPY figma_mcp/ ./figma_mcp/
COPY tests/ ./tests/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Create non-root user
RUN useradd -m -u 1000 figma && chown -R figma:figma /app
USER figma

# Environment variables
ENV FIGMA_API_TOKEN=""
ENV MCP_LOG_LEVEL="INFO"
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import figma_mcp; print('healthy')" || exit 1

# Default command
CMD ["python", "-m", "figma_mcp.server"]
