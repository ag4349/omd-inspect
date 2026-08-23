import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


@dataclass
class StateSummary:
    particles: int
    step_count: int | None
    time_ps: float | None
    has_positions: bool
    has_velocities: bool
    has_box: bool
    box_volume_nm3: float | None
    openmm_version: str | None
    valid: bool

    def __str__(self) -> str:
        lines = [
            f"particles       {self.particles}",
            f"step            {self.step_count}",
            f"time            {self.time_ps} ps",
            f"positions       {self.has_positions}",
            f"velocities      {self.has_velocities}",
            f"box             {self.has_box}",
        ]
        if self.box_volume_nm3 is not None:
            lines.append(f"box volume      {self.box_volume_nm3:.3f} nm^3")
        lines.append(f"openmm version  {self.openmm_version}")
        return "\n".join(lines)


def inspect_state(path: Path) -> StateSummary:
    root = ET.parse(path).getroot()

    positions = root.find("Positions")
    velocities = root.find("Velocities")
    box = root.find("PeriodicBoxVectors")

    valid = True
    particles = 0
    box_volume = None

    try:
        if positions is not None:
            particles = len(positions)
        elif velocities is not None:
            particles = len(velocities)
        if positions is not None and velocities is not None and len(positions) != len(velocities):
            valid = False
        if box is not None:
            box_volume = _box_volume(box)
    except (TypeError, ValueError):
        valid = False

    return StateSummary(
        particles=particles,
        step_count=_int_attr(root, "stepCount"),
        time_ps=_float_attr(root, "time"),
        has_positions=positions is not None,
        has_velocities=velocities is not None,
        has_box=box is not None,
        box_volume_nm3=box_volume,
        openmm_version=root.get("openmmVersion"),
        valid=valid,
    )


def _int_attr(elem: ET.Element, name: str) -> int | None:
    value = elem.get(name)
    return int(value) if value is not None else None


def _float_attr(elem: ET.Element, name: str) -> float | None:
    value = elem.get(name)
    return float(value) if value is not None else None


def _box_volume(box: ET.Element) -> float | None:
    vectors = []
    for tag in ("A", "B", "C"):
        v = box.find(tag)
        if v is None:
            return None
        vectors.append((float(v.get("x")), float(v.get("y")), float(v.get("z"))))
    a, b, c = vectors
    bxc = (
        b[1] * c[2] - b[2] * c[1],
        b[2] * c[0] - b[0] * c[2],
        b[0] * c[1] - b[1] * c[0],
    )
    return abs(a[0] * bxc[0] + a[1] * bxc[1] + a[2] * bxc[2])
