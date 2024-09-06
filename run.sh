#!/bin/bash

# Stop the script if any command fails
set -e

# Delete older .pyc files
find . -type f -name "*.pyc" -exec rm -f {} \;

# Set the Flask app environment variable
export FLASK_APP=core/server.py

# Run required migrations (if you have migrations configured)
# Uncomment the following lines if you need to run migrations
# flask db init -d core/migrations/
# flask db migrate -m "Initial migration." -d core/migrations/
# flask db upgrade -d core/migrations/

# Run the server using gunicorn
gunicorn -c gunicorn_config.py core.server:app
