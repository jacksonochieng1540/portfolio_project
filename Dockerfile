FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False
ENV PORT=10000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p static staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 10000

# Run the application - FIXED THIS LINE
CMD ["gunicorn", "portfolio_project.wsgi:application", "--bind", "0.0.0.0:10000"]