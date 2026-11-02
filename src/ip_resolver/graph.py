from langgraph.graph import START, END, StateGraph

from ip_resolver.models import DomainFlowState
from ip_resolver.validators import(
    validate_top_level_domain,
    validate_site_name,
    validate_ip_address,
)

def check_top_level_domain(state: DomainFlowState) -> dict[str, object]:
    result = validate_top_level_domain(state["normalized_hostname"])
    errors: list[str] = []

    if not result.syntax_valid:
        errors.append("TLD syntax is invalid")
    elif not result.exists:
        errors.append("TLD does not exist")

    return {
        "tld": result.tld,
        "tld_syntax_valid": result.syntax_valid,
        "tld_exists": result.exists,
        "errors": errors,
        "current_stage": "tld_check",
        "status": "success" if result.syntax_valid and result.exists else "failed",
    }

def route_after_tld_check(state: DomainFlowState) -> str:
    if state.get("tld_syntax_valid", False) and state.get(
         "tld_exists", False
    ):
         return "check_site_name"

    return "failed"

def check_site_name(state: DomainFlowState) -> dict[str, object]:
    result = validate_site_name(state["normalized_hostname"])
    errors: list[str] = []

    if not result.syntax_valid:
        errors.append("Site name syntax is invalid")
    elif not result.exists:
        errors.append("Site name does not resolve")

    return {
        "site_name": result.site_name,
        "site_name_syntax_valid": result.syntax_valid,
        "site_name_exists": result.exists,
        "ip_addresses": result.ip_addresses,
        "errors": errors,
        "status": "success" if result.syntax_valid and result.exists else "failed",
        "current_stage": "site_name_check",
    }

def route_after_site_name_check(state: DomainFlowState) -> str:
    if state.get("site_name_syntax_valid", False) and state.get(
        "site_name_exists", False
    ):
        return "validate_ips"

    return "failed"

def validate_ips(state: DomainFlowState) -> dict[str, object]:
    ip_addresses = state.get("ip_addresses", [])
    port = state.get("port")

    valid_ip_addresses: list[str] = []
    reachable_ip_addresses: list[str] = []

    for address in ip_addresses:
        result = validate_ip_address(address, port)

        if result.syntax_valid:
            valid_ip_addresses.append(address)

        if result.exists is True:
            reachable_ip_addresses.append(address)


    if not valid_ip_addresses:
        status = "failed"
        errors = ["No valid IP addresses found"]
    elif port is None:
        status = "success_no_port"
        errors = []
    elif reachable_ip_addresses:
        status = "success"
        errors = []
    else:
        status = "failed"
        errors = [f"No reachable IP addresses found on port {port}"]

    return {
        "valid_ip_addresses": valid_ip_addresses,
        "reachable_ip_addresses": reachable_ip_addresses,
        "ip_syntax_valid": bool(valid_ip_addresses),
        "ip_exists": (
            None if port is None else bool(reachable_ip_addresses)
        ),
        "errors": errors,
        "status": status,
        "current_stage": "ip_check",
    }

def build_domain_graph():

    builder = StateGraph(DomainFlowState)

    builder.add_node("check_tld", check_top_level_domain)
    builder.add_node("check_site_name", check_site_name)
    builder.add_node("validate_ips", validate_ips)

    builder.add_edge(START, "check_tld")
    builder.add_conditional_edges(
    "check_tld",
    route_after_tld_check,
    {
        "check_site_name": "check_site_name",
        "failed": END,
    },
    )
    builder.add_conditional_edges(
    "check_site_name",
    route_after_site_name_check,
    {
        "validate_ips": "validate_ips",
        "failed": END,
    },
    )

    builder.add_edge("validate_ips", END)

    return builder.compile()