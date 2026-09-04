# Blitz: The League II PS3 Save Editor v1.3

Offline save editor for the PlayStation 3 version of **Blitz: The League II**.

Verified save format: **North American BLUS30203**.

The normal interface is the self-contained file:

```text
Blitz2SaveEditor.html
```

Open it in a modern desktop browser. No web server or internet connection is required.


## Reverse-engineering discoveries

The project now has a dedicated research log:

**`DISCOVERIES.md`**

It separates proven save-format/gameplay findings from strong inferences and open hypotheses. It includes the money format, Juice of the Week enums, Team Risk behavior, 14-byte player juice records, player stat mapping, native TGH testing, the custom-TGH validation, Franchise's duplicated player-state records, and remaining questions such as the unknown player modifier and possible custom two-way players.


## v1.3 public release

v1.3 is the first public release since v1.0. The v1.1 through v1.2.5 builds were internal development iterations used to reverse-engineer and validate the expanded editor.

v1.3 includes:

- independent per-campaign cash editing;
- Juice of the Week editing with effect and price descriptions;
- dynamic roster detection;
- zero-risk cleanup for existing juice records;
- arbitrary zero-risk juice insertion for ordinary roster players;
- stock-PS3 validated native-style Franchise juicing across both real player-state copies;
- custom TGH +5 stat effects;
- Select All TGH Effects for every detected roster player, including backups;
- internal Blitz CRC repair and output verification;
- completely offline/local operation.

### Final acceptance tests

**Raiders — Franchise juicing**

The corrected duplicated-Franchise serialization passed the complete stock-PS3 cycle:

- save loaded normally;
- Franchise appeared juiced normally;
- Team Risk stayed at 0;
- Mastaphene's gameplay effect worked;
- the game completed normally;
- save/reload worked;
- the next week initialized normally;
- the post-game save returned the temporary Franchise juice structures to normal.

**Hawgs — Select All TGH Effects**

The full-roster test selected all **43 detected logical roster players**, including backups. One duplicated player-state record caused **44 physical stat modifier writes**.

Validation confirmed:

- every selected logical player received the intended +5 save-side modifier;
- duplicated player-state copies received matching updates;
- no Hawgs juice records were created;
- the save loaded normally;
- the campaign remained healthy after save/reload;
- the modifier changes persisted.

## Internal v1.2.4 development changes

### Native Franchise serialization fix

The first editor-generated Franchise acceptance test on the Raiders softlocked while loading the campaign.

The failure exposed an important mistake in the v1.2.1-v1.2.3 implementation: a duplicated Franchise player cannot be serialized as two ordinary player insertions.

A controlled native pair (`BSAV0_NoJuice.SAV` -> `BSAV0_Juiced.SAV`) provides a clean duplicated-Franchise case in Slot 3. Reproducing the newly decoded native rules now generates the native Slot-3 roster **byte-for-byte with zero differences**.

For a duplicated Franchise player, the native game:

- inserts the same 14-byte juice record before both real player-state names;
- increases the **primary roster size by only 14 bytes**, not 28;
- increases a separate **secondary Franchise container size by 14 bytes** for the second copy;
- leaves the generic name-adjacent Franchise count unchanged;
- increments a Franchise-specific list count in each copy;
- rotates four internal `0x10`/`0x11` references in each Franchise structure exactly as the native game does;
- uses the same juice-slot index on both copies.

v1.2.4 implements this native model with risk `0`.

## What was new in v1.2.3

### Select All TGH render bug fixed

v1.2.2 introduced a JavaScript render-time error:

```text
Campaign is not defined
```

The save file was not the problem. The new Select All button referenced
`campaign.index` even though the campaign-rendering scope uses `c`.

v1.2.3 fixes the button to use the campaign's existing `slotIndex` and
simplifies Select All so it targets the already-existing per-player TGH
checkboxes by their `data-slot` value.

No save-format logic changed in this fix.

## What was new in v1.2.2

### Select all custom TGH effects

Each campaign now includes a **Select All TGH Effects** button.

It checks **Apply effects of TGH?** for every detected roster player in that campaign, including backups.

This does **not** select players for Juice and does not change Juice of the Week or Team Risk. It only saves you from manually checking every TGH-effect box.

## What was new in v1.2.1

### Franchise juicing enabled

v1.2.1 removes the editor-side restriction that prevented juice insertion on Franchise-style duplicated player records.

