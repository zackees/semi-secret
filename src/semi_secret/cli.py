import click
from pathlib import Path
from .crypto import generate_key, derive_key
from .storage import SecretStorage

@click.group()
def main():
    """Semi-secret storage utility"""
    pass

@main.command()
@click.option('--storage-path', type=click.Path(), help='Storage location')
def init(storage_path):
    """Initialize a new secret storage with a random key"""
    key = generate_key()
    path = Path(storage_path) if storage_path else None
    
    # Create storage with the new key
    storage = SecretStorage(key, storage_path=path)
    
    # Save the key in the storage directory
    key_file = storage.storage_path / 'key'
    key_file.write_bytes(key)
    click.echo(f"Initialized storage with new key at {key_file}")

@main.command()
@click.argument('key')
@click.argument('value')
@click.option('--storage-path', type=click.Path(), help='Storage location')
def set(key, value, storage_path):
    """Store a secret value"""
    path = Path(storage_path) if storage_path else None
    storage_dir = path or Path.home() / '.semi_secret'
    key_file = storage_dir / 'key'
    
    if not key_file.exists():
        click.echo("Storage not initialized. Run 'semi-secret init' first.")
        return
    
    storage = SecretStorage(key_file.read_bytes(), storage_path=path)
    storage.set(key, value)
    click.echo(f"Stored value for key '{key}'")

@main.command()
@click.argument('key')
@click.option('--storage-path', type=click.Path(), help='Storage location')
def get(key, storage_path):
    """Retrieve a secret value"""
    path = Path(storage_path) if storage_path else None
    key_file = (path or Path.home() / '.semi_secret') / 'key'
    
    if not key_file.exists():
        click.echo("Storage not initialized. Run 'semi-secret init' first.")
        return
    
    storage = SecretStorage(key_file.read_bytes(), storage_path=path)
    value = storage.get(key)
    if value is None:
        click.echo(f"No value found for key '{key}'")
    else:
        click.echo(value)

@main.command()
@click.option('--storage-path', type=click.Path(), help='Storage location')
def list(storage_path):
    """List all stored keys"""
    path = Path(storage_path) if storage_path else None
    key_file = (path or Path.home() / '.semi_secret') / 'key'
    
    if not key_file.exists():
        click.echo("Storage not initialized. Run 'semi-secret init' first.")
        return
    
    storage = SecretStorage(key_file.read_bytes(), storage_path=path)
    keys = storage.list_keys()
    if not keys:
        click.echo("No secrets stored")
    else:
        click.echo("\n".join(keys))

if __name__ == '__main__':
    main()
