# Base Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python output immediately
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start application
CMD ["uvicorn", "web_main:app", "--host", "0.0.0.0", "--port", "8000"]