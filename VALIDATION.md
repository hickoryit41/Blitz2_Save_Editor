# v1.3 Release Acceptance

## Raiders Franchise juicing — PASS

Exact corrected test:

```text
base:     BSAV0_Before_Edits(1).SAV
campaign: Raiders / Slot 1
player:   CLAUDE BROWN (Franchise)
juice:    Mastaphene
risk:     0
```

Stock-PS3 result:

```text
save loads properly                         PASS
Franchise appears juiced normally           PASS
Team Risk remains 0                         PASS
Mastaphene effect works in gameplay          PASS
game completes normally                     PASS
save/reload works                            PASS
next week initializes normally               PASS
post-game Franchise juice structures clear   PASS
```

## Hawgs Select All TGH — PASS

Save-level verification:

```text
logical roster players selected: 43
physical stat modifier writes:    44
accidental Hawgs juice records:   0
```

Result:

```text
all detected roster players selected         PASS
backups included                              PASS
no accidental juice records                  PASS
save loads normally                          PASS
selected +5 modifiers written correctly      PASS
campaign survives save/reload                PASS
post-save modifier changes persist           PASS
```

## Release decision

The acceptance blockers defined for the experimental branch have passed. v1.3 removes the Experimental label for the verified BLUS30203 stock-PS3 + Bruteforce Save Data workflow.



## Mastaphene behavior refinement

During the successful Raiders Franchise acceptance test, Mastaphene was observed more precisely:

```text
normal stamina drain from tackles / big hits -> prevented
injury-related stamina loss                 -> still applies
injury-treatment minigame stamina recovery  -> does not restore stamina while active
```

This supersedes the earlier shorthand description that Mastaphene makes a player fully immune to stamina loss.

## v1.2.4 Franchise softlock root cause and native reproduction

### Failed acceptance test

Base:

```text
BSAV0_Before_Edits(1).SAV
```

Raiders / Slot 1:

```text
Franchise: CLAUDE BROWN
drug: Mastaphene
risk: 0
physical records requested: 2
```

The v1.2.3 output softlocked when loading the Raiders campaign.

### Root cause

The v1.2.3 editor treated both Franchise player-state copies as ordinary records.
That produced:

```text
primary roster size: +28
generic Franchise counts: +1 on each copy
```

Native serialization does neither.

### Native control

The controlled pair:

```text
BSAV0_NoJuice.SAV
BSAV0_Juiced.SAV
```

contains Slot 3 with KID FRANCHISE as the only logical juiced player.

Native behavior is:

```text
primary roster size:             +14
secondary Franchise size:        +14
Franchise special list count:    3 -> 4 on both copies
generic name-adjacent count:     unchanged
internal refs:                   11/11 + 10/10 -> 10/10 + 11/11
physical juice records:          2
shared juice-slot index:         yes
```

A corrected local transformation applied to `BSAV0_NoJuice.SAV` reproduces the
entire native Slot-3 roster region in `BSAV0_Juiced.SAV` with:

```text
0 byte differences
```

This is the basis of the v1.2.4 Franchise implementation.


## v1.2.3 Select All render regression

The v1.2.2 Select All button used an undefined template variable:

```text
campaign.index
```

The surrounding render function uses:

```text
c.slotIndex
```

This caused the browser to throw:

```text
Campaign is not defined
```

before campaigns could render.

v1.2.3 replaces the bad reference with `c.slotIndex` and uses the existing
`.tghPick[data-slot="..."]` attributes for campaign-scoped Select All.

Static validation confirms there are no remaining `campaign.index` references.

# v1.3 Validation Notes

## Campaign detection

A progressed save that v1.1 originally reported as only two campaigns was inspected.

Actual result:

- all five campaign structures were intact;
- the internal Blitz CRC was valid;
- the old 16-byte signature matched only two slots;
- the stable first 14 bytes matched all five slots.

v1.2 uses the stable 14-byte anchor.


## Franchise insertion local validation

The known Injuns post-game save contains one two-copy Franchise-style player.

The v1.2.1 insertion routine was exercised against that save with Mastaphene.

Result:

```text
detected real Franchise copies: 2
logical juiced players added:   1
physical juice records added:   2
juice slot index:               0 on both copies
risk:                           0 on both copies
serialized roster-size change:  +28
```

Both copies re-parsed successfully as juiced after insertion.

A second local stress test selected:

```text
Franchise
N. Linker
K. Guillotte
```

The output re-parsed as:

```text
logical juiced players: 3
physical juice records: 4
```

with the Franchise records sharing slot index `0`, and the ordinary players receiving slot indexes `1` and `2`.

This validates the serialization logic locally. An editor-generated Franchise save still needs the final stock-PS3 gameplay/save/reload test.

## Arbitrary zero-risk insertion

A v1.1 editor-generated test inserted TGH records for three ordinary players.

On a stock PS3:

- all three appeared correctly in the juicing screen;
- Team Risk displayed as zero;
- the game completed normally;
- nobody was busted in that test;
- the next week's juicing screen initialized normally.

The post-game save returned the temporary juice structures to the expected next-week state.

## Mastaphene behavior

Editor-created Mastaphene was tested separately.

The selected player retained the editor-created juice state and Mastaphene produced its observed stamina behavior.

This is important because it demonstrates that at least one passive juice effect is driven correctly by the editor-created player juice record.

## Native TGH tests

Native TGH was administered by the game itself under several controlled conditions.

### Ordinary player, no training

The player showed TGH in the juicing screen but no visible stat changed before or after the game.

### Franchise, no training

Franchise showed TGH but no visible +5 appeared after the game.

### Ordinary player plus normal Speed training

The player started at Speed 70.

Training UI predicted:

```text
+7 Speed
```

After the game:

```text
Speed = 77
```

Every other displayed rating was unchanged.

Save comparison showed the mapped Speed modifier changing:

```text
0 -> 7
```

No separate TGH +5 appeared in the mapped visible stat vector.

These tests justify the optional custom TGH workaround but do not prove that native TGH fails on every console, region, version, or disc.

## Stat mapping probe

Known baseline for the controlled player:

```text
Speed       77
Agility     64
Strength    36
Hands       71
Pass/Kick   33
Break Tkl   28
Tackle      31
Block       42
Resist Inj  81
```

The first nine candidate modifier bytes were changed by unique amounts.

Result:

```text
Speed       78  (+1)
Agility     66  (+2)
Strength    40  (+4)
Hands       76  (+5)
Pass/Kick   40  (+7)
Break Tkl   34  (+6)
Tackle      39  (+8)
Block       51  (+9)
Resist Inj  81  (+0)
```

This mapped eight visible stats and showed that candidate index `2` was not one of the nine displayed ratings.

## Resist Injury probe

The next candidate byte was changed:

```text
0 -> 10
```

Result:

```text
Resist Injury 81 -> 91
```

Every other displayed rating remained unchanged.

This completed the nine-visible-stat map.

## v1.2 local code validation

Before packaging:

- the standalone HTML JavaScript passed `node --check`;
- the stable campaign anchor was validated against progressed five-slot saves;
- per-campaign cash patching was re-tested in the core logic;
- zero-risk insertion was re-tested in the core logic;
- custom TGH stat writes were re-analyzed and verified against the mapped player vector;
- duplicated Franchise-style stat records were confirmed to receive the same custom TGH modifier update in both serialized copies;
- the final HTML contains no upload code, remote scripts, `fetch`, `XMLHttpRequest`, or telemetry calls.
