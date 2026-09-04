# Reverse-Engineering Discoveries

This document records the save-format and gameplay discoveries made while building the Blitz: The League II PS3 Save Editor.

Verified development target:

```text
North American PS3 release
Title ID: BLUS30203
Stock / non-jailbroken PS3 workflow
```

The purpose of this file is to separate **what we have actually proven** from hypotheses and future experiments.

---

## Confidence labels

### Proven

Reproduced through controlled save diffs, direct save editing, or successful PS3 testing.

### Strongly supported

Multiple pieces of evidence agree, but the behavior has not been exhaustively tested in every situation.

### Open question / hypothesis

Interesting implication that has not yet been demonstrated.

---

# Save container and checksum

## Proven: BSAV0.SAV is the game payload we edit

The editor works on the decrypted:

```text
BSAV0.SAV
```

Sony's save-container encryption and `PARAM.PFD` signing are separate from the game's own internal save integrity.

The tested stock-PS3 workflow is:

```text
PS3 -> USB -> Bruteforce Save Data -> decrypt
-> edit BSAV0.SAV
-> encrypt/rebuild PFD
-> USB -> PS3
```

No HEN, CFW, or on-console save utility is required.

## Proven: internal Blitz checksum

Checksum location:

```text
0x250 - 0x253
```

Checksum coverage:

```text
0x254 through EOF
```

Algorithm:

```text
CRC32Big / non-reflected
polynomial: 0x04C11DB7
initial value: 0
stored big-endian
```

A correct PS3 container is not enough by itself. If this internal checksum is wrong, the game can reject, revert, freeze on, or otherwise mishandle the edited save.

---

# Campaign detection

## Proven: stable campaign anchor

Stable anchor:

```text
C5 1C D1 42 5B 3A 3A 3B 38 39 45 07 51 07
```

Early work incorrectly treated the next two bytes as fixed:

```text
... 51 07 3A 3A
```

Later campaign progression proved those final two bytes are mutable campaign state.

That mistake caused a valid five-campaign save to be detected as containing only two campaigns.

v1.2 uses only the stable 14-byte anchor.

Known fields relative to this anchor:

```text
Juice of the Week = anchor - 0x25
Team Risk         = anchor - 0x15
positive cash     = anchor + 0x10
```

---

# Money

## Proven: four current-cash representations must agree

Each occupied campaign contains four relevant current-cash representations:

1. Plain 32-bit big-endian campaign-summary cash.
2. Plain 32-bit big-endian global campaign cash.
3. XOR-0x3A positive 24-bit campaign cash.
4. XOR-0x3A signed negative 32-bit campaign cash.

Editing only the obvious plain copies is not sufficient.

## Proven: observed current-cash limit

The positive campaign field is 24-bit:

```text
0xFFFFFF = 16,777,215
```

The project deliberately treats that as the maximum current cash value.

Amounts above this have not been intentionally tested.

## Proven: money-spent data is separate

Current cash can be modified while preserving the game's accumulated money-spent counters.

The editor preserves money spent.

---

# XOR serialization

## Proven

A large amount of campaign/player state is bytewise obfuscated with:

```text
stored_byte XOR 0x3A
```

Most of the offsets and records in this document are easier to reason about in decoded form.

---

# Juice of the Week

## Proven: selector location

Decoded weekly-juice selector:

```text
campaign anchor - 0x25
```

## Proven: enum mapping

| Enum | Juice |
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

## Proven: the game initializes/rerolls the weekly drug separately

The selector alone does not tell us whether a new week has initialized.

Observed behavior:

1. A new week begins.
2. Opening the campaign/week menu causes the game to roll the weekly juice.
3. Backing out saves/locks that weekly state.
4. Restoring an earlier save can cause another roll.

That is why the recommended forcing workflow is to let the game initialize the week once before editing the selector.

---

# Juice effects and prices

| Juice | Normal price | Advertised / observed effect |
|---|---:|---|
| Andersol | $55,000 | Removes Clash cooldown. |
| Krextol | $40,000 | Adds +1 extra point to the skill trained that week. |
| Hoptenal | $40,000 | Reduces stamina lost from tackles by 50%. |
| Mastaphene | $60,000 | Prevents normal stamina drain from tackles/big hits; injury-related stamina loss still applies, and injury-treatment minigames do not restore stamina while active. |
| Zoltox | $50,000 | Immune to injury. |
| Letaciline | $40,000 | Successful Clash moves drain opponent Clash. |
| Ultranol | $60,000 | Increases severity of injuries caused. |
| BF-56 | $65,000 | Clash Icon per 30 yards gained on a play. |
| Cyloderm | $75,000 | Clash/Turbo drain slower; Dirty Hits cost less Clash. |
| TGH | $80,000 | Game describes it as permanently +5 to one random stat. See TGH findings below. |

