# IP Resolve Flow

`IP Resolve Flow` is a Python command-line tool built as a LangGraph workflow.
It validates a domain in stages and resolves it to unique IP addresses.

The project currently provides:

- Hostname validation
- IPv4 and IPv6 address resolution
- IDNA-compatible hostname handling
- Clear errors for invalid input and DNS failures
- Logging for successful and failed resolution attempts
- Optional TCP reachability checks
- Conditional LangGraph routing when a validation stage fails
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

Validate a domain, resolve its addresses, and skip TCP reachability:

```powershell
python -m ip_resolver example.com
```

Example output:

```text
104.20.23.154
172.66.147.243
Stage: TLD and site validation passed.
TCP reachability check skipped: no port supplied.
```

Test TCP reachability by supplying a port:

```powershell
python -m ip_resolver example.com --port 443
```

The port must be between `1` and `65535`. Without `--port`, the workflow
checks IP syntax but does not attempt a TCP connection.

For an invalid or unresolvable hostname:

```powershell
python -m ip_resolver site-that-does-not-exist-this-is-a-test.invalid
```

The command prints an error and returns exit code `1`.

## LangGraph flow

The workflow passes a shared state object through three stages:

```text
START
  |
  v
TLD syntax and existence
  |
  v
Site-name syntax and DNS existence
  |
  v
IP syntax and optional TCP reachability
  |
  v
END
```

The TLD stage understands multi-label public suffixes such as `co.uk`.
The site-name stage extracts `example` from `example.co.uk`.

If the TLD or site-name stage fails, a conditional edge routes directly to
`END`. The state includes an error such as `TLD does not exist` or
`Site name does not resolve`.

IP validation has two separate meanings:

- IP syntax checks whether an address is valid IPv4 or IPv6.
- TCP reachability checks whether a connection succeeds on the supplied port.

These are intentionally separate. A valid IP does not guarantee that a
service is listening on a particular port.

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
