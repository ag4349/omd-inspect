from dataclasses import dataclass

from omd_inspect.state import StateSummary

_LABEL_WIDTH = 16


@dataclass
class DiffResult:
    a: StateSummary
    b: StateSummary
    comparable: bool

    def __str__(self) -> str:
        rows: list[tuple[str, object, object]] = [
            ("particles", self.a.particles, self.b.particles),
            ("step", self.a.step_count, self.b.step_count),
            ("time", _fmt_ps(self.a.time_ps), _fmt_ps(self.b.time_ps)),
            ("positions", self.a.has_positions, self.b.has_positions),
            ("velocities", self.a.has_velocities, self.b.has_velocities),
            ("box", self.a.has_box, self.b.has_box),
        ]
        if self.a.box_volume_nm3 is not None or self.b.box_volume_nm3 is not None:
            rows.append(
                ("box volume", _fmt_volume(self.a.box_volume_nm3), _fmt_volume(self.b.box_volume_nm3))
            )
        rows.append(("openmm version", self.a.openmm_version, self.b.openmm_version))
        rows.append(("deep check", self.a.deep_check, self.b.deep_check))

        col_width = max(len(str(v)) for _, av, bv in rows for v in (av, bv)) + 2
        col_width = max(col_width, len("a") + 2)

        lines = [f"{'':<{_LABEL_WIDTH}}{'a':<{col_width}}b"]
        lines.extend(
            f"{label:<{_LABEL_WIDTH}}{a_val!s:<{col_width}}{b_val}" for label, a_val, b_val in rows
        )
        lines.append(f"{'comparable':<{_LABEL_WIDTH}}{self.comparable}")
        return "\n".join(lines)


def _fmt_ps(value: float | None) -> str:
    return f"{value} ps" if value is not None else "None"


def _fmt_volume(value: float | None) -> str:
    return f"{value:.3f} nm^3" if value is not None else "None"
