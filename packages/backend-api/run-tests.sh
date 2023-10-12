#!/bin/bash

# Prepare virtual env
source venv/bin/activate
export PYTHONPATH=$(pwd):$PYTHONPATH

# Run tests 
pytest -s --color=yes --verbose --cov=app --cov-report=term-missing

# Desactiva el entorno virtual al finalizar
deactivate
