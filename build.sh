#!/usr/bin/env bash
# ======================================================
# BattleRoster Heroku Build Script
# Automates setup, migrations, and static file handling
# ======================================================

echo "Starting BattleRoster build setup..."

# Exit immediately if a command fails
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete! Ready for launch."
