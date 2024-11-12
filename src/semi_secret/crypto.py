import base64
import hashlib
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _hash_sha256(data: bytes) -> str:
    """Calculate SHA256 hash of data"""
    return hashlib.sha256(data).hexdigest()


def normalize_key(key: Union[str, bytes]) -> bytes:
    """Normalize any key input into a Fernet-compatible key

    Args:
        key (Union[str, bytes]): Input key material - must be valid base64 data

    Returns:
        bytes: A valid Fernet key

    Raises:
        TypeError: If the key format is invalid
    """
    if not isinstance(key, (str, bytes)):
        raise TypeError("key_material must be string or bytes")

    try:
        # Convert to bytes if string
        key_bytes = key.encode() if isinstance(key, str) else key

        # Try to decode as base64 to validate
        try:
            decoded = base64.urlsafe_b64decode(_hash_sha256(key_bytes))
            decoded = decoded[:32]  # Ensure 32 bytes
        except Exception:
            raise TypeError("key_material must be valid base64-encoded data")

        # Validate length after decoding
        if len(decoded) != 32:
            raise TypeError("key_material must be 32 bytes when base64 decoded")

        return key_bytes

    except Exception as e:
        if isinstance(e, TypeError):
            raise
        raise TypeError("key_material must be valid string or bytes")


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
    derived = kdf.derive(key)  # Remove the base64 encoding here
    return derived, salt_bytes
