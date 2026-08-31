# Changelog

## v1.0

- Detects occupied campaign slots.
- Displays current cash and money-spent values before patching.
- Patches all four known current-cash representations.
- Preserves existing money-spent counters.
- Locates variable campaign structures by signature instead of one fixed deep offset.
- Rebuilds the internal Blitz checksum.
- Verifies patched output before download.
- Enforces the observed `$16,777,215` current-cash ceiling.
- Includes a completely offline browser GUI and a Python reference/CLI implementation.
- Includes a beginner-oriented stock-PS3 + Bruteforce workflow.
