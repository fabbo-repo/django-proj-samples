FROM python:3.10-slim

# Create a group and user to run our app
ENV APP_USER=django-user
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

COPY ./requirements.txt /requirements.txt
COPY ./src /app
WORKDIR /app

RUN ls -l /app
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

USER ${APP_USER}:${APP_USER}

# Gunicorn as app server
CMD exec gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 core.wsgi:application
