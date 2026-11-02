from ip_resolver.graph import build_domain_graph
from ip_resolver.models import DomainFlowState


def test_domain_graph_resolves_example_com():
    graph = build_domain_graph()

    initial_state: DomainFlowState = {
        "original_input": "example.com",
        "normalized_hostname": "example.com",
        "port": 443,
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "success"
    assert result["tld"] == "com"
    assert result["tld_syntax_valid"] is True
    assert result["tld_exists"] is True
    assert result["site_name"] == "example"
    assert result["site_name_syntax_valid"] is True
    assert result["site_name_exists"] is True
    assert result["ip_addresses"]
    assert result["valid_ip_addresses"]
    assert result["reachable_ip_addresses"]
    assert result["ip_syntax_valid"] is True
    assert result["ip_exists"] is True


def test_domain_graph_stops_when_tld_does_not_exist():
    graph = build_domain_graph()

    initial_state: DomainFlowState = {
        "original_input": "example.thistlddoesnotexistxyz",
        "normalized_hostname": "example.thistlddoesnotexistxyz",
        "port": 443,
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["tld_syntax_valid"] is True
    assert result["tld_exists"] is False
    assert result["status"] == "failed"
    assert result["errors"] == ["TLD does not exist"]
    assert "ip_addresses" not in result


def test_domain_graph_stops_when_site_name_is_invalid():
    graph = build_domain_graph()

    initial_state: DomainFlowState = {
        "original_input": "-example.com",
        "normalized_hostname": "-example.com",
        "port": 443,
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["tld_syntax_valid"] is True
    assert result["tld_exists"] is True
    assert result["site_name"] == "-example"
    assert result["site_name_syntax_valid"] is False
    assert result["site_name_exists"] is False
    assert result["status"] == "failed"
    assert result["errors"] == ["Site name syntax is invalid"]
    assert "ip_addresses" in result


def test_domain_graph_stops_when_site_does_not_exist():
    graph = build_domain_graph()

    initial_state: DomainFlowState = {
        "original_input": (
            "site-that-does-not-exist-this-is-a-test.invalid"
        ),
        "normalized_hostname": (
            "site-that-does-not-exist-this-is-a-test.invalid"
        ),
        "port": 443,
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["tld_syntax_valid"] is True
    assert result["tld_exists"] is True
    assert result["site_name_syntax_valid"] is True
    assert result["site_name_exists"] is False
    assert result["status"] == "failed"
    assert result["errors"] == ["Site name does not resolve"]


def test_domain_graph_resolves_without_port():
    graph = build_domain_graph()

    initial_state: DomainFlowState = {
        "original_input": "example.com",
        "normalized_hostname": "example.com",
        "errors": [],
    }

    result = graph.invoke(initial_state)

    assert result["status"] == "success_no_port"
    assert result["ip_addresses"]
    assert result["valid_ip_addresses"]
    assert result["ip_syntax_valid"] is True
    assert result["ip_exists"] is None
    assert result["reachable_ip_addresses"] == []