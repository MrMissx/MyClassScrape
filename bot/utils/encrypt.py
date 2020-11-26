from cryptography.fernet import Fernet

from bot import KEY


f = Fernet(KEY)


def encrypt(text: str):
    """text(str) return a byte"""
    b_str = text.encode("utf-8")
    return f.encrypt(b_str)


def decrypt(enc: bytes):
    """enc(bytes) return a string"""
    return f.decrypt(enc).decode("utf-8")
