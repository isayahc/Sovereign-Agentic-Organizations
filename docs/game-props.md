# Produce a versioned Godot prop

The studio builds one static, single-material hard-surface mesh per revision. Both revisions pass through the local OpenForma MCP compiler under the same project ID. Godot instantiates each GLB and checks the material, triangle count, dimensions and floor pivot. Measurements use meters with +Y up; editable CAD uses millimeters with +Z up.

1. Complete [local physical design setup](physical-designs.md), start OpenForma, and put a Godot 4 executable on PATH. Install the game dependencies using the **same Python interpreter** as the Forma setup. On Windows run `.local/venv/Scripts/python.exe -m pip install -r requirements-game-props.txt`.
2. Run [client reference ingestion and retrieval](client-references.md). Keep the JSON handoff and its immutable originals available on the same machine.
3. In OpenCode run `/game-prop <handoff path> "<client revision request>" <destination.zip>`. The agent reads the brief and references, recalls client preferences through Cognee, and authors a recipe. For the bundled synthetic example, the reviewed recipe and handoff are already present.
4. To replay a reviewed recipe, run the following from the repository root in the Forma Python environment. Set `FORMA_MCP_URL` if the local service uses a different endpoint. Use `--godot <path>` for a custom Godot executable.

```sh
python scripts/build_game_prop.py examples/relay-prop/handoff.json examples/relay-prop/recipe.json .local/relay-delivery.zip --author codex
```

The output path must be new. Each revision contains editable IR and OpenCAD source, STEP, an embedded-material GLB, PNG preview and Godot measurements. The manifest records source IDs, hashes, revision numbers, terms, assumptions and file checksums. To use the result, copy one revision's GLB into a Godot project and drag the imported scene into the level. The package is visual geometry for a static prop; collision and interactive behavior are separate engine work.

## Reference run

[Download both example revisions](../examples/relay-prop/delivery.zip). The reproducible fixture uses a synthetic client brief and revision request. The sample was authored by Codex; its empty preference list records that no recalled client preferences were used. The handoff is a portable example of the #5 manifest and does not require a running embedding model to replay.

| Godot 4.6.3 import | v1 | v2 |
| --- | --- | --- |
| CAD width × depth × height | 92 × 64 × 29 mm | 92 × 64 × 46 mm |
| Cooling slots | 4 | 6 |
| Triangles (budget 5,000) | 3,132 | 3,164 |
| Material | BrushedBrass | BrushedBrass |
