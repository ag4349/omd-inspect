# omd-inspect

Summarize an OpenMM state file from the command line — what `gmx check`/
`gmx dump` give you for GROMACS files, but for the XML `Simulation.saveState()`
produces.

No dedicated tool for this exists today. Inspecting a state file means
opening Python, importing OpenMM, and writing a few lines to load the file
and print its attributes, every time. `omd-inspect` removes that step:
point it at a file, get a summary, no code required.

Note the word "state file," not "checkpoint" — OpenMM's `Context.createCheckpoint()`
writes a binary, platform-specific `.chk` blob, which is a different thing
and out of scope here. This tool reads the portable XML `saveState()`/
`XmlSerializer` produces.

## Install

```bash
pip install omd-inspect          # cheap tier: stdlib only
pip install "omd-inspect[verify]" # adds the openmm-backed deep validation check
```

## Usage

```bash
omd-inspect state.xml
omd-inspect state.xml --json
```

A `.xml` file that isn't actually a `State` (OpenMM also serializes
`System` and `Integrator` objects the same way) is rejected with a clear
message naming what it actually is, rather than silently misparsed.

## Scope

**In scope:** read-only inspection of a single OpenMM `State` XML file —
particle count, step count, simulated time, whether positions/velocities/
a periodic box are present, box volume, and whether the file is well-formed
and (if `openmm` is installed) actually loadable via `XmlSerializer`.

**Out of scope:** trajectory files (`mdtraj`/`MDAnalysis`/`cpptraj` already
cover this), other MD engines' file formats (`gmx check`/`cpptraj` own
those), binary `.chk` checkpoints, live monitoring of a running simulation,
repairing corrupt files, and actually resuming a simulation — rebuilding a
`System` to resume from a state file is inherently pipeline-specific and
outside what a generic inspector can own.

## License

MIT
