#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -e



# Install Python dependencies from requirements.txt
pip install -r requirements.txt


# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

