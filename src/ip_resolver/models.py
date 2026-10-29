from typing import TypedDict


class DomainFlowState(TypedDict, total=False):
    original_input: str
    normalized_hostname: str

    tld: str
    tld_syntax_valid: bool
    tld_exists: bool

    site_name: str
    site_name_syntax_valid: bool
    site_name_exists: bool

    ip_addresses: list[str]
    valid_ip_addresses: list[str]
    reachable_ip_addresses: list[str]

    ip_syntax_valid: bool
    ip_exists: bool

    errors: list[str]
    status: str
    current_stage: str