# semi-secret
A secure key-value storage utility with command-line interface

[![Linting](https://github.com/zackees/semi-secret/actions/workflows/lint.yml/badge.svg)](https://github.com/zackees/semi-secret/actions/workflows/lint.yml) 

[![macOS Tests](https://github.com/zackees/semi-secret/actions/workflows/test_macos.yml/badge.svg)](https://github.com/zackees/semi-secret/actions/workflows/test_macos.yml)
[![Ubuntu Tests](https://github.com/zackees/semi-secret/actions/workflows/test_ubuntu.yml/badge.svg)](https://github.com/zackees/semi-secret/actions/workflows/test_ubuntu.yml)
[![Windows Tests](https://github.com/zackees/semi-secret/actions/workflows/test_win.yml/badge.svg)](https://github.com/zackees/semi-secret/actions/workflows/test_win.yml)
## Installation

```bash
pip install semi-secret
```

## Usage

Store a secret:
```bash
semi-secret --store "mysalt=mykey=myvalue"
```

Retrieve a secret:
```bash
semi-secret --load "mysalt=mykey"
```

## Development

To set up the development environment:
```bash
. ./activate.sh
```

### Windows

This environment requires you to use `git-bash`.

### Linting

Run `./lint.sh` to check code quality using `pylint`, `flake8` and `mypy`.

## Security

This tool uses Fernet encryption (from the cryptography package) with PBKDF2 key derivation to securely store your data. Data is stored encrypted in `~/.semi_secret/secrets.enc`.

## Releases

  * 1.0.2 - Improve usage so that any arbitrary string can be used as the salt
  * 1.0.1 - Usage fixes from the inclusion in `advanced-aicode`
  * 1.0.0 - Initial release