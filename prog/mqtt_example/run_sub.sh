#!/usr/bin/env sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SUB_SRC="$SCRIPT_DIR/src/subscriber.cpp"

if [ ! -s "$SUB_SRC" ]; then
  echo "subscriber.cpp is empty. Add code before running."
  exit 1
fi

cmake -S "$SCRIPT_DIR" -B "$SCRIPT_DIR/build"
cmake --build "$SCRIPT_DIR/build" --target subscriber
"$SCRIPT_DIR/build/subscriber"
