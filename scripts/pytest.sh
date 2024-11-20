#!/bin/bash
cd backend || exit 1
export PYTHONPATH=$(pwd)
poetry run pytest tests --maxfail=1 --disable-warnings
