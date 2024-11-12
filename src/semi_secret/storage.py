import json
from pathlib import Path
from typing import Any, Optional
from cryptography.fernet import Fernet

class SecretStorage:
    """Secure key-value storage using Fernet encryption.
    
    Args:
        key (bytes): The encryption key (must be a valid Fernet key)
        storage_path (Optional[Path]): Custom path for storing encrypted data. 
                                     Defaults to ~/.semi_secret/
    """
    def __init__(self, key: bytes, storage_path: Optional[Path] = None):
        self.fernet = Fernet(key)
        self.storage_path = storage_path or Path.home() / '.semi_secret'
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._data = {}
        self._load()

    def _load(self):
        """Load encrypted data from storage"""
        storage_file = self.storage_path / 'secrets.enc'
        if storage_file.exists():
            encrypted_data = storage_file.read_bytes()
            try:
                decrypted_data = self.fernet.decrypt(encrypted_data)
                self._data = json.loads(decrypted_data)
            except Exception:
                self._data = {}

    def _save(self):
        """Save encrypted data to storage"""
        storage_file = self.storage_path / 'secrets.enc'
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
