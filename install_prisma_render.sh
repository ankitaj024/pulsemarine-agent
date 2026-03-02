#!/bin/bash
pip install -r requirements.txt
export PRISMA_CLI_QUERY_ENGINE_TYPE=binary
export PRISMA_CLIENT_ENGINE_TYPE=binary
export PRISMA_TARGET_DIR=/opt/render/project/src/
export PRISMA_EXPECTED_ENGINE_VERSION=393aa359c9ad4a4bb28630fb5613f9c281cde053
prisma py fetch
prisma generate
