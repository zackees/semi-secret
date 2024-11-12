# semi-secret
A secure key-value storage utility with command-line interface

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

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
