#!/bin/bash

# Activar el entorno virtual
source venv/bin/activate

# Configurar variables de entorno para Flask
export FLASK_APP=app/app.py
export FLASK_DEBUG=1

# Lanzar el servidor Flask con cProfile y guardar el reporte en un archivo
python -m cProfile -o ./cprofile/results.pstats $(which flask) run
