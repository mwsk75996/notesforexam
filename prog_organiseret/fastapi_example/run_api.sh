#!/usr/bin/env sh
set -eu

if [ -x ".venv/bin/fastapi" ]; then
    exec .venv/bin/fastapi dev main.py
fi

exec fastapi dev main.py
