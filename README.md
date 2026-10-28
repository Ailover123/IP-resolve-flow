# IP Resolve Flow

`IP Resolve Flow` is a Python command-line tool that resolves a hostname to
its unique IP addresses.

The project currently provides:

- Hostname validation
- IPv4 and IPv6 address resolution
- IDNA-compatible hostname handling
- Clear errors for invalid input and DNS failures
- Logging for successful and failed resolution attempts
- A command-line interface

## Requirements

- Python 3.14 or newer
- [`uv`](https://docs.astral.sh/uv/)
- PowerShell on Windows

## Project setup

Run these commands from the project directory.

### 1. Create the virtual environment

```powershell
uv venv --seed .venv
```

The `--seed` option includes `pip` in the virtual environment.

### 2. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` at the beginning of your PowerShell prompt.

### 3. Install the project

```powershell
uv pip install -e .
```

The `-e` option installs the project in editable mode, so source changes are
available immediately without reinstalling the package.

### 4. Install development tools

```powershell
python -m pip install pytest
```

## Usage

Resolve a hostname with the module interface:

```powershell
python -m ip_resolver localhost
```

Example output:

```text
127.0.0.1
::1
```

The command returns exit code `0` when resolution succeeds.

For an invalid or unresolvable hostname:

```powershell
python -m ip_resolver hostname-that-does-not-exist.invalid
```

The command prints an error and returns exit code `1`.

## Running the tests

Run the complete test suite:

```powershell
python -m pytest -vv
```

Run only the resolver tests:

```powershell
python -m pytest -vv .\tests\test_resolver.py
```

Run only the command-line interface tests:

```powershell
python -m pytest -vv .\tests\test_cli.py
```

## Dependency workflows

This project supports both `uv` and `pip`:

```powershell
# Install dependencies declared in requirements.txt with pip
python -m pip install -r .\requirements.txt

# Install a package and record it in pyproject.toml with uv
uv add package-name
```

Application dependencies belong in `pyproject.toml`. Development-only tools
such as `pytest` should be installed in the active virtual environment.

## Project structure

```text
IP-resolve-flow/
├── docs/
├── src/
│   └── ip_resolver/
│       ├── __init__.py
│       ├── __main__.py
│       └── resolver.py
├── tests/
│   ├── test_cli.py
│   └── test_resolver.py
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```
