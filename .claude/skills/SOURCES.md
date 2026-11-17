# Installed skills

| Skill | Source | Commit |
|---|---|---|
| ghost-editor | https://github.com/kurbaitaev/ghost-editor | 2566950 |
| motion-design | https://github.com/howseen-ai/claude-motion-design (`skill/motion-design`) | 3d90d34 |
| lemo-opuscar | https://github.com/lemomo-ai/lemo-opuscar (`plugin/skills/lemo-opuscar`) | fdc46d7 |
| anthropics/skills (20 skills: academy-guide, algorithmic-art, brand-guidelines, canvas-design, claude-api, discernment-nudge, doc-coauthoring, docx, frontend-design, internal-comms, mcp-builder, pdf, pptx, skill-creator, slack-gif-creator, template-skill, theme-factory, web-artifacts-builder, webapp-testing, xlsx) | https://github.com/anthropics/skills (`skills/*`, via `npx skills add`, see skills-lock.json) | e4bb5d9 |
| superpowers (15 skills) | https://github.com/obra/superpowers (`skills/*`) | 22f0b46 |
| vercel agent-skills (9 skills) | https://github.com/vercel-labs/agent-skills (`skills/*`) | 1a2c79d |
| find-skills | https://github.com/vercel-labs/skills (`skills/find-skills`) | 57217cf |
| remotion-* (13 skills) | https://github.com/remotion-dev/skills (`skills/*`) | 3e20ac7 |
| gsap-* (8 skills) | https://github.com/greensock/gsap-skills (`skills/*`) | aed9cfd |
| hyperframes and related (9 skills) | https://github.com/heygen-com/hyperframes (`skills/*`) | bc5259d |
| ui-ux-pro-max, design, design-system, brand, banner-design, slides, ui-styling | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (`.claude/skills/*`) | e59ff37 |
| impeccable | https://github.com/pbakaus/impeccable (`.claude/skills/impeccable`) | d41d986 |
| humanizer | https://github.com/blader/humanizer (repo root, without git/plugin metadata) | b48c832 |

Media and tools that are not in git are fetched on first use:
- ghost-editor: `python3 .claude/skills/ghost-editor/scripts/library_restore.py`, then `bash .claude/skills/ghost-editor/scripts/doctor.sh`
- lemo-opuscar: `sh .claude/skills/lemo-opuscar/scripts/setup.sh` and `... setup.sh deps`