---

# Player juice records

## Proven: juice record is 14 decoded bytes

Controlled records use this general structure:

```text
12 04 00 00 01 [juice slot] 00 00 00 [drug enum] [32-bit BE risk]
```

Example: Mastaphene, slot 0, normal risk 20:

```text
12 04 00 00 01 00 00 00 00 0C 00 00 00 14
```

Example: TGH, slot 0, normal risk 25:

```text
12 04 00 00 01 00 00 00 00 12 00 00 00 19
```

The record appears immediately before that serialized player name.

## Proven: normal insertion changes serialized bookkeeping

Adding one juice record causes:

```text
+14 bytes to the player's serialized data
+1 to the player's effect/status count
+14 to the surrounding serialized roster-size field
```

The file itself remains fixed-length because the insertion consumes trailing XOR-zero padding.

## Proven: the field once mistaken for Team Risk is a serialized-size value

A field near:

```text
F0 7B F2 69 3B 3A 3A 30
```

increased by exactly 14 for every inserted juice record.

It was initially mistaken for Team Risk.

It is not Team Risk.

---

# Team Risk

## Proven: real campaign Team Risk field

Decoded Team Risk:

```text
campaign anchor - 0x15
```

Examples from controlled native saves:

```text
Mastaphene:
0 players -> 0
1 player  -> 20
2 players -> 40

TGH:
3 players -> 75
```

Other controlled work also supported drug-dependent per-player values such as 15, 20, and 25.

## Proven: the risk contribution inside the player juice record is authoritative

A native Mastaphene player record normally contained:

```text
drug enum = 12
risk      = 20
```

The save was edited to:

```text
drug enum = 12
risk      = 0
```

and campaign Team Risk was also reset to zero.

Result on PS3:

- the player remained juiced with Mastaphene;
- Team Risk displayed completely empty;
- adding another normally juiced player raised Team Risk only by the new player's normal amount.

This demonstrated that the game does not automatically reconstruct the removed risk from the drug enum.

## Proven: changing only the campaign Team Risk byte is not enough

A test save contained three native TGH-juiced players with normal total risk 75.

Campaign Team Risk values were forced to different values before loading.

The game still displayed the full risk state and a player was busted during the game.

Therefore the saved campaign risk byte alone is not a useful zero-risk exploit while normal-risk player records are present.

---

# Arbitrary player juice insertion

## Proven

The editor can create a player's juice state directly without using the in-game juicing menu.

A controlled v1.1 test inserted zero-risk TGH records for three ordinary players.

On stock PS3:

- all three appeared correctly in the juicing screen;
- Team Risk was zero;
- the game completed normally;
- nobody was busted in that test;
- the following week's juicing screen initialized normally;
- the post-game save returned the temporary effect structures to the expected state.

This proved that the editor's variable-length serialization changes were accepted by the game through an entire play/save/week-transition cycle.

## Proven: editor-created Mastaphene has its gameplay effect

A separate editor-created Mastaphene test confirmed that the player actually behaved as immune to stamina loss.

This is important because it demonstrates that a record created by the editor is not merely cosmetic in the juicing menu.

## Open question: more than three juiced players

The game normally allows only three juiced players.

The save format appears capable of storing independent effect records on individual players, but more than three simultaneous player records have **not yet been tested**.

The editor currently keeps the normal three-player cap.

---


## Proven refinement: Mastaphene stamina behavior

Stock-PS3 gameplay testing refined the earlier description of Mastaphene.

Observed behavior:

- ordinary stamina drain from tackles / big hits is prevented;
- injury-related stamina loss can still reduce the player's stamina;
- the injury-treatment minigame does not restore stamina while Mastaphene is active.

So Mastaphene should **not** be described as complete immunity to all stamina loss.

The exact internal reason for the blocked recovery is still an inference; the gameplay behavior above is the proven observation.

# Native TGH behavior

## Proven on the development setup: advertised +5 could not be reproduced

The game UI explicitly describes TGH as:

```text
Permanently gain +5 in a random statistic.
```

Controlled native tests were performed on the stock PS3 / BLUS30203 copy used for this project.

