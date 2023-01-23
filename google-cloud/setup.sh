#!/bin/bash

rm -r ./app
cp -r ../ProyectoWeb ./app
cp ./settings.py ./app/ProyectoWeb
cp ./entrypoint.sh ./app
cp ./Dockerfile ./app