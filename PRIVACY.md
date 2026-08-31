# Privacy

## Short version

The Blitz: The League II Money Tool does not transmit your save anywhere.

`Blitz2MoneyTool.html` is a self-contained local HTML/JavaScript file. When you choose `BSAV0.SAV`, your browser reads it locally, modifies a copy in memory, and creates a local download.

## The editor does not contain

- Any uploaded PS3 save from development/testing
- `PARAM.SFO` or `PARAM.PFD`
- PS3 account IDs
- console IDs
- PSN usernames
- player/team names from test saves
- Windows usernames or local file paths from development
- analytics IDs
- telemetry endpoints
- tracking pixels
- remote JavaScript libraries

## Network behavior

The editor contains no `fetch`, `XMLHttpRequest`, WebSocket, analytics, or remote-script code.

There is one normal clickable help hyperlink to The Project Lounge's Bruteforce guide. The editor does not open that page automatically. If you click an external link, your browser visits that website normally; that visit is separate from the save editor and is governed by that site's privacy practices.

## Publishing this release

This public package intentionally contains only source/docs and no sample save files. Anyone redistributing it should keep it that way unless they have permission to distribute a particular save.
