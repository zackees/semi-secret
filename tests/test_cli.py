"""
Unit test file.
"""

import unittest

from click.testing import CliRunner

from semi_secret.cli import main


class MainTester(unittest.TestCase):
    """Main tester class."""

    def setUp(self):
        pass  # We don't need temp_dir setup anymore

    def test_help(self):
        """Test help command."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        self.assertEqual(0, result.exit_code)

    def test_store_and_load(self):
        """Test storing and loading values."""
        runner = CliRunner()
        store_cmd = [
            "--store",
            "test_salt=test_key=test_value",
        ]
        result = runner.invoke(main, store_cmd)
        self.assertEqual(0, result.exit_code)

        load_cmd = [
            "--load",
            "test_salt=test_key",
        ]
        result = runner.invoke(main, load_cmd)
        self.assertEqual(0, result.exit_code)
        self.assertIn("test_value", result.output)


if __name__ == "__main__":
    unittest.main()
