from dataclasses import dataclass
import re
import dns.exception
import dns.resolver
import ipaddress
import socket
import tldextract

from ip_resolver.resolver  import(
    HostnameResolutionError,
    resolve_hostname,
)

_TLD_EXTRACT = tldextract.TLDExtract(suffix_list_urls=())

@dataclass(frozen =True)
class TopLevelDomainResult:
    tld: str
    syntax_valid: bool
    exists: bool

@dataclass(frozen=True)
class SiteNameResult:
    site_name: str
    syntax_valid: bool
    exists: bool
    ip_addresses: list[str]

@dataclass(frozen=True)
class IPAddressResult:
    address: str
    syntax_valid: bool
    exists: bool | None
    port: int | None


def validate_top_level_domain(hostname: str) -> TopLevelDomainResult:
    """
    Validate the top-level domain (TLD) of a given hostname.

    Args:
        hostname (str): The hostname to validate.

    Returns:
        TopLevelDomainResult: A dataclass containing the TLD, syntax validity, and existence status.
    """
    normalized_hostname = hostname.strip().lower().rstrip(".")
    parts = normalized_hostname.split(".")

    if len(parts)< 2:
        return TopLevelDomainResult(
            tld= "",
            syntax_valid= False,
            exists= False,
        )


    extracted = _TLD_EXTRACT(normalized_hostname)
    tld = extracted.suffix or parts[-1]
    syntax_valid = all(
        (
            label.isalpha()
            or (
                label.startswith("xn--")
                and re.fullmatch(
                    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?",
                    label,
                )
                is not None
            )
        )
        and 2 <= len(label) <= 63
        for label in tld.split(".")
    )

    if not syntax_valid:
        return TopLevelDomainResult(
            tld = tld,
            syntax_valid = False,
            exists = False,
        )

    try:
        dns.resolver.resolve(tld, "NS")
    except dns.exception.DNSException:
        return TopLevelDomainResult(
            tld = tld,
            syntax_valid = True,
            exists = False,
        )

    return TopLevelDomainResult(
        tld = tld,
        syntax_valid = True,
        exists = True,
    )



def validate_site_name(hostname: str) -> SiteNameResult:
    """
    Validate the site name of a given hostname.

    Args:
        hostname (str): The hostname to validate.

    Returns:
        SiteNameResult: A dataclass containing the site name, syntax validity, existence status, and resolved IP addresses.
    """
    normalized_hostname = hostname.strip().lower().rstrip(".")
    parts = normalized_hostname.split('.')

    if len(parts) < 2:
        return SiteNameResult(
            site_name = "",
            syntax_valid = False,
            exists = False,
            ip_addresses = [],
        )

    extracted = _TLD_EXTRACT(normalized_hostname)
    site_name = extracted.domain if extracted.suffix else parts[-2]
    site_name_pattern= r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    syntax_valid= re.fullmatch(site_name_pattern, site_name) is not None

    if not syntax_valid:
        return SiteNameResult(
            site_name = site_name,
            syntax_valid = False,
            exists = False,
            ip_addresses = [],
        )

    try:
        ip_addresses = resolve_hostname(normalized_hostname)
    except HostnameResolutionError:
        return SiteNameResult(
            site_name = site_name,
            syntax_valid = True,
            exists = False,
            ip_addresses = [],
        )

    return SiteNameResult(
        site_name = site_name,
        syntax_valid = True,
        exists = True,
        ip_addresses = ip_addresses,
    )




def validate_ip_address(address: str, port: int| None = None) -> IPAddressResult:
    try:
        ipaddress.ip_address(address)
    except ValueError:
        return IPAddressResult(
            address=address,
            syntax_valid=False,
            exists=False,
            port=port,
        )

    if port is None:
        return IPAddressResult(
            address=address,
            syntax_valid=True,
            exists=None,
            port=None,
        )

    try:
        with socket.create_connection((address, port), timeout=2):
            exists = True
    except (OSError, ValueError):
        exists = False

    return IPAddressResult(
        address=address,
        syntax_valid=True,
        exists=exists,
        port=port,
    )