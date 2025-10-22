#!/usr/bin/env bash

set -o errexit


pip install -r requirements.txt


python manage.py migrate

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput


