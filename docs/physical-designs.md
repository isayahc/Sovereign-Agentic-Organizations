# Physical design with OpenCode

OpenCode authors the design; the local **Mapped-Assembly/OpenForma** backend supplies MCP compilation, validation, and persistence. Its bundled OpenCAD adapter creates native CAD exports.

## Windows setup

Prerequisites: Git, uv, Python 3.12 (installable through uv), and OpenCode V2 with a working model connection.

From this repository:

```powershell
./scripts/setup-design.ps1
./scripts/start-design.ps1
```

Keep the backend terminal open. In another terminal in this repository:

```powershell
opencode mcp list
opencode
```

The project config registers `openforma` at `http://127.0.0.1:8000/mcp` and discovers the upstream `forma-hardware` skill. OpenCode reloads configuration automatically; use `/reload` if the tools have not appeared in an existing session.

## Start designing

Example prompt:

> Use the forma-hardware skill to design a desktop enclosure, 100 x 60 x 30 mm, with a removable lid and four mounting holes. Ask me for missing fit requirements. Use the local OpenForma tools and export STEP and STL with the model source and feature tree.

OpenCode should use the project Python interpreter, `.local/venv/Scripts/python.exe`, for the skill scripts. Create each design workspace with the upstream `scripts/create_project.py` helper; it returns a fresh directory under `~/forma-workspace/` for the source and artifacts.

For host-authored electronics, use the discovered `forma.compile_project` MCP tool with `authoring_agent: opencode`, then persist its compiled result and returned artifacts. For CAD, follow the skill's `references/cad.md` and use `cad.py build` for actual native exports. Server-side LLM generation requires separate provider configuration; this setup uses OpenCode as the author.

## Verification and troubleshooting

```powershell
# Verify native OCCT and the supported OpenCAD feature set.
.local/venv/Scripts/python.exe .local/OpenForma/.agents/skills/forma-hardware/scripts/cad.py check

# Verify the running backend's MCP tool catalog independently of OpenCode.
.local/venv/Scripts/python.exe .local/OpenForma/.agents/skills/forma-hardware/scripts/forma.py tools
```

- If MCP cannot connect, check the backend terminal and whether port 8000 is already in use.
- If CAD setup fails, use the adapter's reported diagnostic; a connected MCP server alone does not establish native CAD readiness.
- Stop the backend with Ctrl+C. Start it again with `start-design.ps1` when needed.
- `.local/` holds the pinned upstream checkout, virtual environment, SQLite database, and persistent local encryption key. It is excluded from Git. Keep the key with any backup of encrypted local settings.
- Upstream source is pinned to `718d955c42bb31fd30b512c3a9f08c68f25c02e5`; Python dependencies follow upstream constraints rather than a project lockfile.

The backend binds to loopback in local authentication mode. Generated exports are prototype artifacts; record actual export and validation results alongside each design.
