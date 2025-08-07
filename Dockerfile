
# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipx
RUN pip install pipx
RUN pipx ensurepath

# Copy the entire project
COPY . .

# Install the package in development mode if setup.py/pyproject.toml exists
# This ensures the MCP server dependencies are available
RUN pip install -e .

# Set environment variables (these will be overridden by docker run or compose)
ENV GOOGLE_EMAIL=""
ENV GOOGLE_MASTER_TOKEN=""
ENV UNSAFE_MODE="false"
ENV PYTHONPATH="/app"

# Expose port (adjust if your MCP server uses a specific port)
EXPOSE 8000

# Default command - runs the MCP server using pipx
CMD ["pipx", "run", "--no-cache", "--spec", ".", "mcp"]
