# Blitz: The League II Money Tool v1.0

Offline campaign-money editor for the PlayStation 3 version of **Blitz: The League II**.

## What it does

The tool opens a **decrypted** `BSAV0.SAV`, detects the occupied campaign slots, shows their current cash and money-spent values, changes current cash to the amount you choose, repairs all known duplicated/obfuscated cash fields, and rebuilds the game's internal checksum.

It has been verified on the North American PS3 release **BLUS30203**. Other regions are currently **untested and unsupported** even if they happen to work.

The editor is a single local HTML file. It contains no upload code, analytics, telemetry, remote scripts, or network requests. Selecting a save reads it locally in your browser. The only external link in the page is a help link that opens The Project Lounge guide if you click it.

## What it does NOT do

This tool does **not** decrypt Sony's PS3 save encryption and does **not** rebuild/resign `PARAM.PFD`. You still need a PC save utility such as **Bruteforce Save Data 4.7.5** before and after using this editor.

You do **not** need to jailbreak the PS3 for the workflow described here. A stock PS3 can copy the save to USB and copy the finished save back through the normal **Saved Data Utility (PS3)**.

---

# Before you begin

You need:

- A PlayStation 3 and Blitz: The League II.
- A USB storage device readable by the PS3. FAT32 is the simplest choice.
- A Windows PC.
- Bruteforce Save Data 4.7.5.
- `Blitz2MoneyTool.html` from this release.
- One backup you promise not to touch.

**Seriously: make a backup.** Save editing is inherently experimental. Keep an untouched copy of the entire PS3 save folder, not just `BSAV0.SAV`.

Bruteforce Save Data is old third-party software distributed outside normal app stores. Use the linked reference guide, keep antivirus protections enabled, and treat any third-party download as software you install/run at your own risk.

---

# Part 1 — Copy your Blitz save from PS3 to USB

1. Plug the USB drive into the PS3.
2. On the PS3 XMB, go to **Game**.
3. Open **Saved Data Utility (PS3)**.
4. Highlight **Blitz: The League II**.
5. Press **Triangle**.
6. Choose **Copy**.
7. Choose the USB device.
8. Wait for the copy to finish.
9. Shut down/eject normally, then plug the USB into the Windows PC.

On the USB, PS3 save data normally lives under:

```text
USB:\PS3\SAVEDATA\
```

The verified North American Blitz save uses title ID:

```text
BLUS30203
```

---

# Part 2 — Make backups on the PC

Do not work directly on the only USB copy.

A simple folder layout is:

```text
C:\Blitz2MoneyMod\
├── Original\
└── Working\
```

1. Copy the **entire** PS3 save tree from the USB into `Original`.
2. Copy `Original` again into `Working`.
3. Never edit `Original`.
4. Point Bruteforce at the copy under `Working`.

If anything goes wrong, delete the broken working copy and start again from `Original`.

---

# Part 3 — Set up Bruteforce Save Data 4.7.5

For the Bruteforce portion, this release follows the detailed Windows 10/11 walkthrough published by **The Project Lounge**:

https://theprojectlounge.co.uk/how-to-share-and-mod-playstation-3-game-saves/

That guide provides the Bruteforce 4.7.5 download link and screenshots. These are the important points for this Blitz workflow:

1. Download **Bruteforce Save Data 4.7.5** using the link on the guide above.
2. Extract the download with **Right-click > Extract All**.
3. Use the included/prepared folder named approximately:

   ```text
   BruteforceSaveData_v4.7.5
   ```

4. **Do not run the included 4.7.4 installer on Windows 10/11 unless you have a specific reason.** The guide recommends using the prepared 4.7.5 folder directly because the older installer caused problems in its testing.
5. Run:

   ```text
   BruteforceSaveData.exe
   ```

6. If Bruteforce shows a **Cheats Repository** update window, **DO NOT CLICK DOWNLOAD**. The guide warns that the downloaded repository data is currently in the wrong format and can stop Bruteforce from decrypting saves. Uncheck **Check updates on start up** and close the prompt.
7. If Windows reports that `msvbvm50.dll` is missing, use the included Visual Basic 5 Runtime installer. Do not install it preemptively if Bruteforce already launches.
8. If Bruteforce gives an initial first-run information prompt, close it.
9. If it asks whether to create a template immediately, choose **No** for that prompt.
10. Click the **...** browse button and choose the folder that contains your working `PS3` directory. Example:

    ```text
    C:\Blitz2MoneyMod\Working
    ```

    with the save underneath it like:

    ```text
    C:\Blitz2MoneyMod\Working\PS3\SAVEDATA\BLUS30203\...
    ```

