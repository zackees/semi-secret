import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_key() -> bytes:
    """Generate a new random key"""
    return Fernet.generate_key()


def derive_key(salt: str, key: bytes) -> tuple[bytes, bytes]:
    """Derive a final key using salt and initial key

    Args:
        salt (str): Salt string for key derivation
        key (bytes): Initial key bytes

    Returns:
        tuple[bytes, bytes]: (derived key, salt used)
    """
    salt_bytes = salt.encode()[:16].ljust(16, b"\0")  # Ensure 16 byte salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt_bytes,
        iterations=100000,
    )
    derived = base64.urlsafe_b64encode(kdf.derive(key))
    return derived, salt_bytes


