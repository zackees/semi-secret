import base64
import json
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet

from .crypto import derive_key


class SecretStorage:
    """Secure key-value storage using Fernet encryption.

    Args:
        key (Union[bytes, str]): The encryption key (must be a valid Fernet key or string)
        salt (str): Salt value used for key derivation
        storage_path (Path): Path for storing encrypted data
    """

    def __init__(self, key: bytes | str, salt: str, storage_path: Path):
        """Initialize storage with key and salt

        Args:
            key (Union[bytes, str]): The encryption key (must be a valid Fernet key or string)
            salt (str): Salt value used for key derivation
            storage_path (Path): Path for storing encrypted data
        """
        # Convert key to bytes if it's a string
        if isinstance(key, str):
            try:
                # First try to decode the string as base64
                key_bytes = base64.urlsafe_b64decode(key)
                # Then verify it's the right length for a Fernet key
                if len(key_bytes) != 32:
                    raise ValueError("Invalid key length")
                key = key.encode()  # Only encode after validation
            except Exception as e:
                raise TypeError(
                    "Invalid key_material: must be valid base64-encoded Fernet key"
                ) from e
        elif not isinstance(key, bytes):
            raise TypeError("key must be string or bytes")

        derived_key, _ = derive_key(salt, key)  # Use the salt to derive the final key
        self.fernet = Fernet(derived_key)
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._data: dict[str, Any] = {}
        self._load()

    def _load(self):
        """Load encrypted data from storage"""
        storage_file = self.storage_path / "secrets.enc"
        if storage_file.exists():
            encrypted_data = storage_file.read_bytes()
            try:
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self._data = json.loads(decrypted_data)
            except Exception:
                self._data = {}

    def _save(self):
        """Save encrypted data to storage"""
        storage_file = self.storage_path / "secrets.enc"
        encrypted_data = self.fernet.encrypt(json.dumps(self._data).encode())
        storage_file.write_bytes(encrypted_data)

    def set(self, key: str, value: Any):
        """Store a value"""
        self._data[key] = value
        self._save()

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value"""
        return self._data.get(key, default)

    def delete(self, key: str):
        """Delete a value"""
        if key in self._data:
            del self._data[key]
            self._save()

    def list_keys(self) -> list[str]:
        """List all stored keys"""
        return list(self._data.keys())
