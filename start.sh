#!/bin/bash
# Fetch Prisma binaries at runtime since Render clears the cache directory after build
echo "Fetching Prisma binaries at runtime..."
prisma py fetch

# Start the FastAPI application
echo "Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
