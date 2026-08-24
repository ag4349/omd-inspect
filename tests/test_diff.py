from pathlib import Path

from omd_inspect import state
from omd_inspect.diff import DiffResult

FIXTURES = Path(__file__).parent / "fixtures"


def _summary(name: str) -> state.StateSummary:
    return state.inspect_state(FIXTURES / name)


def test_comparable_when_same_particle_count_and_both_valid():
    result = DiffResult(
        a=_summary("state_valid.xml"),
        b=_summary("state_valid_later.xml"),
        comparable=True,
    )
    assert result.comparable is True
    assert result.a.step_count == 5
    assert result.b.step_count == 250


def test_not_comparable_on_particle_count_mismatch():
    a = _summary("state_valid.xml")
    b = _summary("state_valid_2particles.xml")
    comparable = a.valid and b.valid and a.particles == b.particles
    assert comparable is False


def test_str_includes_both_columns_and_comparable_line():
    result = DiffResult(a=_summary("state_valid.xml"), b=_summary("state_valid_later.xml"), comparable=True)
    text = str(result)
    assert "particles" in text
    assert "step" in text
    assert "comparable" in text
    assert "True" in text
