import pytest

from ip_resolver.__main__ import main


def test_main_prints_domain_addresses_without_port(capsys):
    exit_code = main(["example.com"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "TCP reachability check skipped" in captured.out
    assert captured.out.splitlines()[0]
    assert "Stage: TLD and site validation passed." in captured.out


def test_main_reports_resolution_error(capsys):
    exit_code = main(["site-that-does-not-exist-this-is-a-test.invalid"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Site name does not resolve" in captured.out


def test_main_rejects_invalid_port():
    with pytest.raises(SystemExit) as error:
        main(["example.com", "--port", "70000"])

    assert error.value.code == 2