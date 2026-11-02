from typing import TypedDict, NotRequired


class DomainFlowState(TypedDict):
    original_input: str
    normalized_hostname: str
    port: NotRequired[int]

    tld: NotRequired[str]
    tld_syntax_valid: NotRequired[bool]
    tld_exists: NotRequired[bool]

    site_name: NotRequired[str]
    site_name_syntax_valid: NotRequired[bool]
    site_name_exists: NotRequired[bool]

    ip_addresses: NotRequired[list[str]]
    valid_ip_addresses: NotRequired[list[str]]
    reachable_ip_addresses: NotRequired[list[str]]

    ip_syntax_valid: NotRequired[bool]
    ip_exists: NotRequired[bool]

    errors: list[str]
    status: NotRequired[str]
    current_stage: NotRequired[str]