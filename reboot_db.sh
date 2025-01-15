#!/bin/bash

# Script para hacer un reboot de la base de datos con alembic
# Se debe ejecutar en el directorio root
cd db || { echo "No se encuentra el directorio db"; exit 1; }

echo "Comenzando el downgrade DB"
alembic downgrade base
if [ $? -ne 0 ]; then
    echo "Error al hacer downgrade"
    exit 1
fi

echo "Comenzando el upgrade DB"
alembic upgrade head
if [ $? -ne 0 ]; then
    echo "Error al hacer upgrade"
    exit 1
fi

cd .. || { echo "No se encuentra el directorio raiz"; exit 1; }

echo "Reboot finalizado"