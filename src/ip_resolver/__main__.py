import argparse

from ip_resolver.graph import build_domain_graph
from ip_resolver.models import DomainFlowState

def parse_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "port must be an integer between 1 and 65535"
        ) from error

    if not 1 <= port <= 65535:
        raise argparse.ArgumentTypeError(
            "port must be an integer between 1 and 65535"
        )

    return port


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate a domain and resolve its IP addresses."
    )
    parser.add_argument("hostname", help="The domain name to validate.")
    parser.add_argument(
        "--port",
        type=parse_port,
        help="Optional TCP port to test for IP reachability.",
    )
    args = parser.parse_args(arguments)

    initial_state: DomainFlowState = {
        "original_input": args.hostname,
        "normalized_hostname": args.hostname,
        "errors": [],
    }

    if args.port is not None:
        initial_state["port"] = args.port

    result = build_domain_graph().invoke(initial_state)

    if result.get("status") not in {"success", "success_no_port"}:
        for error in result.get("errors", []):
            print(f"Error: {error}")
        return 1

    for address in result.get("valid_ip_addresses", []):
        print(address)

    print("Stage: TLD and site validation passed.")
    if result.get("status") == "success_no_port":
        print("TCP reachability check skipped: no port supplied.")
    else:
        reachable = len(result.get("reachable_ip_addresses", []))
        print(
            f"TCP reachability on port {args.port}: "
            f"{reachable} reachable address(es)."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
