#!/usr/bin/env sh
set -eu

if [ -x ".venv/bin/python" ]; then
    exec .venv/bin/python testclients.py
fi

exec python3 testclients.py
