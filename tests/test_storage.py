import pytest
from pathlib import Path
from semi_secret.storage import SecretStorage
from semi_secret.crypto import generate_key

@pytest.fixture
def temp_storage(tmp_path):
    key = generate_key()
    return SecretStorage(key, storage_path=tmp_path)

def test_set_get(temp_storage):
    temp_storage.set('test_key', 'test_value')
    assert temp_storage.get('test_key') == 'test_value'

def test_get_nonexistent(temp_storage):
    assert temp_storage.get('nonexistent') is None
    assert temp_storage.get('nonexistent', 'default') == 'default'

def test_delete(temp_storage):
    temp_storage.set('test_key', 'test_value')
    temp_storage.delete('test_key')
    assert temp_storage.get('test_key') is None

def test_list_keys(temp_storage):
    temp_storage.set('key1', 'value1')
    temp_storage.set('key2', 'value2')
    keys = temp_storage.list_keys()
    assert sorted(keys) == ['key1', 'key2']

def test_persistence(tmp_path):
    key = generate_key()
    
    # Create and store some data
    storage1 = SecretStorage(key, storage_path=tmp_path)
    storage1.set('test_key', 'test_value')
    
    # Create new instance with same key and path
    storage2 = SecretStorage(key, storage_path=tmp_path)
    assert storage2.get('test_key') == 'test_value'
