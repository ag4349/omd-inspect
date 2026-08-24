import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from omd_inspect import __version__
from omd_inspect.diff import DiffResult
from omd_inspect.state import StateSummary, inspect_state
from omd_inspect.xmltypes import sniff_root_tag

_EPILOG = """examples:
  omd-inspect state.xml
  omd-inspect state.xml --json
  omd-inspect a.xml --diff b.xml
  omd-inspect state.xml -q && echo still running
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omd-inspect",
        description=(
            "Summarize an OpenMM State file (from Simulation.saveState()) without "
            "loading it in Python. Does not handle .chk checkpoints "
            "(Context.createCheckpoint()) — those are a separate, binary, "
            "non-portable format and out of scope for this tool."
        ),
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("path", type=Path, help="OpenMM State .xml file (not a .chk checkpoint)")
    parser.add_argument(
        "--diff",
        type=Path,
        metavar="PATH",
        default=None,
        help="diff against a second State file instead of inspecting one",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="suppress the summary output; only the exit code signals validity/comparability",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _load_state(path: Path) -> tuple[StateSummary | None, str | None]:
    if not path.is_file():
        return None, f"no such file: {path}"

    root_tag = sniff_root_tag(path)
    if root_tag is None:
        return None, f"not well-formed XML: {path}"
    if root_tag != "State":
        return None, f"{path} is a {root_tag} file, not a State — nothing to inspect"

    return inspect_state(path), None


def _run_inspect(path: Path, *, json_output: bool, quiet: bool) -> int:
    summary, err = _load_state(path)
    if err is not None:
        print(f"omd-inspect: {err}", file=sys.stderr)
        return 1

    if not quiet:
        print(json.dumps(asdict(summary)) if json_output else summary)
    return 0 if summary.valid else 1


def _run_diff(path_a: Path, path_b: Path, *, json_output: bool, quiet: bool) -> int:
    summary_a, err_a = _load_state(path_a)
    if err_a is not None:
        print(f"omd-inspect: {err_a}", file=sys.stderr)
    summary_b, err_b = _load_state(path_b)
    if err_b is not None:
        print(f"omd-inspect: {err_b}", file=sys.stderr)

    if summary_a is None or summary_b is None:
        return 1

    result = DiffResult(
        a=summary_a,
        b=summary_b,
        comparable=summary_a.valid and summary_b.valid and summary_a.particles == summary_b.particles,
    )

    if not quiet:
        if json_output:
            payload = {"a": asdict(result.a), "b": asdict(result.b), "comparable": result.comparable}
            print(json.dumps(payload))
        else:
            print(result)
    return 0 if result.comparable else 1


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.diff is not None:
        return _run_diff(args.path, args.diff, json_output=args.json, quiet=args.quiet)
    return _run_inspect(args.path, json_output=args.json, quiet=args.quiet)


if __name__ == "__main__":
    sys.exit(main())
