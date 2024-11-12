"""
Unit test file.
"""

import unittest
from pathlib import Path

from appdirs import user_config_dir  # type: ignore
from click.testing import CliRunner

from semi_secret import SecretStorage
from semi_secret.cli import main

# Create a proper Fernet-compatible key for testing
STORAGE_KEY = (
    "YWljb2RlX29wZW5haV9jb25maWdfMzJieXRlc19sb25nX2tleQ=="  # base64-encoded 32-byte key
)
SALT = "aicode_salt"  # We should use a consistent salt for the storage

STORAGE_PATH = Path(user_config_dir("advanced-aicode", roaming=True))


class MainTester(unittest.TestCase):
    """Main tester class."""

    def setUp(self):
        """Set up test environment."""
        self.runner = CliRunner()
        self.storage = SecretStorage(STORAGE_KEY, SALT, STORAGE_PATH)
        # Clean up any existing test data
        if STORAGE_PATH.exists():
            for key in self.storage.list_keys():
                self.storage.delete(key)

    def tearDown(self):
        """Clean up after tests."""
        if STORAGE_PATH.exists():
            for key in self.storage.list_keys():
                self.storage.delete(key)

    def test_store_and_load(self):
        """Test storing and loading secrets."""
        test_key = "test_key"
        test_value = "test_value"

        # Test storing
        result = self.runner.invoke(
            main, ["--store", f"test_salt={test_key}={test_value}"]
        )
        self.assertEqual(result.exit_code, 0)

        # Test loading
        result = self.runner.invoke(main, ["--load", f"test_salt={test_key}"])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output.strip(), test_value)

    def test_storage_direct(self):
        """Test direct storage operations."""
        test_key = "direct_test"
        test_value = "direct_value"

        # Test setting value
        self.storage.set(test_key, test_value)

        # Test getting value
        retrieved_value = self.storage.get(test_key)
        self.assertEqual(retrieved_value, test_value)

        # Test listing keys
        keys = self.storage.list_keys()
        self.assertIn(test_key, keys)

        # Test deleting
        self.storage.delete(test_key)
        self.assertNotIn(test_key, self.storage.list_keys())


if __name__ == "__main__":
    unittest.main()
