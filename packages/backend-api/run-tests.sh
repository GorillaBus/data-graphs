#!/bin/bash

# Activa tu entorno virtual
source venv/bin/activate

# Ejecuta los tests
pytest --color=yes --verbose --cov=app --cov-report=term-missing -n 4

# Desactiva el entorno virtual al finalizar
deactivate
