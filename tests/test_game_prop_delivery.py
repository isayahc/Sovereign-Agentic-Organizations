"""Regression checks for the downloadable OpenForma/Godot acceptance package."""

import hashlib
import json
import unittest
import zipfile
from pathlib import Path


class DeliveryTest(unittest.TestCase):
    """Ensure the published sample stays tied to its reviewed inputs and engine checks."""

    def test_revisions(self) -> None:
        """Validate packaged sources, delivery hashes, engine reports and revision changes."""
        sample = Path(__file__).resolve().parents[1] / "examples/relay-prop"
        with zipfile.ZipFile(sample / "delivery.zip") as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertEqual(bundle.read("recipe.json"), (sample / "recipe.json").read_bytes())
            manifest = json.loads(bundle.read("manifest.json"))
            ref, = manifest["references"]
            self.assertEqual(ref["sha256"], hashlib.sha256((sample / "client-note.md").read_bytes()).hexdigest())
            first, second = manifest["versions"]
            for label, version, height in (("v1", first, .029), ("v2", second, .046)):
                for name, digest in version["files"].items():
                    self.assertEqual(hashlib.sha256(bundle.read(f"{label}/{name}")).hexdigest(), digest)
                engine = json.loads(bundle.read(f"{label}/godot.json"))
                self.assertEqual(engine, version["godot"])
                self.assertAlmostEqual(engine["size_m"][1], height, places=5)
                self.assertLessEqual(engine["triangles"], manifest["triangle_budget"])
                self.assertEqual(engine["material"], "BrushedBrass")
                self.assertTrue(bundle.read(f"{label}/prop.step").startswith(b"ISO-10303-21"))
                self.assertTrue(bundle.read(f"{label}/prop.glb").startswith(b"glTF"))
            for output in ("preview.png", "prop.step", "prop.glb"):
                self.assertNotEqual(first["files"][output], second["files"][output])
