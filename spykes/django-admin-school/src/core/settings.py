from pathlib import Path
from configurations import Configuration
import os
import environ
from django.utils.translation import gettext_lazy as _
from django.core.management.utils import get_random_secret_key
from cryptography.fernet import Fernet

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    APP_DEBUG=(bool, os.getenv("APP_DEBUG", default=True)),
    APP_ALLOWED_HOSTS=(str, os.getenv("APP_ALLOWED_HOSTS", default='*')),
    APP_CORS_HOSTS=(str, os.getenv("APP_CORS_HOSTS")),
    DATABASE_URL=(str, os.getenv(
        "DATABASE_URL",
        default='sqlite:///'+os.path.join(BASE_DIR, 'default.sqlite3'))),
    APP_EMAIL_HOST=(str, os.getenv(
        "APP_EMAIL_HOST", default='smtp.gmail.com')),
    APP_EMAIL_PORT=(int, os.getenv("APP_EMAIL_PORT", default=587)),
    APP_EMAIL_HOST_USER=(str, os.getenv(
        "APP_EMAIL_HOST_USER", default='example@gmail.com')),
    APP_EMAIL_HOST_PASSWORD=(str, os.getenv(
        "APP_EMAIL_HOST_PASSWORD", default='password')),
    APP_CELERY_BROKER_URL=(str, os.getenv(
        "APP_CELERY_BROKER_URL", default="redis://localhost:6379/0")),
)


class Dev(Configuration):

    DEBUG = env('APP_DEBUG')
    
    # SECRET key setup
    secret_key_file = os.path.join(BASE_DIR, 'secret.key')
    if os.path.exists(secret_key_file):
        print("* Using SECRET key from file")
        with open(secret_key_file, 'r') as reader:
            SECRET_KEY = reader.read()
    else:
        print("* Generating SECRET key")
        SECRET_KEY = get_random_secret_key()
        with open(secret_key_file, 'w') as writer:
            print("* Generating SECRET key file")
            writer.write(SECRET_KEY)
    # FERNET key setup
    fernet_key_file = os.path.join(BASE_DIR, 'fernet.key')
    if os.path.exists(fernet_key_file):
        print("* Using FERNET key from file")
        with open(fernet_key_file, 'r') as reader:
            FERNET_KEY = reader.read()
    else:
        print("* Generating FERNET key")
        FERNET_KEY = Fernet.generate_key().decode('utf-8')
        with open(fernet_key_file, 'w') as writer:
            print("* Generating FERNET key file")
            writer.write(FERNET_KEY)

    ALLOWED_HOSTS = env('APP_ALLOWED_HOSTS').split(',')
    if env('APP_CORS_HOSTS'):
        CORS_ALLOW_ALL_ORIGINS = False
        CORS_ALLOWED_ORIGINS = env('APP_CORS_HOSTS').split(',')
    else:
        CORS_ALLOW_ALL_ORIGINS = True

    X_FRAME_OPTIONS = 'DENY'

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Cors
        'corsheaders',
        # Extra templates components
        'crispy_forms',
        # Django axes
        'axes',
        # Custom apps
        'core',
        'user',
        'practices',
        'vacations',
        'agencies',
    ]

    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'axes.middleware.AxesMiddleware',
    ]

    ROOT_URLCONF = 'core.urls'

    # CSRF error template view render
    CSRF_FAILURE_VIEW = 'core.views.csrf_failure'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

    AUTH_USER_MODEL = "user.AppUser"

    AUTHENTICATION_BACKENDS = [
        # AxesStandaloneBackend should be the first backend.
        # (Brute force auth prevention)
        'axes.backends.AxesStandaloneBackend',

        # Django ModelBackend is the default authentication backend.
        'django.contrib.auth.backends.ModelBackend',
    ]

    # AXES setup
    AXES_ENABLED = True
    AXES_FAILURE_LIMIT = 5
    AXES_RESET_ON_SUCCESS = True
    AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True
    # Inactivity period for failed login attempts (hours)
    AXES_COOLOFF_TIME = 24

    WSGI_APPLICATION = 'core.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    DATABASES = {"default": env.db()}

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/4.0/topics/i18n/
    LANGUAGE_CODE = 'en'
    LOCALE_PATHS = [
        BASE_DIR / 'locale/',
    ]
    LANGUAGES = (
        ('en', _('English')),
        ('es', _('Spanish')),
    )
    TIME_ZONE = "UTC"
    # Enables Django’s translation system
    USE_I18N = True
    # Django will display numbers and dates using the format of the current locale
    USE_L10N = True
    # Datetimes will be timezone-aware
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / "static"
    # Media files (Videos, Images)
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / "media"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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

    # Template pack for django crispy application
    CRISPY_TEMPLATE_PACK = 'bootstrap4'

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
