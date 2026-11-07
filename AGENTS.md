# Project guidance

## Physical design

- Use the `forma-hardware` skill and the `openforma` MCP server for OpenForma work.
- The selected upstream is `https://github.com/Mapped-Assembly/OpenForma`, installed under `.local/OpenForma` by `scripts/setup-design.ps1`.
- Run skill helpers with `.local/venv/Scripts/python.exe` on Windows so CAD and backend dependencies resolve consistently.
- Read `docs/physical-designs.md` for startup and verification. If the backend is stopped, run `scripts/start-design.ps1` in a persistent terminal/background process.
- OpenCode authors designs. Prefer host-authored compilation rather than server-side LLM generation unless the user requests the latter.
- Use the skill's fresh-project helper and keep design source and outputs in its returned project directory.
- Verify CAD availability with the adapter before building. Report only artifacts actually exported and checks actually performed.
- `.local/` contains runtime data and secrets; do not commit its contents.
