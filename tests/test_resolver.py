import pytest

from ip_resolver.resolver import(
    resolve_hostname,
    InvalidHostnameError,
    HostnameResolutionError,
)
def test_resolve_hostname_returns_ip_addresses():
    addresses = resolve_hostname("example.com")

    assert isinstance(addresses, list)
    assert addresses
"""
def test_resolve_hostname_accepts_unicode_hostname():
    addresses = resolve_hostname("例子.测试")

    assert isinstance(addresses, list)
    assert addresses
"""
@pytest.mark.parametrize("invalid_hostname", ["", "   ", None, 123])
def test_resolve_hostname_rejects_invalid_input(invalid_hostname):
    with pytest.raises(InvalidHostnameError):
        resolve_hostname(invalid_hostname)


def test_resolve_hostname_reports_dns_failure():
    with pytest.raises(HostnameResolutionError, match="Could not resolve hostname"):
        resolve_hostname("hostname-that-does-not-exist.invalid")


def test_resolve_hostname_logs_success(caplog):
    with caplog.at_level("INFO"):
        resolve_hostname("example.com")

    assert "Resolved hostname example.com" in caplog.text

def test_resolve_hostname_logs_invalid_input(caplog):
    with caplog.at_level("WARNING"):
        with pytest.raises(InvalidHostnameError):
            resolve_hostname("")

    assert "Invalid hostname input" in caplog.text


def test_resolve_hostname_logs_dns_failure(caplog):
    with caplog.at_level("ERROR"):
        with pytest.raises(HostnameResolutionError):
            resolve_hostname("hostname-that-does-not-exist.invalid")

    assert "Failed to resolve hostname" in caplog.text