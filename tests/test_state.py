from pathlib import Path

import pytest

from omd_inspect import state

FIXTURES = Path(__file__).parent / "fixtures"


def test_deep_validate_skipped_when_openmm_unavailable(monkeypatch):
    monkeypatch.setattr(state, "_deep_validate", lambda path: None)
    summary = state.inspect_state(FIXTURES / "state_valid.xml")
    assert summary.deep_check == "skipped (openmm not installed)"
    assert summary.valid is True


def test_deep_validate_failure_marks_invalid(monkeypatch):
    monkeypatch.setattr(state, "_deep_validate", lambda path: False)
    summary = state.inspect_state(FIXTURES / "state_valid.xml")
    assert summary.deep_check == "failed"
    assert summary.valid is False


def test_deep_validate_success_with_real_openmm():
    pytest.importorskip("openmm")
    summary = state.inspect_state(FIXTURES / "state_valid.xml")
    assert summary.deep_check == "passed"
    assert summary.valid is True
    assert summary.step_count == 5


def test_malformed_numeric_attr_marks_invalid_without_crashing(monkeypatch):
    monkeypatch.setattr(state, "_deep_validate", lambda path: None)
    summary = state.inspect_state(FIXTURES / "state_bad_stepcount.xml")
    assert summary.valid is False
    assert summary.step_count is None
    assert summary.particles == 2
