#!/bin/bash
cd backend || exit 1
export PYTHONPATH=$(pwd)
poetry run ruff check --config ruff.toml .
