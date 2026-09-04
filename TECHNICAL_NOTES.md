# Technical Notes — Blitz: The League II PS3 Save Editor v1.3

Verified against controlled saves from the North American PS3 release (`BLUS30203`).

## Scope

The editor modifies the game's **decrypted** `BSAV0.SAV`.

Sony PS3 save-container encryption and `PARAM.PFD` signing/rebuilding are outside the editor and must be handled separately.

## XOR serialization

Many campaign/player values are stored bytewise XOR-obfuscated with:

```text
0x3A
```

A "decoded" byte in these notes means:

```text
stored_byte XOR 0x3A
```

## Stable campaign anchor

v1.2 uses:

```text
C5 1C D1 42 5B 3A 3A 3B 38 39 45 07 51 07
```

The two bytes immediately following that anchor are campaign state and are not treated as fixed.

Known fields relative to the anchor:

```text
Juice of the Week selector = anchor - 0x25
Team Risk byte             = anchor - 0x15
positive 24-bit cash       = anchor + 0x10
```

All three are XOR-`0x3A` encoded except the separate plain cash copies documented below.

## Juice enum

| Decoded enum | Drug |
|---:|---|
| 9 | Andersol |
| 10 | Krextol |
| 11 | Hoptenal |
| 12 | Mastaphene |
| 13 | Zoltox |
| 14 | Letaciline |
| 15 | Ultranol |
| 16 | BF-56 |
| 17 | Cyloderm |
| 18 | TGH |

## Roster signature

Stored-byte signature:

```text
F0 7B F2 69 3B 3A 3A 30
```

The decoded byte immediately after the eight-byte signature behaves as a roster serialized-size value. It increases by exactly 14 for every player juice record inserted.

This field was initially mistaken for Team Risk during early reverse engineering. It is **not** Team Risk.


## Franchise-style duplicated player records

### Proven native model

The first v1.2.1-v1.2.3 implementation incorrectly treated the two real Franchise
player-state copies as two ordinary player insertions. A stock-PS3 acceptance test
softlocked on campaign load.

A controlled native pair (`BSAV0_NoJuice.SAV` and `BSAV0_Juiced.SAV`) contains a
clean Slot-3 case where **KID FRANCHISE is the only logical juiced player**.

Applying the corrected model to the no-juice save reproduces the native Slot-3
roster byte-for-byte with **zero differences**.

For an unjuiced duplicated Franchise player, relative to each serialized name:

```text
special list count: name - 50
reference A1:       name - 44
reference A2:       name - 39
generic count:      name - 28   (DO NOT increment for Franchise juice)
reference B1:       name - 22
reference B2:       name - 17
```

Before native Franchise juicing the four references are:

```text
11 11 ... 10 10
```

After juicing:

```text
10 10 ... 11 11
```

The special list count changes:

```text
3 -> 4
```

For the **primary** Franchise copy:

```text
primary roster serialized size += 14
insert one 14-byte juice record before the name
generic name-adjacent count remains unchanged
```

For the **secondary** Franchise copy:

```text
secondary container size at unjuiced name - 51 += 14
insert the matching 14-byte juice record before the name
generic name-adjacent count remains unchanged
```

The primary roster size therefore grows by **14 per logical juiced player**, not
14 per physical Franchise record. The secondary copy has its own container
bookkeeping.

Both Franchise juice records use the same drug enum and the same juice-slot index.
v1.2.4 uses risk `0` in both records.


### Stock-PS3 acceptance

The corrected duplicated-Franchise model completed the full Raiders acceptance test:

```text
campaign load:        PASS
Franchise juice UI:   PASS
Team Risk 0:          PASS
gameplay effect:      PASS
game completion:      PASS
save/reload:          PASS
next-week init:       PASS
post-game cleanup:    PASS
```

This behavior is stable in v1.3 for the verified BLUS30203 workflow.


## Player juice record

A normal player juice effect is a 14-byte decoded record immediately before the serialized player name.

General controlled format:

```text
12 04 00 00 01 [juice index] 00 00 00 [drug enum] [32-bit BE risk]
```

Example, Mastaphene, first juice slot, risk 20:

```text
12 04 00 00 01 00 00 00 00 0C 00 00 00 14
```

Example, TGH, risk 25:

```text
12 04 00 00 01 00 00 00 00 12 00 00 00 19
```

v1.2-created records use:

```text
risk = 0
```

## Real Team Risk field

Decoded Team Risk:

```text
campaign anchor - 0x15
```