Native save analysis proved that when the game juices Franchise, it writes the same 14-byte juice effect to **both real Franchise player-state copies**, using the same drug and the same juice-slot index.

The editor now mirrors that behavior:

- Franchise counts as **one** player toward the normal three-player juicing limit.
- The same zero-risk juice record is inserted into both real Franchise player-state copies.
- The generic Franchise name-adjacent count is left unchanged, matching native serialization.
- The primary roster grows by 14 bytes and the secondary Franchise container grows by 14 bytes.
- Franchise-specific list counts and internal references are updated exactly as observed in the native save pair.
- The unrelated Franchise-name/metadata occurrence is not touched.
- Output verification requires every real Franchise player-state copy to contain the expected zero-risk record.

This implementation reproduces native save behavior and has completed stock-PS3 gameplay, save/reload, and next-week transition validation.

## What was new in v1.2

- Cash is now editable **independently for each detected campaign** instead of using one global target.
- The Juice of the Week selector now shows the drug's known gameplay effect and normal in-game price.
- The v1.1 campaign-detection hotfix is integrated. The detector now uses the stable 14-byte campaign anchor instead of incorrectly treating two mutable campaign-state bytes as part of the signature.
- Arbitrary zero-risk juice insertion is retained after successful stock-PS3 gameplay/save/week-transition testing.
- The player progression/stat block has now been mapped for all nine visible ratings.
- Added an experimental, completely separate **Apply effects of TGH?** option.
- The custom TGH option does **not** add a juice record. It only adds +5 to one random mapped visible stat modifier.
- Custom TGH and normal juicing can be used independently or together on the same player.
- The custom TGH stat change is applied to all serialized copies of a duplicated Franchise-style player record, while juice-record insertion into duplicated Franchise records remains disabled.

## Feature status

### Stable / validated

- Four-copy current-cash editing.
- Per-campaign cash targets.
- Internal Blitz CRC repair.
- Juice of the Week detection and editing.
- Roster-name detection from the save itself.
- Existing juice-record detection.
- Zeroing the per-player juice risk contribution.
- Resetting campaign Team Risk.
- Arbitrary juice-record insertion for unique ordinary player records.
- Editor-created zero-risk juice records surviving gameplay, game save, week transition, and reload.
- Editor-created Mastaphene producing its observed normal-stamina-drain prevention gameplay effect.
- Custom **Apply effects of TGH?** successfully changing an ordinary player's selected displayed stat by +5 without juicing him.
- Select All TGH Effects has been validated across a full detected 43-player roster, including backups and a duplicated player-state record.
- Native-style editor-created Franchise juicing has completed gameplay, save/reload, and next-week transition validation on stock PS3.

### Known limitations / future work

- The save-side stat modifier map is proven, but the game's built-in base ratings are not yet decoded from the save.
- Juice insertion remains capped at the normal in-game total of three **logical players**.
- Franchise-style two-copy players are supported and stock-PS3 validated. Franchise counts as one juiced player while the editor writes matching native-style records to both real player-state copies.

## TGH compatibility finding

The game itself describes TGH as:

> Permanently gain +5 in a random statistic.

During controlled testing on the **stock PS3, BLUS30203 game copy, and disc used for this project**, native TGH could be selected and administered normally, but the advertised visible/persistent +5 could not be reproduced.

Tests included:

- TGH on an ordinary player who was not training.
- TGH on Franchise while Franchise was not training.
- TGH on an ordinary player who was simultaneously assigned normal Speed training.

In the training test, the ordinary player received exactly the training increase predicted by the training UI and no additional visible +5. Save-file comparisons also showed the normal training modifier being written, while no analogous TGH +5 appeared in the mapped visible stat modifiers.

**This project is not claiming that TGH is universally broken in every copy of Blitz: The League II.** We do not currently know whether the behavior is caused by:

- the particular console;
- game version or region;
- the particular disc/copy;
- some other game-state condition we have not identified;
- or an actual bug in this release.

Because the advertised native effect could not be reproduced on the development setup, v1.2 adds an optional custom implementation.

## Custom "Apply effects of TGH?"

This control is deliberately separate from juicing.

Checking **Apply effects of TGH?** for a player:

1. Does **not** add a juice record.
2. Does **not** change the Juice of the Week.
3. Does **not** change Team Risk.
4. Randomly chooses one of the nine mapped visible player stats.
5. Adds `+5` to that stat's persistent save-side modifier.
6. Updates every serialized copy when the player has a duplicated Franchise-style record.

