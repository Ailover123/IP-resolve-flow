from ip_resolver.validators import(
    validate_site_name,
    validate_top_level_domain,
    validate_ip_address,
)

def test_validate_top_level_domain_accepts_existing_com():
    result = validate_top_level_domain("example.com")

    assert result.tld == "com"
    assert result.syntax_valid is True
    assert result.exists is True


def test_validate_top_level_domain_rejects_invalid_syntax():
    result = validate_top_level_domain("example.1")

    assert result.tld == "1"
    assert result.syntax_valid is False
    assert result.exists is False


def test_validate_top_level_domain_rejects_nonexistent_tld():
    result = validate_top_level_domain("example.thistldisnotreal")

    assert result.tld == "thistldisnotreal"
    assert result.syntax_valid is True
    assert result.exists is False


def test_validate_top_level_domain_accepts_multi_label_suffix():
    result = validate_top_level_domain("example.co.uk")

    assert result.tld == "co.uk"
    assert result.syntax_valid is True
    assert result.exists is True


def test_validate_site_name_accepts_existing_site():
    result = validate_site_name("example.com")

    assert result.site_name == "example"
    assert result.syntax_valid is True
    assert result.exists is True
    assert result.ip_addresses


def test_validate_site_name_extracts_name_before_multi_label_suffix():
    result = validate_site_name("example.co.uk")

    assert result.site_name == "example"

def test_validate_site_name_rejects_invalid_syntax():
    result = validate_site_name("-example.com")

    assert result.site_name == "-example"
    assert result.syntax_valid is False
    assert result.exists is False
    assert result.ip_addresses == []


def test_validate_site_name_rejects_nonexistent_site():
    result = validate_site_name(
        "site-that-does-not-exist-this-is-a-test.invalid"
    )

    assert result.site_name == "site-that-does-not-exist-this-is-a-test"
    assert result.syntax_valid is True
    assert result.exists is False
    assert result.ip_addresses == []

def test_validate_ip_address_accepts_reachable_localhost():
    result = validate_ip_address("127.0.0.1", 135)

    assert result.address == "127.0.0.1"
    assert result.syntax_valid is True
    assert result.exists is True
    assert result.port == 135

def test_validate_ip_address_rejects_invalid_syntax():
    result = validate_ip_address("999.999.999.999", 135)

    assert result.address == "999.999.999.999"
    assert result.syntax_valid is False
    assert result.exists is False
    assert result.port == 135


def test_validate_ip_address_skips_reachability_without_port():
    result = validate_ip_address("127.0.0.1")

    assert result.address == "127.0.0.1"
    assert result.syntax_valid is True
    assert result.exists is None
    assert result.port is None