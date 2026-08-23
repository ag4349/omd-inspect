from dataclasses import dataclass
from pathlib import Path


@dataclass
class StateSummary:
    particles: int
    has_positions: bool
    has_velocities: bool
    has_box: bool
    time_ps: float | None
    box_volume_nm3: float | None
    valid: bool


def inspect_state(path: Path) -> StateSummary:
    raise NotImplementedError(
        f"state inspection for {path} is not implemented yet — see "
        "IMPLEMENTATION_PLAN.md"
    )
