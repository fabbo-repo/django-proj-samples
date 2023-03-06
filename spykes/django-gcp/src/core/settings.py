from pathlib import Path
from configurations import Configuration
import os
import io
from django.contrib.messages import constants as err_msg
import environ
import google.auth
from google.cloud import secretmanager

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(
    APP_DEBUG=(bool, os.getenv("APP_DEBUG", default=True)),
    APP_SECRET_KEY=(str, os.getenv("APP_SECRET_KEY", 
        default=os.urandom(34).hex())),
    APP_CSRF_TRUSTED_ORIGINS=(str, os.getenv("APP_CSRF_TRUSTED_ORIGINS")),
    DATABASE_URL=(str, os.getenv("DATABASE_URL", 
        default='sqlite:///'+os.path.join(BASE_DIR, 'default.sqlite3'))),
    GS_BUCKET_NAME=(str, os.getenv("GS_BUCKET_NAME")),
)

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

# If a Proxy is used then the secret manager service won't be used
if os.getenv("GOOGLE_CLOUD_PROJECT", None) and not os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.getenv("SETTINGS_NAME", "django_app_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode(
        "UTF-8"
    )
    env.read_env(io.StringIO(payload))


class Dev(Configuration):

    SECRET_KEY = os.urandom(34).hex()

    # True by default but have the option to set it false with an environment variable
    DEBUG = env('APP_DEBUG')

    ALLOWED_HOSTS = [ '*' ]
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
        'axes',
        'crispy_forms',
        'core',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'axes.middleware.AxesMiddleware',
    ]

    ROOT_URLCONF = 'core.urls'

    CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

    LOGIN_REDIRECT_URL = "/admin"

    AUTHENTICATION_BACKENDS = [
        # AxesStandaloneBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
        'axes.backends.AxesStandaloneBackend',

        # Django ModelBackend is the default authentication backend.
        'django.contrib.auth.backends.ModelBackend',
    ]

    # Inactivity period for failed login attempts (hours)
    AXES_COOLOFF_TIME = 24
    
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
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'core.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/4.1/ref/settings/#databases
    DATABASES = {"default": env.db()}
    # If the flag as been set, configure to use proxy
    if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
        DATABASES["default"]["HOST"] = "cloudsql-proxy"
        DATABASES["default"]["PORT"] = 5432


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
    if not env("GS_BUCKET_NAME"):
        STATIC_ROOT = BASE_DIR / "static"

    MEDIA_URL = 'media/'

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

    if env("GS_BUCKET_NAME"):
        STATICFILES_DIRS = []
        GS_BUCKET_NAME = env("GS_BUCKET_NAME")
        DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        # Allow django-admin collectstatic to automatically put static files in GC bucket
        STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        # "publicRead" to return a public url, non-expiring url. All other files return a signed (expiring) url.
        GS_DEFAULT_ACL = "publicRead"
        # Note:
        # GOOGLE_APPLICATION_CREDENTIALS env is needed for JSON credentials path
        # it is automatically fetched


class Prod(Dev):
    DEBUG = False
    
    SECRET_KEY = env('APP_SECRET_KEY')
    DATABASES = {"default": env.db()}
    if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
        DATABASES["default"]["HOST"] = "cloudsql-proxy"
        DATABASES["default"]["PORT"] = 5432
    ALLOWED_HOSTS = [ '*' ]
    if env("APP_CSRF_TRUSTED_ORIGINS"):
        CSRF_TRUSTED_ORIGINS = env("APP_CSRF_TRUSTED_ORIGINS").split(',')
    else:
        CSRF_TRUSTED_ORIGINS = [ 'https://*.run.app', 'https://*.com' ]
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
            "level": "ERROR",
        }
    }