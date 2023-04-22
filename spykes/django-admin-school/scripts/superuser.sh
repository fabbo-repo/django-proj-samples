#!/bin/bash

cd ..

docker-compose up -d
docker exec -it django_admin_school python manage.py createsuperuser
#docker-compose down

cd -