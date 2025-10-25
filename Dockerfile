FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y \
    gcc \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Copy the FIXED nginx config
COPY Nginx/nginx.conf /etc/nginx/sites-available/default

# Create directories
RUN mkdir -p staticfiles media/projects

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate --noinput

EXPOSE 10000

# Start nginx and gunicorn
CMD service nginx start && gunicorn portfolio_project.wsgi:application --bind 127.0.0.1:8000