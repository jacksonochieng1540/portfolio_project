FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

WORKDIR /app

# Install only necessary dependencies (no nginx)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Create directories
RUN mkdir -p staticfiles media/projects

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate --noinput

EXPOSE 10000

# Simple gunicorn command to run the app
CMD gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:$PORT