### Test 1: ordinary player, no training

N. Linker received native TGH.

His displayed ratings were identical:

```text
before TGH
after TGH
after playing the game
```

No persistent +5 appeared in the mapped stat data.

### Test 2: Franchise, no training

Franchise received native TGH without training.

No displayed rating gained +5 after the game.

### Test 3: ordinary player plus normal training

J. Mims received TGH and was also assigned Speed training.

Training UI predicted:

```text
+7 Speed
```

Observed result:

```text
Speed 70 -> 77
```

No other displayed rating changed.

The save showed the normal Speed modifier changing:

```text
0 -> 7
```

with no additional TGH +5 written into the mapped visible stat modifiers.

## Important limitation

This project is **not claiming TGH is universally broken**.

The current evidence only proves that the advertised visible/persistent +5 could not be reproduced on the development setup.

Possible explanations remain:

- console-specific behavior;
- region/version differences;
- a particular disc/copy;
- another unidentified game-state requirement;
- or an actual bug in this release.

---

# Player stat/progression system

## Proven: stock player ratings are base value + persistent modifier

Controlled training demonstrated that the save stores persistent player progression/modifier values rather than simply storing every displayed rating as a full byte.

Example:

```text
J. Mims Speed:
displayed 70 -> 77
save modifier 0 -> 7
```

## Proven: ten-byte modifier vector

The decoded player modifier vector begins at:

```text
effect/status count offset + 12
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

## Proven: eight stats mapped in one probe

A player with known baseline ratings was given unique changes to the first nine candidates.

Observed changes:

```text
Speed       +1
Agility     +2
index 2     no displayed-stat change
Strength    +4
Hands       +5
Break Tkl   +6
Pass/Kick   +7
Tackle      +8
Block       +9
```

## Proven: Resist Injury mapped separately

The tenth candidate was changed:

```text
0 -> 10
```

Result:

```text
Resist Injury 81 -> 91
```

All other displayed ratings remained unchanged.

## Open question: vector index 2

Changing vector index `2` did not change any of the nine displayed player ratings.

It is clearly adjacent to the real progression vector and may represent another player attribute or state.

Possibilities such as stamina or another hidden gameplay value are hypotheses only.

---

# Custom TGH workaround

## Proven end-to-end on an ordinary player

Because native TGH did not produce the advertised visible +5 on the development setup, the editor implements the advertised effect separately.

The custom operation:

1. does **not** juice the player;
2. does **not** add a juice record;
3. does **not** affect Team Risk;
4. chooses one mapped visible stat;
5. adds +5 to that persistent modifier.

### Validation

v1.2 applied the custom effect to Raiders N. Linker.

The generated save differed from its base in only:

```text
one mapped player-stat byte
plus the required four CRC bytes
```

The randomly selected stat was:

```text
Strength
```

Save modifier:

```text
0 -> 5
```

Observed in game:

```text
Strength 21 -> 26
```

This confirms the custom TGH stat-editing mechanism works end-to-end.

## Proven: custom TGH and juicing are conceptually independent

The custom stat mutation does not require:

- TGH to be the weekly drug;
- a juice effect record;
- Team Risk;
- or any juicing operation at all.

This separation is intentional.

---

# Displayed stat ceiling

## Known from normal gameplay

Displayed player stats cap at:

```text
100
```

The project has deliberately **not** tested hacked values above 100 because overflow/wrap/gameplay behavior is unknown.

Future stat editing should therefore enforce a 100 displayed-stat ceiling.

## Current technical limitation

The save contains persistent stat modifiers, while stock-player base ratings appear to be provided elsewhere by the game.

Those base ratings have not yet been decoded from BSAV0.SAV.

That means exact absolute-value stat editing still requires more work if the editor is to calculate a player's displayed rating without the game.

---

# Roster/player identity

## Proven: ordinary roster player names are serialized in the campaign

The save contains readable, XOR-decoded first and last names for ordinary roster players, not just Franchise.

Examples encountered during development included:

```text
NELSON LINKER
ASHLEY ASHWIN
BEN ROBEY
JOSH MIMS
DAMON LARSON
```

This made dynamic roster extraction possible.

## Strongly supported: canonical player asset identifiers also exist

Other save regions contain identifiers such as:

```text
nelson_linker_2_player
ashley_ashwin_2_player
ben_robey_2_player
...
```

These may provide another stable identity source for future deeper roster editing.

---

# Franchise / two-way player serialization

## Proven: Franchise has duplicated real player-state records

Native save comparisons show that Franchise is represented by more than one real player-state copy.

During a native TGH experiment, the game inserted the same TGH effect record into **both actual Franchise player-state copies**.

There was also another occurrence of the Franchise name in a different metadata context; the game did not insert a juice record there.

This gives us the correct model for future Franchise juice insertion:

```text
juice both real Franchise player-state copies
do not juice unrelated metadata/name occurrences
```

## v1.2.4 correction: duplicated Franchise serialization is now fully decoded

The first editor-generated Franchise acceptance test exposed that the earlier
v1.2.1-v1.2.3 implementation was incomplete. The Raiders campaign softlocked.

The mistake was treating both Franchise copies like ordinary player records.

A clean native control pair now proves the correct duplicated-player model.

### Proven native behavior

For each Franchise copy, native juicing:

- inserts the same 14-byte juice record before the serialized name;
- changes a Franchise-specific list count from `3 -> 4`;
- leaves the generic name-adjacent count unchanged;
- rotates two pairs of internal references from `11/11 + 10/10` to
  `10/10 + 11/11`.

Container bookkeeping is split:

```text
primary Franchise copy:
  primary roster size +14

