import argparse
import sys
from pathlib import Path

from omd_inspect.state import inspect_state
from omd_inspect.trajectory import inspect_trajectory

STATE_SUFFIXES = {".xml"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omd-inspect",
        description=(
            "Summarize an OpenMM checkpoint state file or trajectory segment "
            "without loading it in Python."
        ),
    )
    parser.add_argument("path", type=Path, help="state .xml or trajectory file")
    parser.add_argument(
        "--top",
        type=Path,
        default=None,
        help="topology file, required for trajectory formats that don't carry one (e.g. .xtc)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.path.is_file():
        print(f"omd-inspect: no such file: {args.path}", file=sys.stderr)
        return 1

    try:
        if args.path.suffix.lower() in STATE_SUFFIXES:
            summary = inspect_state(args.path)
        else:
            summary = inspect_trajectory(args.path, topology=args.top)
    except NotImplementedError as exc:
        print(f"omd-inspect: {exc}", file=sys.stderr)
        return 1

    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
