#!/usr/bin/env bash
set -e
echo "Starting on port: $PORT"
exec gunicorn main:app \
  --workers 1 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind "0.0.0.0:$PORT" \
  --timeout 120 \
  --log-level info