You can therefore:

- apply the custom TGH +5 without juicing the player;
- juice a player without applying the custom TGH +5;
- or do both.


### Custom TGH validation

A controlled v1.2 test applied the custom TGH effect to **Raiders N. Linker** without juicing him.

The editor randomly selected **Strength**.

Save comparison showed:

```text
Strength modifier: 0 -> 5
```

with no juice record, Team Risk change, or unrelated player-data change.

In game:

```text
Strength: 21 -> 26
```

This confirms that the custom TGH stat mutation works end-to-end on an ordinary roster player.

### Stat cap note

Normal gameplay displays player ratings no higher than **100**.

v1.2 never writes a mapped save-side stat modifier above `100`. When possible it chooses a field that can receive the full +5 without the modifier itself passing 100.

The game combines these save-side modifiers with built-in player base ratings (and potentially other bonuses). Those built-in base-rating values have **not yet been decoded from this save structure**, so v1.2 does not pretend it can mathematically reconstruct every player's final displayed rating before the game loads it.

No intentional test of hacked displayed ratings above 100 has been performed.

## Player stat modifier map

A controlled training test and two direct save probes mapped the persistent player modifier block.

Relative to the player's ten-byte modifier vector:

| Vector index | Visible stat |
|---:|---|
| 0 | Speed |
| 1 | Agility |
| 2 | **Unknown / not displayed** |
| 3 | Strength |
| 4 | Hands |
| 5 | Break Tackle |
| 6 | Pass/Kick |
| 7 | Tackle |
| 8 | Block |
| 9 | Resist Injury |

The unknown index `2` changed during a probe without changing any of the nine ratings on the player screen. v1.2 does not touch it when applying the custom TGH effect.

### How the mapping was proven

One controlled player had normal Speed training resolve from:

```text
Speed 70 -> 77
```

and the first modifier byte changed:

```text
0 -> 7
```

A later probe gave the first nine candidate bytes unique deltas. The resulting visible changes mapped Speed, Agility, Strength, Hands, Break Tackle, Pass/Kick, Tackle, and Block in one screenshot.

A final isolated probe changed the tenth candidate:

```text
0 -> 10
```

and Resist Injury changed:

```text
81 -> 91
```

with every other displayed rating unchanged.

## Juice of the Week effects

| Juice | Normal price | Effect |
|---|---:|---|
| Andersol | $55,000 | Removes Clash cooldown. |
| Krextol | $40,000 | Adds +1 extra point to the skill trained that week. |
| Hoptenal | $40,000 | Reduces stamina lost from tackles by 50%. |
| Mastaphene | $60,000 | Prevents normal stamina drain from tackles/big hits, but injury-related stamina loss still applies. Injury-treatment minigames also do not restore stamina while the effect is active. |
| Zoltox | $50,000 | Makes the player immune to injury. |
| Letaciline | $40,000 | Successful Clash moves drain the opponent's Clash meter. |
| Ultranol | $60,000 | Increases the severity of injuries caused. |
| BF-56 | $65,000 | Ball carrier gains a Clash Icon for every 30 yards gained on a play. |
| Cyloderm | $75,000 | Clash/Turbo drain 50% slower, and Dirty Hits cost 50% less Clash. |
| TGH | $80,000 | Advertised as permanently +5 to one random statistic. See the compatibility note above. |

## Zero-risk juice records

A normal juice record contains the drug enum and a 32-bit risk contribution.

For example, a decoded Mastaphene record can end in:

```text
0C 00 00 00 14
```

where:

```text
0C          = Mastaphene enum 12
00 00 00 14 = risk 20
```

Changing only the risk contribution to zero while retaining the drug enum was tested on PS3. The player remained juiced, Team Risk became empty, and later normally juicing another player added only that new player's risk.

New records created by the editor therefore use risk `0`.


## Franchise juicing implementation

Native TGH saves showed that Franchise has two real player-state copies in the active roster serialization. The game wrote the same TGH record to both copies:

```text
drug enum: TGH
juice slot index: same on both copies
risk: same on both copies
```

v1.2.1 reproduces that model with risk `0`.

Local structural validation on the known Injuns post-game save confirmed:

```text
Franchise logical players added: 1
serialized juice records added: 2
roster serialized-size delta: +28
both Franchise effect counts: +1
same juice-slot index on both copies
risk: 0 on both copies
```

A second local stress test inserted:

```text
Franchise + two ordinary players
```

