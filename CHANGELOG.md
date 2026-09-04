# Changelog

> **Publishing note:** v1.0 was the previous public release. v1.1 through v1.2.5 were internal development iterations. v1.3 is the current public release.

## v1.3 — 2026-09-04

- First public release since v1.0.
- Removed the Experimental label after completing the final stock-PS3 acceptance tests.
- Promoted independent per-campaign cash editing.
- Promoted Juice of the Week editing.
- Promoted arbitrary zero-risk juice insertion for ordinary roster players.
- Promoted native-style zero-risk Franchise juicing after the corrected duplicated-Franchise model completed:
  - normal campaign load;
  - normal Franchise juice display;
  - Team Risk 0;
  - working gameplay effect;
  - game completion;
  - save/reload;
  - next-week initialization;
  - clean post-game removal of the temporary Franchise juice structures.
- Promoted custom TGH +5 effects.
- Promoted Select All TGH Effects after validating a full detected Hawgs roster:
  - 43 logical roster players selected, including backups;
  - 44 physical stat modifier writes due to one duplicated player-state record;
  - no accidental juice records;
  - normal load and save/reload;
  - persistent modifier changes.
- Retained the normal three-logical-player juice cap.
- Retained the known limitation that the save stores stat modifiers rather than decoded stock base ratings, so full absolute stat editing is not exposed.
- Mastaphene description reflects observed behavior: normal tackle/big-hit stamina drain is prevented, while injury-related stamina loss still applies and injury-treatment minigames do not restore stamina while active.
- Editor remains completely offline/local.
- MIT License, Copyright (c) 2026 hickoryit41.

## v1.2.5 EXPERIMENTAL — 2026-09-04

- Refined Mastaphene's documented gameplay behavior based on stock-PS3 testing.
- Replaced the overly broad "immune to stamina loss" description.
- Documented that normal stamina drain from tackles/big hits is prevented.
- Documented that injury-related stamina loss still applies.
- Documented that injury-treatment minigames do not restore stamina while Mastaphene is active.
- No save-format logic changed.

## v1.2.4 EXPERIMENTAL — 2026-09-04

- Fixed the Franchise juicing serialization that caused the Raiders acceptance-test save to softlock.
- Invalidated the earlier assumption that two-copy Franchise juicing can be implemented as two ordinary insertions.
- Decoded native duplicated-Franchise bookkeeping using `BSAV0_NoJuice.SAV` -> `BSAV0_Juiced.SAV`.
- Correct Franchise behavior:
  - primary roster size grows by 14 bytes for one logical Franchise player;
  - secondary Franchise container size grows independently by 14 bytes;
  - generic name-adjacent Franchise counts remain unchanged;
  - Franchise-specific list counts change 3 -> 4 on both copies;
  - four internal 0x10/0x11 references rotate to match native serialization;
  - matching zero-risk juice records are inserted into both copies with the same juice-slot index.
- Corrected implementation reproduced the native Slot-3 KID FRANCHISE roster byte-for-byte with zero differences.
- Kept ordinary one-copy juice insertion on the previously field-tested path.

## v1.2.3 EXPERIMENTAL — 2026-09-04

- Fixed the v1.2.2 render-time `Campaign is not defined` error.
- Root cause: the Select All TGH button referenced `campaign.index` inside a template whose campaign variable is `c`.
- The button now uses `c.slotIndex`.
- Simplified Select All TGH selection to target existing `.tghPick[data-slot="..."]` checkboxes.
- No save-format logic changed.

## v1.2.2 EXPERIMENTAL — 2026-09-04

- Added **Select All TGH Effects** to each campaign.
- The button selects the custom **Apply effects of TGH?** checkbox for every detected roster player in that campaign, including backups.
- The control is separate from Juice selection and does not change Juice of the Week, Team Risk, or the three-player juicing cap.

## v1.2.1 EXPERIMENTAL — 2026-09-04

- Removed the editor-side Franchise juicing restriction.
- Added the first duplicated-Franchise insertion implementation.
- This implementation was later proven incomplete by the Raiders softlock and superseded by the native serialization model in v1.2.4.
- Franchise counted as one logical player toward the normal three-player juice limit.
- Added output verification for duplicated player-state copies.

## v1.2 EXPERIMENTAL — 2026-09-04

- Integrated the stable 14-byte campaign-detection hotfix.
- Fixed progressed saves that could incorrectly appear to contain only two campaigns.
- Replaced global cash editing with independent per-campaign cash controls.
- Added Juice of the Week effect descriptions and normal in-game prices.
- Promoted arbitrary zero-risk juice insertion after stock-PS3 gameplay/save/week-transition testing.
- Mapped all nine visible save-side player stat modifiers.
- Identified one unresolved modifier-vector byte that does not change any of the nine displayed ratings.
- Added **Apply effects of TGH?** per-player controls.
- Custom TGH is independent from juice-record insertion.
- Custom TGH updates all serialized copies of duplicated Franchise-style records.
- Added the build summary showing which random stat received the custom TGH change.
- Added `DISCOVERIES.md`.

## v1.1 EXPERIMENTAL — 2026-09-03

- Expanded the v1.0 money utility into a broader offline save editor.
- Added Juice of the Week detection and editing.
- Added dynamic roster-name parsing.
- Added existing juice-record detection.
- Added zero-risk editing.
- Added arbitrary-player juice insertion for unique ordinary roster records.
- Added structural insertion safety checks.
- Preserved CRC repair and output verification.

## v1.0

- Initial public offline BLUS30203 money editor.
- Patched all four known current-cash representations.
- Preserved money-spent counters.
- Rebuilt the internal Blitz CRC.
