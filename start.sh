#!/usr/bin/env bash
set -e



prefect agent local start &
uvicorn main:app --host 0.0.0.0 --port 8080 &

wait -n