Controlled Mastaphene samples:

```text
0 players -> 0
1 player  -> 20
2 players -> 40
```

Controlled TGH:

```text
3 players -> 75
```

Preloading a different campaign Team Risk value did not override risk while active normal juice records existed. The game recalculated/used the player records.

Zeroing the risk inside the player record itself successfully removed that player's contribution.

## Arbitrary juice insertion

For a unique ordinary unjuiced player, the game-generated transformation is:

1. Shift bytes from the player's current name through the fixed roster boundary right by 14.
2. Consume 14 bytes of trailing XOR-zero (`3A`) padding.
3. Write the 14-byte juice record at the old name offset.
4. Increase the roster serialized-size byte by 14.
5. Increase the player's effect/status count by 1.

The player effect/status count is located at:

```text
unjuiced name - 28
```

When a 14-byte juice record is present, the name shifts right, so the same underlying count becomes:

```text
juiced name - 42
```

v1.2 re-analyzes the roster after every insertion rather than assuming stale offsets.

## Player stat/progression vector

The ten-byte decoded player modifier vector begins at:

```text
effect_count_offset + 12
```

Mapping:

| Vector index | Meaning |
|---:|---|
| 0 | Speed |
| 1 | Agility |
| 2 | Unknown / not one of the nine displayed ratings |
| 3 | Strength |
| 4 | Hands |
| 5 | Break Tackle |
| 6 | Pass/Kick |
| 7 | Tackle |
| 8 | Block |
| 9 | Resist Injury |

### Mapping evidence

Natural Speed training:

```text
displayed Speed: 70 -> 77
vector[0]:        0 -> 7
```

Nine-field probe from known baseline:

```text
vector before:
7 0 0 0 0 0 0 0 0 0

probe:
index 0 +1
index 1 +2
index 2 +3
index 3 +4
index 4 +5
index 5 +6
index 6 +7
index 7 +8
index 8 +9
```

Observed display changes:

```text
Speed       +1
Agility     +2
Strength    +4
Hands       +5
Break Tkl   +6
Pass/Kick   +7
Tackle      +8
Block       +9
Resist Inj   0
```

Therefore index `2` was the only one of those nine candidates not represented on the visible ratings screen.

Separate tenth-byte probe:

```text
vector[9]: 0 -> 10
Resist Inj: 81 -> 91
```

No other displayed rating changed.

## Custom TGH implementation

The custom TGH option is intentionally **not** a juice operation.

For each selected player:

1. Re-analyze the player after any roster insertions.
2. Confirm all serialized copies have consistent mapped stat modifiers.
3. Exclude vector index `2`.
4. Randomly select one of the nine mapped visible stats.
5. Prefer a modifier value `<= 95` so the save-side field can receive the full +5.
6. Write:

```text
new_modifier = min(old_modifier + 5, 100)
```

7. If the player has multiple serialized copies, write the same value to each copy.
8. Re-analyze the output and verify the chosen modifier.

This does not add a juice record, does not change Team Risk, and does not depend on the weekly drug selector.

### Cap limitation

The save block stores a **modifier**, not the complete built-in stock player rating.

The game-side base-rating data has not yet been decoded from `BSAV0.SAV`, so `100` is currently a cap on the mapped save-side modifier field. v1.2 does not claim this reconstructs every player's exact final displayed rating before game load.

## Native TGH investigation

The game UI on the development setup states that TGH permanently adds +5 to a random statistic.

Controlled native TGH tests did not produce such a visible/persistent +5 in the mapped stat modifiers for:

- an ordinary non-training player;
- Franchise with no training;
- an ordinary player undergoing normal Speed training.

In the last case, only the expected Speed training increase was written.

This is documented as a development-environment observation, not a universal claim about every game copy.

## Money

For each campaign v1.2 can independently patch:

1. plain 32-bit campaign-summary cash;
2. plain 32-bit global campaign cash;
3. XOR-`0x3A` positive 24-bit campaign cash;
4. XOR-`0x3A` signed negative 32-bit campaign cash.

Money spent is preserved.

Observed current-cash maximum:

```text
0xFFFFFF = 16,777,215
```

## Internal Blitz CRC

Stored:

```text
0x250 - 0x253
```

Coverage:

```text
0x254 through EOF
```

Algorithm:

- polynomial `0x04C11DB7`;
- initial value `0`;
- non-reflected / big-endian bit processing;
- result stored big-endian.

The editor rebuilds and verifies the CRC after all edits.
