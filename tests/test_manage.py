import importlib.util
import json
import hashlib
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "manage.py"
spec = importlib.util.spec_from_file_location("manage", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        (self.repo / "packages").mkdir(parents=True)
        self.game = self.root / "Deadlock" / "game" / "citadel"
        self.addons = self.game / "addons"
        self.addons.mkdir(parents=True)
        (self.game / "pak01_dir.vpk").write_bytes(b"base-game")
        self.config = b'"GameInfo" { FileSystem { SearchPaths { Game citadel/addons Game citadel } } }'
        (self.game / "gameinfo.gi").write_bytes(self.config)
        (self.addons / "pak01_dir.vpk").write_bytes(b"other-mod")
        (self.addons / ".dmm.json").write_bytes(b"other-config")
        packages = []
        for i in range(6, 11):
            name = f"pak{i:02}_dir.vpk"
            payload = f"payload-{i}".encode()
            (self.repo / "packages" / name).write_bytes(payload)
            packages.append({"file": name, "sha256": hashlib.sha256(payload).hexdigest(), "component": str(i)})
        (self.repo / "manifest.json").write_text(json.dumps({"packages": packages}))
        self.closed = patch.object(m, "require_closed")
        self.closed.start()
        self.addCleanup(self.closed.stop)

    def run_mod(self, **kwargs):
        return m.run(self.game, repo=self.repo, **kwargs)

    def test_dry_run_writes_nothing(self):
        before = sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*"))
        result = self.run_mod()
        self.assertEqual(result["mode"], "dry-run")
        self.assertEqual(before, sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")))

    def test_install_uninstall_preserves_other_mods_and_backups(self):
        installed = self.run_mod(apply=True)
        self.assertEqual(len(installed["changed"]), 5)
        removed = self.run_mod(apply=True, uninstall=True)
        self.assertEqual(len(removed["changed"]), 5)
        for i in range(6, 11):
            name = f"pak{i:02}_dir.vpk"
            self.assertFalse((self.addons / name).exists())
            self.assertEqual((Path(removed["backup"]) / name).read_bytes(), (self.repo / "packages" / name).read_bytes())
        self.assertEqual((self.addons / "pak01_dir.vpk").read_bytes(), b"other-mod")
        self.assertEqual((self.addons / ".dmm.json").read_bytes(), b"other-config")
        self.assertEqual((self.game / "gameinfo.gi").read_bytes(), self.config)

    def test_conflicting_slot_aborts_entire_install(self):
        (self.addons / "pak09_dir.vpk").write_bytes(b"unrelated")
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)
        self.assertFalse((self.addons / "pak06_dir.vpk").exists())
        self.assertEqual((self.addons / "pak09_dir.vpk").read_bytes(), b"unrelated")

    def test_uninstall_refuses_modified_file(self):
        self.run_mod(apply=True)
        (self.addons / "pak09_dir.vpk").write_bytes(b"modified")
        with self.assertRaises(RuntimeError): self.run_mod(apply=True, uninstall=True)
        self.assertTrue((self.addons / "pak06_dir.vpk").exists())

    def test_already_installed_is_noop(self):
        self.run_mod(apply=True)
        result = self.run_mod(apply=True)
        self.assertEqual(result["changed"], [])

    def test_corrupt_distribution_refused(self):
        (self.repo / "packages" / "pak10_dir.vpk").write_bytes(b"tamper")
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)
        self.assertFalse((self.addons / "pak06_dir.vpk").exists())

    def test_search_path_requires_explicit_flag_and_preserves_original(self):
        original = b'"GameInfo" { FileSystem { SearchPaths { Game citadel } } }'
        (self.game / "gameinfo.gi").write_bytes(original)
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)
        result = self.run_mod(apply=True, enable_addons=True)
        self.assertIn(b"citadel/addons", (self.game / "gameinfo.gi").read_bytes())
        self.assertEqual((Path(result["backup"]) / "gameinfo.gi").read_bytes(), original)
        self.run_mod(apply=True, uninstall=True)
        self.assertIn(b"citadel/addons", (self.game / "gameinfo.gi").read_bytes())

    def test_commented_addons_entry_does_not_enable_loading(self):
        original = b'GameInfo { FileSystem { SearchPaths { // Game citadel/addons\n Game citadel } } }'
        (self.game / "gameinfo.gi").write_bytes(original)
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)

    def test_addons_after_base_is_refused(self):
        original = b'GameInfo { FileSystem { SearchPaths { Game citadel Game citadel/addons } } }'
        (self.game / "gameinfo.gi").write_bytes(original)
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)

    def test_backup_inside_game_refused(self):
        with self.assertRaises(RuntimeError): self.run_mod(apply=True, backup_dir=self.game / "backup")

    def test_process_gate_precedes_mutation(self):
        with patch.object(m, "require_closed", side_effect=RuntimeError("busy")):
            with self.assertRaises(RuntimeError): self.run_mod(apply=True)
        self.assertFalse((self.addons / "pak06_dir.vpk").exists())

    def test_install_failure_rolls_back_new_packages(self):
        original = m.copy_exclusive
        count = 0
        def fail(source, dest, digest):
            nonlocal count
            count += 1
            if count == 3: raise OSError("simulated write failure")
            return original(source, dest, digest)
        with patch.object(m, "copy_exclusive", side_effect=fail):
            with self.assertRaises(OSError): self.run_mod(apply=True)
        self.assertFalse((self.addons / "pak06_dir.vpk").exists())
        self.assertFalse((self.addons / "pak07_dir.vpk").exists())
        self.assertEqual((self.game / "gameinfo.gi").read_bytes(), self.config)

    def test_manifest_path_traversal_refused(self):
        data = json.loads((self.repo / "manifest.json").read_text())
        data["packages"][0]["file"] = "../escape.vpk"
        (self.repo / "manifest.json").write_text(json.dumps(data))
        with self.assertRaises(RuntimeError): self.run_mod(apply=True)

if __name__ == "__main__": unittest.main()
