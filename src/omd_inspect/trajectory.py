from dataclasses import dataclass
from pathlib import Path


@dataclass
class TrajectorySummary:
    frames: int
    atom_count: int
    time_range_ps: tuple[float, float] | None
    box_range_nm3: tuple[float, float] | None
    valid: bool


def inspect_trajectory(path: Path, topology: Path | None = None) -> TrajectorySummary:
    raise NotImplementedError(
        f"trajectory inspection for {path} is not implemented yet — see "
        "IMPLEMENTATION_PLAN.md"
    )
