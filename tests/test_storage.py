import pytest

from semi_secret.crypto import generate_key
from semi_secret.storage import SecretStorage


@pytest.fixture
def temp_storage(tmp_path):
    key = generate_key()
    salt = "test_salt_12345678"  # Fixed salt for testing
    return SecretStorage(key, salt, storage_path=tmp_path)


def test_set_get(temp_storage):
    temp_storage.set("test_key", "test_value")
    assert temp_storage.get("test_key") == "test_value"


def test_get_nonexistent(temp_storage):
    assert temp_storage.get("nonexistent") is None
    assert temp_storage.get("nonexistent", "default") == "default"


def test_delete(temp_storage):
    temp_storage.set("test_key", "test_value")
    temp_storage.delete("test_key")
    assert temp_storage.get("test_key") is None


def test_list_keys(temp_storage):
    temp_storage.set("key1", "value1")
    temp_storage.set("key2", "value2")
    keys = temp_storage.list_keys()
    assert sorted(keys) == ["key1", "key2"]


def test_persistence(tmp_path):
    key = generate_key()
    salt = "test_salt_12345678"  # Use a string instead of bytes

    # Create and store some data
    storage1 = SecretStorage(key, salt, storage_path=tmp_path)
    storage1.set("test_key", "test_value")

    # Create new instance with same key and path
    storage2 = SecretStorage(key, salt, storage_path=tmp_path)
    assert storage2.get("test_key") == "test_value"


def test_string_key_handling(tmp_path):
    """Test that string keys are properly handled or rejected"""
    string_key = "this-is-not-a-valid-key"  # Not a valid Fernet key
    salt = "test_salt_12345678"

    with pytest.raises(TypeError) as exc_info:
        SecretStorage(string_key, salt, storage_path=tmp_path)

    assert "key_material" in str(exc_info.value)


def test_valid_string_key(tmp_path):
    """Test that valid base64 string keys work properly"""
    valid_key = generate_key().decode()  # Convert bytes to string
    salt = "test_salt_12345678"

    # Should not raise any exception
    storage = SecretStorage(valid_key, salt, storage_path=tmp_path)
    storage.set("test", "value")
    assert storage.get("test") == "value"
