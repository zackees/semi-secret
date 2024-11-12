import click

from .storage import SecretStorage


@click.command()
@click.option("--store", help="Store a secret in salt=key=value format")
@click.option("--load", help="Load a secret in salt=key format")
def main(store, load):
    """Semi-secret storage utility"""
    if store:
        try:
            salt, rest = store.split("=", 1)
            key, value = rest.split("=", 1)
            storage = SecretStorage(salt.encode(), salt)
            storage.set(key, value)
            click.echo(f"Stored value for key '{key}'")
        except ValueError:
            click.echo("Error: --store must be in format 'salt=key=value'")
            return

    elif load:
        try:
            salt, key = load.split("=", 1)
            storage = SecretStorage(salt.encode(), salt)
            value = storage.get(key)
            if value is None:
                click.echo(f"No value found for key '{key}'")
            else:
                click.echo(value)
        except ValueError:
            click.echo("Error: --load must be in format 'salt=key'")
            return


if __name__ == "__main__":
    main()
