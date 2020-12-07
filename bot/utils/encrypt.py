"""Encrypt and Decrypt."""

from cryptography.fernet import Fernet

from bot import KEY


f = Fernet(KEY)


def encrypt(text: str) -> bytes:
    """Encrypt any string."""
    b_str = text.encode("utf-8")
    return f.encrypt(b_str)


def decrypt(enc: bytes) -> str:
    """decrypt any encrypted string."""
    return f.decrypt(enc).decode("utf-8")
