**English** · [Русский](README.ru.md)

# Dota 2 → Deadlock

[![GameBanana](assets/badge-gamebanana.svg)](https://gamebanana.com/mods/729017)
[![Deadlock Mod Manager](assets/badge-mod-manager.svg)](https://gamebanana.com/mods/729017#Files)

Dota item icons and effects for Deadlock. Icons are picked by what an item does: lifesteal, armor reduction, barriers and so on. Some use two or more Dota images; upgraded versions have gold or red variants.

The effects included so far are Counterspell, Refresher, Shiva’s Guard for Cold Front, Arctic Blast/Frostbite and Pavise barriers. Barrier appearance, hit and break effects also apply to barriers from hero abilities. More Dota effects are planned.

V18 has 154 mapped item definitions and leaves 19 with their native icon. The [full table](docs/ITEMS.md) includes upgrades and mode-specific entries. Hero skins and voices are separate mods.

## Download

[V18 archive](https://github.com/hqvdvn-cmd/dota2todeadlock/releases/tag/v18) · [Full repository ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) · [GameBanana](https://gamebanana.com/mods/729017#Files)

V18 is available on GitHub. The GameBanana file update is still pending.

The GameBanana file has one-click install buttons for **Deadlock Mod Manager**, **Grimoire Mod Manager** and **HELLCAT**. Disable the previous version, install the new archive and enable all five components.

## Manual installation

1. Close Deadlock and your mod manager. Back up `game/citadel/gameinfo.gi` and any older files from this mod.
2. In Steam, open Deadlock → Properties → Installed Files → Browse, then open `game/citadel`.
3. Copy the five VPK files into `game/citadel/addons`. In the full repository ZIP they are in `packages`; in the V18 release archive they are at the archive root. Do not overwrite another mod’s files.
4. In `gameinfo.gi`, find `FileSystem` → `SearchPaths`. Place `Game citadel/addons` above `Game citadel`. Keep the existing game/language paths and make sure these entries are present:

```text
Game  citadel/addons
Mod   citadel
Write citadel
Mod   core
Write core
```

To update, remove only the previous copy of this pack before copying the new files. To uninstall, remove this pack’s five VPKs after checking [SHA256SUMS.txt](SHA256SUMS.txt). Keep other files in `addons`.

### Optional Python installer

The GitHub ZIP also has an installer that checks the current native ability resource and backs up configuration changes. Python 3.10+ is required. Replace the game path with yours:

```powershell
python scripts/manage.py install --game-dir "D:/SteamLibrary/steamapps/common/Deadlock/game/citadel" --enable-addons --apply
python scripts/manage.py launch --game-dir "D:/SteamLibrary/steamapps/common/Deadlock/game/citadel" --apply
```

For removal, use `uninstall` instead of `install` and omit `--enable-addons`, from the same extracted folder. Keep `.local/backups`.

## Preview

![V18 item icons](assets/demo/icons-v18.png)

The video and game screenshots below show an earlier version. The character skin in them is not included.

[Watch the 27-second showcase](assets/demo/showcase.mp4)

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

## Compatibility

Based on the October 21 game resources. New game updates can break replacements or reset addon loading. The Python installer checks the native ability file; managers and manual copying do not run this check. The newest icon revision has file/pixel checks, with in-game confirmation still pending.

When using [Shura](https://github.com/hqvdvn-cmd/sekiro-shura-deadlock), use its D2D compatibility patch for the ultimate binding. Do not combine whole ability-resource replacements without a matching patch.

For a bug report, include the affected item/effect, game build and other installed mods. A screenshot or short clip helps.

Original assets: Valve. [Credits](CREDITS.md).
