import socket
import logging

logger = logging.getLogger(__name__)

class InvalidHostnameError(ValueError):
    """Raised when the hostname input is invalid"""

class HostnameResolutionError(Exception):
    """Raised when a hostname cannot be resolved to an IP address"""

def resolve_hostname(hostname: object) -> list[str]:
    """
    Resolves a hostname to its corresponding IP addresses.

    Args:
        hostname (str): The hostname to resolve.

    Returns:
        list[str]: A list of IP addresses associated with the hostname.
    """

    if not isinstance(hostname, str) or not hostname.strip():
        logger.warning("Invalid hostname input: %r", hostname)
        raise InvalidHostnameError("Invalid hostname")

    normalized_hostname = hostname.strip().encode("idna").decode("ascii")

    try:
        addresses = socket.getaddrinfo(normalized_hostname, None)
    except socket.gaierror as error:
        logger.error("Failed to resolve hostname: %s", hostname)
        raise HostnameResolutionError(
            f"Could not resolve hostname: {hostname}"
        )from error

    

    ip_addresses: set[str] = set()

    for address in addresses:
        host = address[4][0]

        if isinstance(host, str):
            ip_addresses.add(host)

    result = sorted(ip_addresses)
    logger.info("Resolved hostname %s to %s", hostname, result)
    return result