11. Press **Ctrl+T** in Bruteforce, confirm creation of a profile/template, and give it a simple name such as `Main`.

### Things you should NOT do for this guide

The Project Lounge article also explains how to import **somebody else's** save, unlock saves for other profiles, and change game regions. That is not what this editor needs when you are editing your own Blitz save for the same PS3/profile.

For this workflow, do **not** randomly use:

- `Unlock Save to work on any PS3 account`
- `Change Title ID/Region`
- account-ID changes
- region conversion
- unrelated built-in cheats

Keep the operation as boring as possible: decrypt your own save, patch `BSAV0.SAV`, then re-encrypt/rebuild it.

---

# Part 4 — Decrypt the Blitz save

1. In Bruteforce, select the **Blitz: The League II** save.
2. Click:

   ```text
   Decrypt PFD >
   ```

3. Choose:

   ```text
   Decrypt All
   ```

4. Confirm **Yes** when asked.
5. Leave Bruteforce open.

At this point the `BSAV0.SAV` inside your **Working** save folder is the file this money editor expects.

**Do not feed the money editor an encrypted `BSAV0.SAV`.**

---

# Part 5 — Patch the money

1. Double-click:

   ```text
   Blitz2MoneyTool.html
   ```

2. Your normal web browser opens the editor. Internet access is not required.
3. Click the file selector and choose the **decrypted**:

   ```text
   BSAV0.SAV
   ```

   from your **Working** save folder.
4. The editor analyzes the file before enabling the patch button.
5. Look at **Detected campaigns**.

For each occupied slot, the tool shows:

- Slot number
- Current cash
- Money spent
- Whether the duplicated save structures agree

If the number of detected campaigns is wrong, or it says **No recognized Blitz II campaign structures were found**, **STOP**. Do not try to force the patch.

6. Enter the amount of current cash you want.

The tested default is:

```text
$8,500,000
```

That amount has been tested with five campaign slots, including heavily customized teams, and is enough to purchase all facility upgrades with a small buffer.

The observed save-format maximum is:

```text
$16,777,215
```

The editor refuses anything above that value because one of the game's current-cash fields is only 24 bits wide.

7. Click:

   ```text
   Patch all detected campaigns
   ```

8. Your browser downloads a new file named exactly:

   ```text
   BSAV0.SAV
   ```

9. Replace the **decrypted `BSAV0.SAV` in the Working folder** with the newly downloaded file.
10. Do not replace anything in your `Original` backup.

The editor intentionally creates a new download instead of modifying your selected file in place.

---

# Part 6 — Re-encrypt and rebuild the PS3 save

Go back to Bruteforce with the Blitz save selected.

Follow these operations in order:

1. Click:

   ```text
   Update PFD >
   ```

2. Select a **Full update**.
3. Click **Yes** when asked to encrypt the files.
4. If this menu option is available/not greyed out, click:

   ```text
   Encrypt PFD > Encrypt decrypted files
   ```

5. Click:

   ```text
   Verify PFD >
   ```

   Make sure Bruteforce does not report an error.

6. Click:

   ```text
   Rebuild > Rebuild Full
   ```

7. Confirm the resulting prompt.

Do not skip the rebuild step just because everything already looks correct. The referenced Bruteforce guide treats the full rebuild as part of the finished-save process.

---

# Part 7 — Put the save back on the USB

Your finished save folder needs to be under:

```text
USB:\PS3\SAVEDATA\
```

For the verified North American release, that means the folder containing `PARAM.SFO`, `PARAM.PFD`, `BSAV0.SAV`, etc. belongs under the BLUS30203 save directory.

Copy the **whole finished save folder**, not only `BSAV0.SAV`.

Safely eject the USB from Windows.

---

# Part 8 — Copy the modified save back to the stock PS3

1. Plug the USB into the PS3.
2. Go to:

   ```text
   Game
   > Saved Data Utility (PS3)
   > USB Device
   ```

3. Highlight **Blitz: The League II**.
4. Press **Triangle**.
5. Choose **Copy**.
6. If the PS3 warns that a save already exists, make sure you really have your untouched backup, then confirm the overwrite.
7. Launch Blitz: The League II.

---

# Part 9 — Prove the save actually works

Do not stop at the campaign-select screen.

For each patched campaign:

1. Load the campaign.
2. Confirm the cash is correct **inside** the campaign.
3. Buy at least one item/upgrade.
4. Save the campaign normally.
5. Exit/reload the game or campaign.
6. Confirm the money and purchase still exist.

