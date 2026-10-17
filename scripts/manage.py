"""Install or remove this exact mod distribution. Standard library, Windows only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().lower()


def require_closed():
    if os.name != "nt":
        raise RuntimeError("This installer supports Windows only.")
    command = (
        "$ErrorActionPreference='Stop'; "
        "$p=@(Get-Process | Where-Object { $_.ProcessName -match "
        "'deadlock|citadel|modmanager|deadlockmod|deadlock-mod' }); "
        "if ($p.Count) { $p | Select-Object Id,ProcessName | ConvertTo-Json; exit 9 }"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        raise RuntimeError("Close Deadlock and its mod manager first. " + result.stdout.strip())


def copy_exclusive(source, dest, digest):
    """Stage on the destination volume, then publish without replacing a file."""
    fd, temporary = tempfile.mkstemp(prefix=".dota-mod-", dir=dest.parent)
    os.close(fd)
    temporary = Path(temporary)
    try:
        shutil.copyfile(source, temporary)
        if sha(temporary) != digest:
            raise RuntimeError("Staged file checksum mismatch")
        os.link(temporary, dest)  # Atomic; fails if a destination already exists.
    finally:
        temporary.unlink(missing_ok=True)


def run(game_dir, *, apply=False, uninstall=False, enable_addons=False,
        repo=ROOT, backup_dir=None):
    require_closed()
    game = Path(game_dir).resolve(strict=True)
    repo = Path(repo).resolve(strict=True)
    config = game / "gameinfo.gi"
    if not config.is_file() or not (game / "pak01_dir.vpk").is_file():
        raise RuntimeError("Expected Deadlock/game/citadel with gameinfo.gi and pak01_dir.vpk")
    if config.is_symlink() or config.resolve().parent != game:
        raise RuntimeError("Unexpected configuration path")
    addons = game / "addons"
    if addons.is_symlink() or addons.resolve().parent != game:
        raise RuntimeError("Unexpected addons path")
    if addons.exists() and not addons.is_dir():
        raise RuntimeError("addons is not a directory")
    manifest = json.loads((repo / "manifest.json").read_text(encoding="utf-8"))
    packages = manifest["packages"]
    names = [p["file"] for p in packages]
    expected = {f"pak{i:02}_dir.vpk" for i in range(6, 11)}
    if set(names) != expected or len(names) != len(expected):
        raise RuntimeError("Manifest must contain exactly pak06 through pak10")
    planned = []
    for item in packages:
        name, digest = item["file"], item["sha256"].lower()
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise RuntimeError("Invalid package digest")
        source, dest = repo / "packages" / name, addons / name
        if source.is_symlink() or source.resolve().parent != (repo / "packages").resolve():
            raise RuntimeError("Unexpected package path")
        if sha(source) != digest:
            raise RuntimeError("Distribution checksum mismatch: " + name)
        if dest.is_symlink() or dest.resolve().parent != addons.resolve():
            raise RuntimeError("Unexpected destination path: " + name)
        if dest.exists() and sha(dest) != digest:
            raise RuntimeError("Occupied or modified addon; refusing to change: " + name)
        if (uninstall and dest.exists()) or (not uninstall and not dest.exists()):
            planned.append((source, dest, digest))

    original_config = config.read_bytes()
    # Decode as ASCII-compatible bytes so BOM, CRLF and unrelated settings survive.
    # Mask comments without changing offsets into the original file.
    masked = re.sub(rb'"[^"\r\n]*"|//[^\r\n]*|/\*.*?\*/',
                    lambda m: m[0] if m[0].startswith(b'"') else b' ' * len(m[0]),
                    original_config, flags=re.S)
    matches = list(re.finditer(rb'\bSearchPaths\s*\{', masked))
    enabled = False
    if len(matches) == 1:
        start = matches[0].end()
        depth, end = 1, None
        for token in re.finditer(rb'"[^"\r\n]*"|[{}]', masked[start:]):
            depth += 1 if token[0] == b'{' else -1 if token[0] == b'}' else 0
            if depth == 0:
                end = start + token.start()
                break
        if end is not None:
            enabled = re.search(rb'\bGame"?\s+"?citadel[/\\]addons"?(?=\s|\})', masked[start:end], re.I)
            base = re.search(rb'\bGame"?\s+"?citadel"?(?=\s|\})', masked[start:end], re.I)
            if not uninstall and enabled and base and enabled.start() > base.start():
                raise RuntimeError("Addons follows the base game path. Move its Game line above Game citadel; see README.")
    new_config = original_config
    if not uninstall and not enabled:
        if not enable_addons:
            raise RuntimeError("Addons search path missing. Review README, then add --enable-addons.")
        if len(matches) != 1 or end is None:
            raise RuntimeError("Ambiguous SearchPaths; configure it manually using README.")
        end = matches[0].end()
        newline = b"\r\n" if b"\r\n" in original_config else b"\n"
        new_config = original_config[:end] + newline + b"            Game citadel/addons" + newline + original_config[end:]

    backup_base = (Path(backup_dir) if backup_dir else repo / ".local" / "backups").resolve()
    if backup_base.is_relative_to(game.parent.parent):
        raise RuntimeError("Backups must be outside the Deadlock directory")
    protected_paths = list(addons.glob("*.vpk")) if addons.exists() else []
    protected_paths += [addons / ".dmm.json"] if (addons / ".dmm.json").exists() else []
    changed_dest = {dest for _, dest, _ in planned}
    protected = {str(p): sha(p) for p in protected_paths if p not in changed_dest}
    result = {"mode": "apply" if apply else "dry-run", "action": "uninstall" if uninstall else "install",
              "game_dir": str(game), "changed": [d.name for _, d, _ in planned],
              "enable_addons": new_config != original_config, "backup": None,
              "runtime": "not tested; restart game to observe changes"}
    if not apply or (not planned and new_config == original_config):
        return result

    backup_base.mkdir(parents=True, exist_ok=True)
    backup = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + result["action"] + "-", dir=backup_base))
    result["backup"] = str(backup)
    (backup / "gameinfo.gi").write_bytes(original_config)
    if uninstall:
        for _, dest, digest in planned:
            shutil.copy2(dest, backup / dest.name)
            if sha(backup / dest.name) != digest:
                raise RuntimeError("Backup checksum mismatch")
    completed = []
    config_changed = False
    try:
        require_closed()
        if config.read_bytes() != original_config or any(sha(Path(p)) != h for p, h in protected.items()):
            raise RuntimeError("Another process changed game files during preflight")
        addons.mkdir(exist_ok=True)
        for source, dest, digest in planned:
            if uninstall:
                if sha(dest) != digest:
                    raise RuntimeError("Package changed during uninstall")
                dest.unlink()
            else:
                copy_exclusive(source, dest, digest)
            completed.append((source, dest, digest))
        if new_config != original_config:
            config_changed = True
            config.write_bytes(new_config)
        for _, dest, digest in planned:
            if (uninstall and dest.exists()) or (not uninstall and sha(dest) != digest):
                raise RuntimeError("Final package verification failed")
        if any(sha(Path(p)) != h for p, h in protected.items()):
            raise RuntimeError("An unrelated mod/config changed during operation")
        if config.read_bytes() != new_config:
            raise RuntimeError("Configuration verification failed")
    except BaseException:
        for _, dest, digest in reversed(completed):
            if uninstall and not dest.exists():
                copy_exclusive(backup / dest.name, dest, digest)
            elif not uninstall and dest.exists() and sha(dest) == digest:
                dest.unlink()
        if config_changed and config.read_bytes() == new_config:
            config.write_bytes(original_config)
        raise
    result["protected_sha256"] = protected
    (backup / "receipt.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "uninstall"])
    parser.add_argument("--game-dir", type=Path, required=True, help="Path ending in Deadlock/game/citadel")
    parser.add_argument("--apply", action="store_true", help="Write changes; default is preview only")
    parser.add_argument("--enable-addons", action="store_true", help="Insert missing Game citadel/addons search path with backup")
    parser.add_argument("--backup-dir", type=Path, help="Backup location outside the game directory")
    args = parser.parse_args()
    try:
        result = run(args.game_dir, apply=args.apply, uninstall=args.action == "uninstall",
                     enable_addons=args.enable_addons, backup_dir=args.backup_dir)
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        parser.exit(1, "Refused: " + str(exc) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
