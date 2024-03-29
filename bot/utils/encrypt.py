"""Encrypt and Decrypt."""

from cryptography.fernet import Fernet

from bot import KEY

F = Fernet(KEY)


def encrypt(text: str) -> bytes:
    """Encrypt any string."""
    b_str = text.encode("utf-8")
    return F.encrypt(b_str)


def decrypt(enc: bytes) -> str:
    """decrypt any encrypted string."""
    return F.decrypt(enc).decode("utf-8")
