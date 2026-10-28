from ip_resolver.__main__ import main


def test_main_prints_localhost_addresses(capsys):
    exit_code = main(["localhost"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out.strip()


def test_main_reports_resolution_error(capsys):
    exit_code = main(["hostname-that-does-not-exist.invalid"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Could not resolve hostname" in captured.out