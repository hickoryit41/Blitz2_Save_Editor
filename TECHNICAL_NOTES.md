# Technical Notes — Blitz: The League II PS3 Campaign Money

Verified against the North American PS3 release (`BLUS30203`).

## Why a simple hex edit fails

Campaign cash is represented multiple times. Editing only the obvious plain integer fields can change what the campaign-selection screen displays while the loaded campaign reconstructs a different value from its serialized state. The game also stores an internal checksum inside `BSAV0.SAV`.

## Known current-cash representations

For each detected occupied campaign, v1.0 updates:

1. A plain 32-bit big-endian current-cash value in the campaign summary.
2. A plain 32-bit big-endian current-cash value in the global campaign cash array.
3. A 24-bit positive current-cash value whose three bytes are XOR-obfuscated with `0x3A`.
4. A signed 32-bit negative-current-cash value whose four bytes are XOR-obfuscated with `0x3A`.

The tool leaves the existing money-spent counters unchanged.

## Why the deep offsets are not hard-coded

Controlled saves showed that team/player customization changes the serialized campaign length. In particular, longer strings and other customization can shift later structures. Therefore the editor locates campaign serialization using invariant byte signatures and then derives the nearby money fields instead of assuming one fixed absolute offset for every save.

## Internal Blitz checksum

`BSAV0.SAV` stores its game-level checksum at:

```text
0x250 - 0x253
```

The checksum covers:

```text
0x254 through end-of-file
```

Algorithm used by the tool:

- CRC polynomial: `0x04C11DB7`
- initial value: `0`
- non-reflected / big-endian bit processing
- result stored big-endian at `0x250`

The tool recalculates this checksum after patching and then re-analyzes the produced file before allowing the output.

## Cash limit

One current-cash representation is 24 bits wide:

```text
0xFFFFFF = 16,777,215
```

Therefore v1.0 deliberately rejects larger requested values.

Normal gameplay behavior when cash-on-hand crosses that boundary has not been fully characterized. Keep backups.

## Verified behavior

The patch logic was validated using controlled saves with multiple spending states and multiple player/team configurations. A five-campaign save patched to `$8,500,000` per occupied campaign was successfully loaded on a stock PS3; all five campaigns could purchase upgrades, save, and reload normally.

## Scope

This utility edits the game-level decrypted `BSAV0.SAV`. It does not implement Sony PS3 save encryption or PFD resigning. That outer save-container work is intentionally left to Bruteforce Save Data in the documented stock-PS3 workflow.
