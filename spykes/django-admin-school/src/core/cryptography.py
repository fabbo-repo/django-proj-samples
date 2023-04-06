from cryptography.fernet import Fernet
import base64
from django.conf import settings


def encrypt_data(data):
    key = settings.FERNET_KEY.encode('utf-8')
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode('utf-8'))
    return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')


def decrypt_data(encrypted_data):
    key = settings.FERNET_KEY.encode('utf-8')
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(
        base64.urlsafe_b64decode(encrypted_data.encode('utf-8')))
    return decrypted_data.decode('utf-8')
