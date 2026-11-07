"""Compile two reviewed prop designs through local OpenForma MCP and package Godot assets."""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import trimesh
from PIL import Image, ImageDraw
from trimesh.visual.material import PBRMaterial

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".local/OpenForma/.agents/skills/forma-hardware/scripts"


def write_json(path: Path, value: object) -> None:
    """Write a portable UTF-8 JSON record."""
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    """Hash an artifact for the delivery manifest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preview(mesh: trimesh.Trimesh, color: np.ndarray, path: Path, frame: float) -> None:
    """Render a shared orthographic three-quarter view with flat directional lighting."""
    view = np.array([1.3, 1.0, 1.65])
    view /= np.linalg.norm(view)
    right = np.cross([0, 1, 0], view)
    right /= np.linalg.norm(right)
    up = np.cross(view, right)
    points = np.column_stack((mesh.vertices @ right, -mesh.vertices @ up))
    points = points * (900 / frame) + [600, 480]
    image = Image.new("RGB", (1200, 820), "#202831")
    draw = ImageDraw.Draw(image)
    depths = mesh.triangles_center @ view
    light = np.array([-0.3, 0.88, 0.36])
    for face in np.argsort(depths):
        normal = mesh.face_normals[face]
        if normal @ view <= 0:
            continue
        shade = 0.48 + 0.52 * max(0, normal @ light)
        rgb = tuple((color * shade).astype(int))
        draw.polygon([tuple(point) for point in points[mesh.faces[face]]], fill=rgb)
    image.resize((600, 410), Image.Resampling.LANCZOS).save(path)


def build_revision(spec: dict, folder: Path, project: str, frame: float, budget: int,
                   author: str, godot: str) -> dict:
    """Compile reviewed IR, verify STEP integrity, and load its converted mesh into Godot."""
    folder.mkdir()
    ir = dict(spec["project_ir"])
    ir["assembly_metadata"] = {**ir.get("assembly_metadata", {}), "project_id": project}
    source = folder / "design.json"
    write_json(source, ir)
    cmd = [sys.executable, str(SKILL / "forma.py"), "compile", str(source), "--authoring-agent", author]
    result = json.loads(subprocess.check_output(cmd, text=True))
    if result.get("project_id") != project or result.get("is_valid") is not True:
        raise ValueError("MCP compile did not return the requested valid project")
    cad = result["project_ir"]["cad_model"]
    step = folder / "prop.step"
    shutil.copyfile(cad["path"], step)
    if not cad.get("generated") or digest(step) != cad["stored_sha256"]:
        raise ValueError("Native STEP failed provenance check")
    shutil.copyfile(cad["model_source_path"], folder / "model.py")
    geom, = cad["meshes"]
    mesh = trimesh.Trimesh(vertices=np.reshape(geom["vertices"], (-1, 3)),
                           faces=np.reshape(geom["faces"], (-1, 3)), process=False)
    # Right-handed mm/Z-up to glTF meters/Y-up. Place the pivot at floor center.
    mesh.vertices = mesh.vertices[:, [0, 2, 1]] * np.array([.001, .001, -.001])
    center = mesh.bounds.mean(axis=0)
    center[1] = mesh.bounds[0, 1]
    mesh.apply_translation(-center)
    mat = spec["material"]
    color = np.array(list(bytes.fromhex(mat["srgb"])))
    srgb = color / 255
    linear = np.where(srgb <= .04045, srgb / 12.92, ((srgb + .055) / 1.055) ** 2.4)
    material = PBRMaterial(name=mat["name"], baseColorFactor=[*np.rint(linear * 255).astype(int), 255],
                           metallicFactor=mat["metallic"], roughnessFactor=mat["roughness"])
    mesh.visual = trimesh.visual.TextureVisuals(material=material)
    glb = folder / "prop.glb"
    mesh.export(glb)
    preview(mesh, color, folder / "preview.png", frame)
    check = folder / "godot.json"
    subprocess.run([godot, "--headless", "--script", str(ROOT / "scripts/godot/check_prop.gd"),
                    "--", str(glb), str(check)], check=True, timeout=90)
    measured = json.loads(check.read_text())
    expected = np.array(spec["expected_xyz_mm"])[[0, 2, 1]] * .001
    if not np.allclose(measured["size_m"], expected, atol=0.00005, rtol=0) or abs(measured["floor_m"]) > .00005:
        raise ValueError(f"Unexpected imported bounds: {measured}")
    if not 0 < measured["triangles"] <= budget or measured["triangles"] != len(mesh.faces):
        raise ValueError("Godot triangle count differs from CAD or exceeds budget")
    imported_color = np.array(list(bytes.fromhex(measured["albedo"])))
    if (measured["material"] != mat["name"] or not np.allclose(imported_color, color, atol=2)
            or abs(measured["metallic"] - mat["metallic"]) > .01
            or abs(measured["roughness"] - mat["roughness"]) > .01):
        raise ValueError(f"Godot material differs from request: {measured}")
    return dict(request=spec["request"], expected_xyz_mm=spec["expected_xyz_mm"], godot=measured,
                files={p.name: digest(p) for p in sorted(folder.iterdir())})


def main() -> None:
    """Build in a fresh Forma workspace and exclusively publish a complete two-version ZIP."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path, help="Request manifest from client_references.py design")
    parser.add_argument("recipe", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--godot", default="godot")
    parser.add_argument("--author", choices=["opencode", "codex", "other"], required=True)
    args = parser.parse_args()
    handoff = json.loads(args.handoff.read_text(encoding="utf-8"))
    recipe = json.loads(args.recipe.read_text(encoding="utf-8"))
    if args.output.exists():
        parser.error("Output already exists")
    refs = []
    for ref in handoff["references"]:
        if not ref["allowed"] or ref["client"] != handoff["client"]:
            parser.error("Handoff includes an ineligible reference")
        original = Path(ref["original"])
        if not original.is_absolute():
            original = args.handoff.parent / original
        if digest(original) != ref["sha256"]:
            parser.error("Reference checksum mismatch")
        refs.append({k: ref[k] for k in ("source_id", "revision", "sha256", "terms")})
    pinned = [{k: ref[k] for k in ("source_id", "revision", "sha256")} for ref in refs]
    if (not refs or recipe["references"] != pinned or recipe["client"] != handoff["client"]
            or recipe["brief"] != handoff["brief"]):
        parser.error("Reviewed recipe must match client, brief and selected references")
    first, second = recipe["versions"]
    frame = max(np.linalg.norm(v["expected_xyz_mm"]) for v in (first, second)) / 1000
    job = Path(subprocess.check_output([sys.executable, str(SKILL / "create_project.py")], text=True).strip())
    bundle = job / "delivery"
    bundle.mkdir()
    revisions = [build_revision(s, bundle / label, job.name, frame, recipe["triangle_budget"],
                                args.author, args.godot) for label, s in (("v1", first), ("v2", second))]
    for name in ("prop.glb", "preview.png"):
        if revisions[0]["files"][name] == revisions[1]["files"][name]:
            raise ValueError(f"Revision did not change {name}")
    write_json(bundle / "manifest.json", dict(project_id=job.name, client=recipe["client"], brief=recipe["brief"],
               references=refs, preferences=recipe["preferences"], assumptions=recipe["assumptions"],
               triangle_budget=recipe["triangle_budget"], versions=revisions))
    shutil.copyfile(args.recipe, bundle / "recipe.json")
    (bundle / "IMPORT.txt").write_text("Copy v1/prop.glb or v2/prop.glb into a Godot 4 project. Drag the imported scene into a level. Units are meters, +Y is up, and the pivot is at floor center.\n", encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as tmp:
        archive = Path(tmp) / "bundle.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
            for file in sorted(bundle.rglob("*")):
                if file.is_file():
                    output.write(file, file.relative_to(bundle))
        os.link(archive, args.output)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
