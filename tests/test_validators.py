from ip_resolver.validators import validate_top_level_domain


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