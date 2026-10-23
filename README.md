**English** · [Русский](README.ru.md)

# Dota 2 → Deadlock

[![GameBanana](assets/badge-gamebanana.svg)](https://gamebanana.com/mods/729017)
[![Deadlock Mod Manager](assets/badge-mod-manager.svg)](https://gamebanana.com/mods/729017#Files)

Dota item icons and effects for Deadlock. Icons are picked by what an item does: lifesteal, armor reduction, barriers and so on. Some use two or more Dota images; upgraded versions have gold or red variants.

The effects included so far are Counterspell, Refresher, Shiva’s Guard for Cold Front, Arctic Blast/Frostbite and Pavise barriers. Barrier appearance, hit and break effects also apply to barriers from hero abilities. More Dota effects are planned.

V25 has 154 mapped item definitions and leaves 19 with their native icon. The [full table](docs/ITEMS.md) includes upgrades and mode-specific entries. Hero skins and voices are separate mods.

## Download

[V25 archive](https://github.com/hqvdvn-cmd/dota2todeadlock/releases/tag/v25) · [Full repository ZIP](https://github.com/hqvdvn-cmd/dota2todeadlock/archive/refs/heads/main.zip) · [GameBanana](https://gamebanana.com/mods/729017#Files)

Download V25 from GitHub. GameBanana mirrors the manager archive.

The GameBanana file has one-click install buttons for **Deadlock Mod Manager**, **Grimoire Mod Manager** and **HELLCAT**. Disable the previous version, install the new archive and enable all five components.

## Manual installation

1. Close Deadlock and your mod manager. Back up `game/citadel/gameinfo.gi` and any older files from this mod.
2. In Steam, open Deadlock → Properties → Installed Files → Browse, then open `game/citadel`.
3. Copy the five VPK files into `game/citadel/addons`. In the full repository ZIP they are in `packages`; in the V19 release archive they are at the archive root. Do not overwrite another mod’s files.
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

V25 refits 52 composite icons so secondary components remain visible in circular HUD slots. Component images and upgrade colors follow the current item table. These sheets are rendered previews; the gameplay screenshots and video below are from V19.

![V25 composite icons 1](assets/demo/v25/icons-1.png)


![V25 composite icons 2](assets/demo/v25/icons-2.png)


![V25 composite icons 3](assets/demo/v25/icons-3.png)


[Watch the full one-minute showcase](https://github.com/hqvdvn-cmd/dota2todeadlock/releases/download/v19/dota2-to-deadlock-v19-showcase.mp4)

The screenshots and video below were supplied for V19. The character skin is installed separately and is not included.

![Item icons — 800 souls](assets/demo/v19/items-800.png)

![Item icons — 1600 souls; Mystic Slow uses Lich Frost Blast](assets/demo/v19/items-1600.png)

![Item icons — 3200 souls](assets/demo/v19/items-3200.png)

![Item icons — 6400 souls](assets/demo/v19/items-6400.png)

![Grit — cyan Pavise barrier](assets/demo/v19/grit.png)

![Guardian Ward — gold Pavise barriers](assets/demo/v19/guardian-ward.png)

![Divine Barrier — red Pavise barriers](assets/demo/v19/divine-barrier.png)

![Cold Front — Shiva wave](assets/demo/v19/cold-front.png)

![Arctic Blast — red Shiva wave and Frostbite](assets/demo/v19/arctic-blast.png)

![Counterspell — Anti-Mage shell](assets/demo/v19/counterspell.png)

![Refresher — green spiral](assets/demo/v19/refresher.png)

## Compatibility

The ability bindings were rebased on the October 23 game resources. New game updates can break replacements or reset addon loading. The Python installer checks the native ability file; managers and manual copying do not run this check. The V19 screenshots show all four shop price tiers, including the new Mystic Slow. The supplied footage shows the named effects in the combined local setup; other triggers and standalone matches remain outside this check.

When using [Shura](https://github.com/hqvdvn-cmd/sekiro-shura-deadlock), use its D2D compatibility patch for the ultimate binding. Do not combine whole ability-resource replacements without a matching patch.

For a bug report, include the affected item/effect, game build and other installed mods. A screenshot or short clip helps.

Original assets: Valve. [Credits](CREDITS.md).
