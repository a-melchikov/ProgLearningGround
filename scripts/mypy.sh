#!/bin/bash
cd backend || exit 1
export PYTHONPATH=$(pwd)
poetry run mypy app --config-file mypy.ini
