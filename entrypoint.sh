#!/bin/bash

# Wait for PostgreSQL to be available
echo "Waiting for PostgreSQL to be available..."
until nc -z -v -w30 $DATABASE_HOST $DATABASE_PORT
do
  echo "Waiting for PostgreSQL connection..."
  sleep 1
done

echo "PostgreSQL is up! Applying migrations..."

# Apply migrations using Alembic (or any other migration tool you're using)
alembic upgrade head

# Start FastAPI server
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
