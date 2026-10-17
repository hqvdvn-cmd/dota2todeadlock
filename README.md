**English** · [Русский](README.ru.md)

# Dota 2 → Deadlock

Bring Dota 2 item icons and spell effects into Deadlock.

- **84 item icons**, including red and gold variants for upgraded items.
- Anti-Mage’s **Counterspell** shield and the green **Refresher** spiral.
- **Shiva’s Guard** for Cold Front, plus a red Arctic Blast wave and Frostbite.
- **Pavise** barriers in cyan, gold and red.

[Download ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) · [Item list (RU)](docs/ITEMS.md)

## Preview

[![Watch the mod showcase](assets/demo/poster.jpg)](assets/demo/showcase.mp4)

**[Watch the 27-second showcase](assets/demo/showcase.mp4)** · [Download video](https://github.com/hqvdvn-cmd/dota2todeadlock/raw/refs/heads/main/assets/demo/showcase.mp4)

The character skin shown in the footage is a separate mod and is not included.

<details>
<summary>Screenshots: items and effects</summary>

**Item icons — click an image to view it at full size.**

<a href="assets/demo/items-800-1600.png"><img src="assets/demo/items-800-1600.png" width="32%" alt="Item icons: 800 and 1,600 souls"></a>
<a href="assets/demo/items-3200.png"><img src="assets/demo/items-3200.png" width="32%" alt="Item icons: 3,200 souls"></a>
<a href="assets/demo/items-6400.png"><img src="assets/demo/items-6400.png" width="32%" alt="Item icons: 6,400 souls"></a>

**Pavise: cyan, gold and red variants.**

<a href="assets/demo/pavise-cyan.png"><img src="assets/demo/pavise-cyan.png" width="32%" alt="Cyan Pavise barrier"></a>
<a href="assets/demo/pavise-gold.png"><img src="assets/demo/pavise-gold.png" width="32%" alt="Gold Pavise barrier"></a>
<a href="assets/demo/pavise-red.png"><img src="assets/demo/pavise-red.png" width="32%" alt="Red Pavise barrier on the player and an ally"></a>

**Cold Front / Shiva.**

![Shiva wave in Deadlock](assets/demo/cold-front.png)

</details>

## Requirements

- Deadlock installed through Steam on Windows.
- [Python 3.10 or newer](https://www.python.org/downloads/windows/) for the installer.

## Install

1. [Download the ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) and extract it outside the game folder.
2. Close Deadlock and your mod manager, including its tray icon.
3. In Steam, open **Deadlock → Properties → Installed Files → Browse**. Open `game\citadel` inside that folder and copy its path.
4. Open PowerShell in the extracted mod folder and run the command below. **Replace the example game path with your own.**

```powershell
python scripts/manage.py install --game-dir "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" --enable-addons --apply
```

The installer enables addon loading if needed and backs up the configuration before changing it. Backups are saved in `.local\backups` inside the extracted mod folder. Keep that folder, then launch the game.

If the installer reports an occupied or modified addon, stop and check your other mods. Do not overwrite the conflicting file.

## Uninstall

Close the game and mod manager. From the same mod folder, run:

```powershell
python scripts/manage.py uninstall --game-dir "D:\SteamLibrary\steamapps\common\Deadlock\game\citadel" --apply
```

This removes this mod’s packages and leaves your other mods in place. Restart the game to return to the original item icons and effects.

<details>
<summary>Manual installation</summary>

Back up `game\citadel\gameinfo.gi`. Copy the five files from `packages` into `game\citadel\addons` without overwriting another mod. In `gameinfo.gi`, under `FileSystem → SearchPaths`, add `Game citadel/addons` above `Game citadel` if it is missing.

To uninstall manually, remove only this mod’s `pak06_dir.vpk` through `pak10_dir.vpk` after checking them against [SHA256SUMS.txt](SHA256SUMS.txt). Keep the rest of `addons`.

</details>

## Compatibility

Made for the **October 17, 2026** game build. Game updates may break the mod; if problems appear after an update, uninstall it until an updated version is available. A mod manager may also replace manually installed files when it syncs.

Unofficial fan mod using Dota 2 and Deadlock assets by Valve. [Credits](CREDITS.md).
