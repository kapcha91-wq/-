# Installed skills

| Skill | Source | Commit |
|---|---|---|
| ghost-editor | https://github.com/kurbaitaev/ghost-editor | 2566950 |
| motion-design | https://github.com/howseen-ai/claude-motion-design (`skill/motion-design`) | 3d90d34 |
| lemo-opuscar | https://github.com/lemomo-ai/lemo-opuscar (`plugin/skills/lemo-opuscar`) | fdc46d7 |

Media and tools that are not in git are fetched on first use:
- ghost-editor: `python3 .claude/skills/ghost-editor/scripts/library_restore.py`, then `bash .claude/skills/ghost-editor/scripts/doctor.sh`
- lemo-opuscar: `sh .claude/skills/lemo-opuscar/scripts/setup.sh` and `... setup.sh deps`