secondary Franchise copy:
  secondary Franchise container size +14
```

The primary roster therefore grows by only **14 bytes for one logical Franchise
player**, even though two physical juice records are written.

### Exact reproduction

Applying the corrected transformation to the Slot-3 KID FRANCHISE record in
`BSAV0_NoJuice.SAV` reproduces the native Slot-3 roster in `BSAV0_Juiced.SAV`
byte-for-byte:

```text
0 differences
```

v1.2.4 implements this native structure with zero-risk juice records.

Stock-PS3 gameplay, save/reload, and next-week transition validation has passed for the corrected editor output.


## Open question / hypothesis: custom two-way players

The duplicated Franchise records strongly suggest that Blitz may represent a two-way player as multiple roster/player-state instances associated with the same underlying player.

That raises the possibility of creating additional two-way players.

This has **not** been tested.

We do not yet know all of the position, depth-chart, identity, or cross-reference fields required to duplicate an ordinary player safely.

---

## Proven end-to-end: Franchise juicing acceptance

The corrected duplicated-Franchise implementation completed a full stock-PS3 acceptance test on the Raiders campaign.

Observed:

- save loaded normally;
- Franchise appeared juiced normally;
- Team Risk remained 0;
- Mastaphene's gameplay effect worked;
- the game completed normally;
- save/reload worked;
- the next week initialized normally;
- the post-game save returned the temporary Franchise juice structures to the normal unjuiced state.

This promotes the corrected native-style Franchise juicing model from structural reproduction to proven end-to-end behavior on the verified development setup.

## Proven: full-roster Select All TGH

A Hawgs campaign test applied the custom TGH effect to every detected roster player.

Results:

```text
logical players selected:      43
physical stat modifier writes: 44
accidental juice records:      0
```

The extra physical write is from a duplicated player-state record receiving the matching modifier update in both copies.

The edited save loaded normally, survived save/reload, and retained the selected modifier changes.


# Bust-risk observations

## Proven only for the specific tests performed

A native three-player TGH state produced a full Team Risk bar.

In one controlled game, the Raiders fullback was busted.

This demonstrates that forcing the campaign Team Risk byte to zero while leaving normal-risk player records intact does not eliminate enforcement.

It does **not** prove that a full Team Risk bar guarantees every player, or even guarantees some player, will always be busted.

By contrast, editor-created zero-risk juice records produced an empty Team Risk bar and no bust occurred in the multi-player test performed.

---

# Things deliberately not implemented yet

- More than three simultaneous juiced players.
- Full manual player-stat editing.
- Absolute displayed-stat reconstruction for stock players.
- Editing or exposing the unknown modifier-vector index `2`.
- Custom two-way players.
- Reputation editing.
- Sponsor editing.

These are separate from the save structures already proven for money and juicing.

---

# Current high-level picture

The project began as a money hack.

The save format is now understood well enough to support:

```text
per-campaign cash
weekly drug selection
dynamic roster detection
existing juice detection
arbitrary ordinary-player juice insertion
zero-risk juice records
persistent player-stat modifiers
custom +5 stat effects
```

Additional roster and progression features appear technically possible, but should be added only after controlled tests establish their serialization and gameplay behavior.
