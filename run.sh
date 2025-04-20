#!/bin/bash
PROJECT_DIR=$(dirname "$BASH_SOURCE")

export PYTHONPATH="$PROJECT_DIR/lib"

python3 "$1"