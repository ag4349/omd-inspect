# omd-inspect

Summarize an OpenMM checkpoint state file or trajectory segment from the
command line — what `gmx check`/`gmx dump` give you for GROMACS files, but
for the files `Simulation.saveState()` and `mdtraj` produce.

No dedicated tool for this exists today. Inspecting an OpenMM checkpoint
means opening Python, importing OpenMM, and writing a few lines to load the
file and print its attributes, every time. `omd-inspect` removes that step:
point it at a file, get a summary, no code required.

## Status

Early scaffolding. The CLI and dispatch logic exist; the actual state/
trajectory parsing is not implemented yet (see the commit history and the
project's implementation plan, kept locally, not in this repo).

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```bash
omd-inspect checkpoint.xml
omd-inspect segment.xtc --top topology.pdb
```

## Scope

**In scope:** read-only inspection of a single OpenMM `State` XML file or a
single trajectory segment (via `mdtraj`), reporting the handful of things
you'd actually want to know at a glance — particle/atom count, whether
velocities and a periodic box are present, simulated time, frame count and
time range for trajectories, and whether the file is well-formed.

**Out of scope:** other MD engines' file formats (GROMACS/AMBER/NAMD already
have `gmx check`/`cpptraj` for this), live monitoring of a running
simulation, repairing corrupt files, full trajectory analysis (RMSD, etc.),
and actually resuming a simulation — rebuilding a `System` to resume from a
checkpoint is inherently pipeline-specific and outside what a generic
inspector can own.

## License

MIT
