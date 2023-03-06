#!/bin/bash
set -e

cd ../ProyectoWeb
echo "Initializing proxy..."
docker compose up -d
sleep 3
echo "Creating super user..."
read -p "Username: " username
read -p "Email: " email
read -p "Password: " password
docker compose run --rm app sh -c "export DJANGO_SUPERUSER_PASSWORD=${password}; export DJANGO_SUPERUSER_USERNAME=${username}; export DJANGO_SUPERUSER_EMAIL=${email}; python manage.py createsuperuser --noinput"
echo "Destrying proxy..."
docker compose down