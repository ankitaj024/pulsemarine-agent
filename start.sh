#!/bin/bash
# Remove variables that might cause issues with Prisma expecting different paths
unset PRISMA_TARGET_DIR
unset PRISMA_CLI_QUERY_ENGINE_TYPE
unset PRISMA_CLIENT_ENGINE_TYPE

echo "Fetching Prisma binaries at runtime natively..."
prisma py fetch

echo "Generating Prisma Client..."
prisma generate

echo "Starting Uvicorn..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