This verifies that the edited save is not merely displaying a changed summary value.

---

# Troubleshooting

## The editor says it found zero campaigns

Most likely:

- `BSAV0.SAV` is still encrypted.
- You selected the wrong file.
- You selected a file from the wrong copy/folder.
- Your save is from an untested region or has a structure this version does not know.
- The save is damaged.

Go back to the untouched backup and start again. Do not manually force offsets.

## The editor shows a structure mismatch

The file contains cash copies that disagree. This can happen with an old or partially edited save. The patcher will attempt to make the current-cash copies agree, but if you did not expect the mismatch, make another backup before continuing.

## Bruteforce will not decrypt the save

Check the setup section above. In particular:

- Make sure you are using the prepared 4.7.5 folder from the referenced guide.
- Do not install the broken Cheats Repository update when prompted.
- Only install the VB5 runtime if Windows says the DLL is missing.
- Confirm Bruteforce is pointed at the parent folder containing the `PS3` directory.

## PS3 says the save is corrupted

The money editor repairs **Blitz's internal checksum**, but Sony's PS3 save layer still has to be encrypted/rebuilt correctly.

Start again from the backup and repeat:

```text
Decrypt All
> patch BSAV0.SAV
> Update PFD / full update
> encrypt files
> Verify PFD
> Rebuild Full
```

Also make sure you copied the **entire finished save folder**, not just the edited game file.

## The campaign select screen has the money, but loading the campaign does not

Do not use a generic hex edit that changes only the obvious summary cash fields. This editor updates all four known current-cash representations specifically to prevent that problem.

If this editor itself produces that behavior on a new save, keep the broken save and report it along with the game's region/title ID. It may represent a previously unknown save structure.

## I want more than $16,777,215

This version intentionally refuses it. One current-cash representation is only three bytes (24 bits), so `$16,777,215` (`0xFFFFFF`) is the largest value that representation can hold.

The game may behave unpredictably if normal play later pushes cash-on-hand above that value. Keep backups.

---

# Privacy

`Blitz2MoneyTool.html` is offline/local.

It does not:

- upload your save
- send your PSN/account information anywhere
- use analytics
- use telemetry
- use cookies or browser storage
- call an API
- load a remote JavaScript library

Your selected file is read into browser memory and the patched result is generated as a local download.

The help hyperlink to The Project Lounge only opens if you click it. Visiting any external website is separate from the save editor itself.

See `PRIVACY.md` for more detail.

---

# Technical summary

For every detected campaign, the editor repairs four representations of current cash:

1. Plain 32-bit big-endian cash in the campaign summary.
2. Plain 32-bit big-endian cash in the global campaign cash array.
3. XOR-`0x3A` obfuscated positive 24-bit cash inside the serialized campaign.
4. XOR-`0x3A` obfuscated signed negative 32-bit cash inside the serialized campaign.

The deep campaign structure is located using signatures rather than one fixed absolute offset because player/team customization can shift serialized data.

The game's internal checksum is a big-endian CRC using polynomial `0x04C11DB7`, initial value `0`, calculated over `0x254` through end-of-file, and stored at `0x250`.

See `TECHNICAL_NOTES.md` for additional details.

---

# Files in this release

```text
Blitz2MoneyTool.html       Recommended GUI/offline editor
START_HERE.txt             Short beginner checklist
README.md                  Full step-by-step guide
PRIVACY.md                 What the tool does/doesn't collect
TECHNICAL_NOTES.md         Reverse-engineered save-format notes
blitz2_money_tool.py       Command-line/reference implementation
SHA256SUMS.txt             File hashes for this release
```

No PS3 save files, `PARAM.SFO`, `PARAM.PFD`, account IDs, console IDs, PSN names, or test-user data are included in the release.

---

# Credits / references

The Windows/Bruteforce portion of this README was written specifically for this Blitz workflow using this public guide as the setup reference:

**The Project Lounge — “How to Share and Mod PlayStation 3 Game Saves”**  
https://theprojectlounge.co.uk/how-to-share-and-mod-playstation-3-game-saves/

The Blitz-specific money structures and validation were reverse-engineered through controlled save comparisons and successful save/load/purchase testing on the PS3.

Blitz: The League II and PlayStation are trademarks/properties of their respective owners. This is an unofficial fan-made utility and is not affiliated with or endorsed by the game publisher/developer or Sony.

---

# License

MIT License.

Copyright (c) 2026 hickoryit41

See [`LICENSE`](LICENSE) for the full license text.
