#!/bin/bash
set -e

echo "==== Running FlashcardFactory in Docker ===="

# Build and start the container
docker compose up -d

echo ""
echo "FlashcardFactory is now running at http://localhost:8000"
echo ""
echo "To view logs: docker compose logs -f"
echo "To stop: docker compose down"
echo "=================================================" 