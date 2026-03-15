import base64
import hashlib
from cryptography.fernet import Fernet


def generate_key(master_password):
    password = master_password.encode()
    key = hashlib.sha256(password).digest()
    return base64.urlsafe_b64encode(key)


def encrypt_password(password, key):
    f = Fernet(key)
    encrypted = f.encrypt(password.encode())
    return encrypted.decode()


def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted_password.encode())
    return decrypted.decode()