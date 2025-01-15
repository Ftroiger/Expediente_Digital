#!/bin/bash

# Ejecutar el gateway en el puerto 8000
echo "Iniciando el Gateway en el puerto 8000..."
uvicorn gateway.src.gateway:app --host 0.0.0.0 --port 8000 --reload &

# Ejecutar servicios en el puerto 8001
echo "Iniciando todos los servicios en el puerto 8001..."
uvicorn routers.main:app --host 0.0.0.0 --port 8001 --reload --timeout-keep-alive 15 &

# Esperar a que todos los procesos terminen
wait