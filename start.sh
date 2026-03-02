#!/bin/bash
echo "Fetching Prisma binaries at runtime..."
export PRISMA_TARGET_DIR=/opt/render/project/src/
export PRISMA_CLI_QUERY_ENGINE_TYPE=binary
export PRISMA_CLIENT_ENGINE_TYPE=binary
prisma py fetch

echo "Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