which produced the normal logical total of three juiced players while correctly serializing four physical juice records (two for Franchise and one for each ordinary player).

This implementation has completed stock-PS3 gameplay, save/reload, and next-week transition validation.

## Arbitrary juice insertion

Controlled save diffs showed that the game juices an ordinary player by:

1. inserting a 14-byte effect record immediately before the player's serialized name;
2. shifting the following roster data by 14 bytes;
3. consuming 14 bytes of trailing XOR-zero padding;
4. increasing the roster serialized-size byte by 14;
5. increasing that player's effect/status count by 1.

The v1.1 editor reconstruction was subsequently tested on a stock PS3 with multiple editor-created players. The inserted players appeared normally in the juicing screen, Team Risk remained zero, a game completed successfully, nobody was busted in that test, and the next week's juice state initialized normally.

Editor-created Mastaphene was separately confirmed to produce its intended stamina behavior.

v1.2 therefore keeps the feature and still enforces the normal three-player total.

v1.2.1 implements the native Franchise behavior discovered after the original v1.2 build: matching juice records are written to both real Franchise player-state copies. The normal three-player cap counts Franchise as one logical player.

## Campaign detection fix

Early v1.1 builds used this 16-byte sequence as though every byte were fixed:

```text
C5 1C D1 42 5B 3A 3A 3B 38 39 45 07 51 07 3A 3A
```

Later campaign progress proved that the final two bytes can change.

v1.2 uses only the stable 14-byte anchor:

```text
C5 1C D1 42 5B 3A 3A 3B 38 39 45 07 51 07
```

The positive 24-bit cash field remains at:

```text
anchor + 0x10
```

This fixed the case where a valid five-campaign save was incorrectly shown as containing only two campaigns.

## Per-campaign money editing

Each detected campaign now has its own:

- **Edit current cash for this campaign** checkbox;
- target cash field.

The editor still updates all four known current-cash representations for any enabled campaign:

1. plain 32-bit campaign-summary cash;
2. plain 32-bit global campaign cash;
3. XOR-`0x3A` positive 24-bit campaign cash;
4. XOR-`0x3A` signed negative 32-bit campaign cash.

Money spent is preserved.

The observed current-cash limit remains:

```text
0xFFFFFF = 16,777,215
```

## Juice insertion does not charge cash

When the editor itself creates a juice record, it does not subtract the drug price and does not increment money spent.

The normal price is shown in the UI for reference only.

## Stock-PS3 workflow

This editor modifies the game's **decrypted** `BSAV0.SAV`.

It does not decrypt Sony's save container and does not resign `PARAM.PFD`.

The tested workflow remains:

```text
PS3 XMB
  -> copy save to USB
Windows PC
  -> Bruteforce Save Data 4.7.5
  -> decrypt save
  -> edit decrypted BSAV0.SAV with Blitz2SaveEditor.html
  -> replace the working BSAV0.SAV
  -> update/encrypt/rebuild PFD
USB
  -> copy save back using normal PS3 Saved Data Utility
```

No HEN, CFW, or on-console Apollo installation is required for this workflow.

## Important weekly-juice behavior

The game can reroll Juice of the Week when a new week is initialized.

For reliable forced-drug editing:

1. enter the campaign at the start of the week;
2. let the game initialize the weekly juice;
3. back out so that state saves;
4. decrypt and edit the save on PC;
5. return it to PS3.

## Internal Blitz checksum

The game's internal checksum is stored at:

```text
0x250 - 0x253
```

It covers:

```text
0x254 through end-of-file
```

Algorithm:

- CRC32Big / non-reflected;
- polynomial `0x04C11DB7`;
- initial value `0`;
- stored big-endian.

The browser rebuilds this checksum after all edits and re-analyzes the generated save before download.

## Full stat editing

The nine visible modifier fields are now mapped well enough that full manual stat editing is technically plausible.

v1.2 deliberately does **not** expose a full stat editor yet. The next problem to solve is how to reconstruct or safely account for each player's built-in base ratings and other possible bonuses so an absolute displayed-value editor can enforce the game's 100-point ceiling correctly.

## Privacy

The editor is entirely local. It contains no upload code, analytics, telemetry, remote scripts, or network requests.

No development/test saves, PSN/account identifiers, console identifiers, user-created Franchise names, usernames, or local machine paths are included in this release.

See `PRIVACY.md`.

## License

MIT License. See `LICENSE`.

Copyright (c) 2026 hickoryit41
