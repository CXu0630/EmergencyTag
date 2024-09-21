from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
from dotenv import load_dotenv

def load_encryption_key():
    """
    Loads the encryption key from environment variables.

    :return: bytes (encryption key)
    """
    load_dotenv()  # Load variables from .env
    encryption_key = os.getenv('ENCRYPTION_KEY')

    if encryption_key is None:
        raise ValueError("ENCRYPTION_KEY is not set in the environment variables.")

    # Ensure the key is 32 bytes for AES-256
    if len(encryption_key) < 32:
        # Pad the key with zeros if it's shorter than 32 bytes
        encryption_key = encryption_key.ljust(32, '0')
    elif len(encryption_key) > 32:
        # Truncate the key if it's longer than 32 bytes
        encryption_key = encryption_key[:32]

    return encryption_key.encode('utf-8')  # Convert to bytes

def gen_nonce():
    return os.urandom(16)

def aes_ctr_encrypt_keyed(key, nonce, plaintext):
    """
    Encrypts plaintext using AES-CTR.

    :param key: 32-byte AES key
    :param nonce: 16-byte nonce
    :param plaintext: bytes
    :return: ciphertext as bytes
    """
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
    return ciphertext

def aes_ctr_decrypt_keyed(key, nonce, ciphertext):
    """
    Decrypts ciphertext using AES-CTR.

    :param key: 32-byte AES key
    :param nonce: 16-byte nonce
    :param ciphertext: bytes
    :return: plaintext as bytes
    """
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode('utf-8')

def aes_ctr_encrypt(nonce, plaintext):
    key = load_encryption_key()
    return aes_ctr_encrypt_keyed(key, nonce, plaintext)

def aes_ctr_decrypt(nonce, cipher):
    key = load_encryption_key()
    return aes_ctr_decrypt_keyed(key, nonce, cipher)