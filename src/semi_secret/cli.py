import hashlib
from pathlib import Path

import click

from .storage import SecretStorage

# Default storage location in user's home directory
DEFAULT_STORAGE_PATH = Path.home() / ".semi_secret"
# Create default storage directory if it doesn't exist
DEFAULT_STORAGE_PATH.mkdir(parents=True, exist_ok=True)


# Constants for consistent storage
STORAGE_KEY = "aicode_openai_config"
SALT = "aicode_salt"


@click.command()
@click.option("--store", help="Store a secret in salt=key=value format")
@click.option("--load", help="Load a secret by key")
def main(store, load):
    """Semi-secret storage utility"""
    if store:
        try:
            salt, rest = store.split("=", 1)
            key, value = rest.split("=", 1)
            # Derive a proper length key from the salt
            derived_key = hashlib.sha256(salt.encode()).hexdigest()
            storage = SecretStorage(derived_key, salt, DEFAULT_STORAGE_PATH)
            storage.set(key, value)
            click.echo(f"Stored value for key '{key}'")
        except ValueError:
            click.echo("Error: --store must be in format 'salt=key=value'", err=True)
            return 1
        except Exception as e:
            click.echo(f"Error storing value: {str(e)}", err=True)
            return 1

    elif load:
        try:
            salt, key = load.split("=", 1)
            # Use same key derivation as store
            derived_key = hashlib.sha256(salt.encode()).hexdigest()
            storage = SecretStorage(derived_key, salt, DEFAULT_STORAGE_PATH)
            value = storage.get(key)
            if value is None:
                click.echo(f"No value found for key '{key}'")
            else:
                click.echo(value)
        except ValueError:
            click.echo("Error: --load must be in format 'salt=key'", err=True)
            return 1
        except Exception as e:
            click.echo(f"Error loading value: {str(e)}", err=True)
            return 1

    return 0


if __name__ == "__main__":
    main()
