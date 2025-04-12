FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

RUN chmod 1777 /tmp
# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt requirements.txt
COPY . .
# Install Python dependencies

FROM base AS development

RUN pip install -r requirements.txt
# Expose the port the app runs on
EXPOSE 3000
# Run the application
CMD ["uvicorn" , "main:app" , "--host" , "0.0.0.0" , "--port", "3000" , "--reload"]