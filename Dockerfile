FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY arachne_mcp/ ./arachne_mcp/
COPY pyproject.toml .

# Install the package
RUN pip install --no-cache-dir -e .

# Default command
CMD ["python", "-m", "arachne_mcp"]
