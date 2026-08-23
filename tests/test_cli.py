import pytest

from omd_inspect.cli import main


def test_help_exits_zero(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_missing_file_exits_nonzero(tmp_path, capsys):
    missing = tmp_path / "does_not_exist.xml"
    assert main([str(missing)]) == 1
    assert "no such file" in capsys.readouterr().err


def test_unimplemented_state_file_exits_nonzero(tmp_path, capsys):
    state_file = tmp_path / "checkpoint.xml"
    state_file.write_text("<State/>")
    assert main([str(state_file)]) == 1
    assert "not implemented yet" in capsys.readouterr().err
