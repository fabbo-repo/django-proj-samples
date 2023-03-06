import os
from configurations.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

application = get_asgi_application()
