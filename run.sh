#!/bin/bash
PROJECT_DIR=$(dirname "$BASH_SOURCE")

export PYTHONPATH="$PROJECT_DIR/lib"

set -o allexport
source "$PROJECT_DIR/.pyenv"
set +o allexport

python3 "$@"