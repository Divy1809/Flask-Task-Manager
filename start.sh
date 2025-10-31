#!/bin/bash
# Startup script for Flask Task Manager application

set -e

echo "Starting Flask Task Manager Application..."

# Create data directory if it doesn't exist
mkdir -p /data

# Set database path to persistent volume
export SQLALCHEMY_DATABASE_URI="sqlite:////data/tasks.db"

# Production mode settings
export FLASK_ENV=production
export PYTHONUNBUFFERED=1

# Start application with Gunicorn production server
echo "Initializing database..."
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

echo "Starting Gunicorn server on port ${PORT:-5000}..."
exec gunicorn \
    --bind 0.0.0.0:${PORT:-5000} \
    --workers 4 \
    --threads 2 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    "app.main:app"
