from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_key() -> bytes:
    """Generate a new random key"""
    return Fernet.generate_key()

def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]:
    """Derive a key from a password using PBKDF2"""
    if salt is None:
        salt = Fernet.generate_key()[:16]  # Use first 16 bytes as salt
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt
