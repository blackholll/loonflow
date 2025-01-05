import os
import base64
from django.conf import settings
from service.base_service import BaseService
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class EncryptService(BaseService):
    @classmethod
    def encrypt(cls, data:str)->str:
        """
        AES encrypt
        """
        encrypt_key = settings.ENCRYPTION_KEY
        iv = os.urandom(16)
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode()) + padder.finalize()
        cipher = Cipher(algorithms.AES(base64.b64decode(encrypt_key)), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(iv).decode('utf-8') +',' + base64.b64encode(encrypted_data).decode('utf-8')

    @classmethod
    def decrypt(cls, data:str)->str:
        encrypt_key = settings.ENCRYPTION_KEY
        iv = base64.b64decode(data.split(',')[0])
        encrypted_data = base64.b64decode(data.split(',')[1])
        cipher = Cipher(algorithms.AES(base64.b64decode(encrypt_key)), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        return data.decode()


