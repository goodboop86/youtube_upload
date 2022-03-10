#!/usr/bin/env bash
set -e

# prefect ENV
export PREFECT__LOGGING__LEVEL="INFO"
export PREFECT__LOGGING__FORMAT="[%(asctime)s] %(levelname)s - %(name)s | %(message)s"

echo echo $GOOGLEDRIVE_ACCESS_TOKEN

prefect agent local start &
uvicorn main:app --host 0.0.0.0 --port 8080 --reload --reload-exclude '*.json' &

wait -n