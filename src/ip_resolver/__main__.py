import argparse

from ip_resolver.resolver import (
    HostnameResolutionError,
    InvalidHostnameError,
    resolve_hostname,
)

def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Resolve a hostname to its IP addresses."
    )
    parser.add_argument("hostname", help="The hostname to resolve.")
    args = parser.parse_args(arguments)

    try:
        addresses = resolve_hostname(args.hostname)
    except (InvalidHostnameError, HostnameResolutionError) as error:
        print(f"Error: {error}")
        return 1

    for address in addresses:
        print(address)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
