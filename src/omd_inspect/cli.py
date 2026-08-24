import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from omd_inspect.state import inspect_state
from omd_inspect.xmltypes import sniff_root_tag


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omd-inspect",
        description=(
            "Summarize an OpenMM State file (from Simulation.saveState()) without "
            "loading it in Python. Does not handle .chk checkpoints "
            "(Context.createCheckpoint()) — those are a separate, binary, "
            "non-portable format and out of scope for this tool."
        ),
    )
    parser.add_argument("path", type=Path, help="OpenMM State .xml file (not a .chk checkpoint)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.path.is_file():
        print(f"omd-inspect: no such file: {args.path}", file=sys.stderr)
        return 1

    root_tag = sniff_root_tag(args.path)
    if root_tag is None:
        print(f"omd-inspect: not well-formed XML: {args.path}", file=sys.stderr)
        return 1
    if root_tag != "State":
        print(
            f"omd-inspect: {args.path} is a {root_tag} file, not a State "
            "— nothing to inspect",
            file=sys.stderr,
        )
        return 1

    try:
        summary = inspect_state(args.path)
    except NotImplementedError as exc:
        print(f"omd-inspect: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(asdict(summary)) if args.json else summary)
    return 0 if summary.valid else 1


if __name__ == "__main__":
    sys.exit(main())
