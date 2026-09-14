#!/bin/bash
#set -e

#echo "Running database migrations..."
#cd /app/models/db_schemes/minirag/
#alembic upgrade head

#cd /app

#exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4











#!/bin/bash
set -e

if [ "$1" = "uvicorn" ] || [ -z "$1" ]; then
  echo "Running database migrations..."
  cd /app/models/db_schemes/minirag/
  alembic upgrade head
  cd /app
fi

if [ -z "$1" ]; then
  exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
else
  exec "$@"
fi