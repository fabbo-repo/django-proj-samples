from pathlib import Path
from configurations import Configuration
import os
import dj_database_url
from django.contrib.messages import constants as err_msg

def get_env(environ_name, default_value=None):
    return os.environ.get(environ_name) or default_value

def get_int_env(environ_name, default_value=None):
    return int(os.environ.get(environ_name) or default_value)

def get_bool_env(environ_name, default_value=None):
    if not os.environ.get(environ_name): return default_value
    if os.environ.get(environ_name).lower() in ['true', '1', 't', 'y', 'yes']: return True
    return False

def get_list_env(environ_name, default_value=None):
    if not os.environ.get(environ_name): return default_value
    return os.environ.get(environ_name).split(',')

class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    SECRET_KEY = os.urandom(34).hex()

    # True by default but have the option to set it false with an environment variable
    DEBUG = get_bool_env('APP_DEBUG', True)

    ALLOWED_HOSTS = [ '*' ]
    CORS_ALLOW_ALL_ORIGINS = True
    # X_FRAME_OPTIONS = 'ALLOW-FROM ' + os.environ.get('HOSTNAME')
    # CSRF_COOKIE_SAMESITE = None
    # CSRF_TRUSTED_ORIGINS = [os.environ.get('HOSTNAME')]
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SAMESITE = 'None'
    # SESSION_COOKIE_SAMESITE = 'None'

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Custom Apps:
        'ProyectoWebApp',
        'servicios',
        'blog',
        'contacto',
        'tienda',
        'cesta_tienda',
        'autenticacion',
        'crispy_forms'
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'ProyectoWeb.urls'
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'cesta_tienda.context_processor.importe_total_cesta'
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'ProyectoWeb.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases

    # conn_max_age is the lifetime of a database connection in seconds
    DATABASES = {'default': dj_database_url.config(
        default='sqlite:///'+os.path.join(BASE_DIR, 'default.sqlite3'),
        conn_max_age=600
    )}


    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]


    # Internationalization
    # https://docs.djangoproject.com/en/4.1/topics/i18n/
    LANGUAGE_CODE = 'es-eu'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.1/howto/static-files/

    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    # CONFIG to messages tags
    MESSAGE_TAGS={
        err_msg.DEBUG: 'debug',
        err_msg.INFO: 'info',
        err_msg.SUCCESS: 'success',
        err_msg.WARNING: 'warning',
        err_msg.ERROR: 'danger',
    }

    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        }
    }

    CRISPY_TEMPLATE_PACK='bootstrap4'


class Prod(Dev):
    DEBUG = False
    
    SECRET_KEY = get_env('APP_SECRET_KEY', os.urandom(34).hex())
    ALLOWED_HOSTS = get_list_env('APP_ALLOWED_HOSTS', 
        [ "localhost", "0.0.0.0" ])
    if get_list_env("APP_CORS_ALLOWED_HOSTS"):
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOWED_ORIGINS = get_list_env("APP_CORS_ALLOWED_HOSTS")
    CSRF_TRUSTED_ORIGINS = get_list_env("APP_CORS_ALLOWED_HOSTS", 
        [ "http://localhost:8000", "http://127.0.0.1:8000" ]
    )
    
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "logfile": {
                "class": "logging.FileHandler",
                "filename": "/var/log/app/app.log",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["logfile"],
            "level": "ERROR",
        }
    }