#!/bin/sh

# Exit immediately if any of the following command exits 
# with a non-zero status
set -e

# Create log directory
touch /var/log/app/app.log
chmod 777 /var/log/app/app.log

# Call collectstatic
python manage.py collectstatic --noinput

# Execute database migrations
if  python manage.py migrate --check; then
    echo Migrations applied
else
    echo Applying migrations
    python manage.py migrate --noinput
fi

# Create superuser
if  python manage.py createsuperuser --no-input; then
    echo Superuser created
else
    echo Superuser already created, skipping
fi

APP_USER_UID=`id -u $APP_USER`
exec uwsgi --uid=$APP_USER_UID --http-auto-chunked --http-keepalive --ini app.uwsgi.ini "$@"