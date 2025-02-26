FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install necessary build tools
RUN apt update && apt install -y gcc && rm -rf /var/lib/apt/lists/*

# copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

# Stage 2: Final Image
FROM python:3.11-slim

WORKDIR /app

# copy installed packages from the builder stage
COPY --from=builder /usr/local /usr/local 

# set hugging face cache directory outside the container
ENV TRANSFORMERS_CACHE=/models

# copy the application
COPY . .

ENV PYTHONPATH="/app"
# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]