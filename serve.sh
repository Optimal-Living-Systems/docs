#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source .venv/bin/activate
exec mkdocs serve -a 0.0.0.0:8000
