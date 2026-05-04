FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Create a group and non-root user and ensure non-root user has access
RUN groupadd --gid 1183 devgroup && useradd --uid 1183 --gid devgroup --shell /bin/bash --create-home devuser && \
    mkdir /app && \
    chown -R devuser:devgroup /app

# Turn interactive prompts off
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for postgres client and other packages
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Selective copy
COPY body /app/body
COPY core /app/core
COPY intro /app/intro
COPY link /app/link
COPY static /app/static
COPY portfolio_ws_project /app/portfolio_ws_project
COPY manage.py /app/
COPY .env /app/

# Switch to non-root user
USER devuser

# Expose port 8080 for the Django development server
EXPOSE 8080

# Command to run the application (will be overridden by docker-compose in most cases)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "16", "--timeout", "0", "portfolio_ws_project.wsgi:application"]

