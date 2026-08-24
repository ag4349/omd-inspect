import json
from pathlib import Path

import pytest

from omd_inspect import __version__
from omd_inspect.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def test_help_exits_zero(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_version_exits_zero(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_missing_file_exits_nonzero(tmp_path, capsys):
    missing = tmp_path / "does_not_exist.xml"
    assert main([str(missing)]) == 1
    assert "no such file" in capsys.readouterr().err


def test_valid_state_exits_zero(capsys):
    assert main([str(FIXTURES / "state_valid.xml")]) == 0
    out = capsys.readouterr().out
    assert "particles       4" in out
    assert "step            5" in out


def test_valid_state_json(capsys):
    assert main([str(FIXTURES / "state_valid.xml"), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["particles"] == 4
    assert payload["step_count"] == 5
    assert payload["has_velocities"] is True
    assert payload["valid"] is True
    assert payload["openmm_version"] == "8.6"


def test_quiet_suppresses_output_on_success(capsys):
    assert main([str(FIXTURES / "state_valid.xml"), "--quiet"]) == 0
    out, err = capsys.readouterr()
    assert out == ""
    assert err == ""


def test_quiet_still_reports_missing_file_on_stderr(tmp_path, capsys):
    missing = tmp_path / "does_not_exist.xml"
    assert main([str(missing), "-q"]) == 1
    out, err = capsys.readouterr()
    assert out == ""
    assert "no such file" in err


def test_not_xml_rejected(capsys):
    assert main([str(FIXTURES / "not_xml.txt")]) == 1
    assert "not well-formed XML" in capsys.readouterr().err


def test_truncated_state_rejected(capsys):
    assert main([str(FIXTURES / "state_truncated.xml")]) == 1
    assert "not well-formed XML" in capsys.readouterr().err


def test_wrong_xml_type_rejected(capsys):
    assert main([str(FIXTURES / "system.xml")]) == 1
    err = capsys.readouterr().err
    assert "System" in err
    assert "not a State" in err
