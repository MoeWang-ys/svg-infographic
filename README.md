# SVG Infographic

[中文 README](./README.zh.md)

**Make diagrams with your coding agent — no image-generation model needed.**

Architecture diagrams, flowcharts, comparison charts, README banners. Accurate labels, clean vectors, ~8 KB per file.

Ask for a diagram, get a diagram:

![svg-infographic overview](assets/hero.svg)

## Why no image model

Image models **draw the picture for you — and get the words wrong.** Chinese especially. An infographic is 100% about its words, so a typo is a dead image.

This skill skips image models entirely. Your agent writes SVG by hand, so **every word is exactly the word you wrote** — and you can edit one label without regenerating the whole picture.

| | Image-gen AI | This skill |
|---|---|---|
| **Uses an image model** | Yes, the whole point | **No** |
| Text accuracy | Often misspells — worse in Chinese | **100% yours** |
| Change one word | Regenerate everything | Edit one line |
| File size | Hundreds of KB to MBs | **~8 KB, vector** |
| Style consistency | Drifts every run | Identical every time |
| Version control | ❌ Binary | ✅ Text diff |
| API key / cost per image | Required, paid | **None** |

Use it when **text matters**. Use an image model for illustrations and mood shots. Use Mermaid for pure logic diagrams — GitHub renders it natively for free.

## What you get

- **Every label spelled right** — including Chinese, which image models mangle most.
- **Editable forever** — change one word, not the whole picture. Re-run any time, same result.
- **~8 KB vector files** — crisp at any zoom, cheap to commit, diffable in git.
- **No API key, no per-image cost** — it's just SVG and Chrome, both already on your machine.
- **Verified, not vibes** — every diagram is checked for text overflow, blank regions and colour drift before you ship it.
- **Looks intentional** — a warm sand / terracotta / ink-teal palette that avoids the neon-on-navy, purple-gradient AI look.
- **Bilingual out of the box** — Chinese and English layouts measured separately, because English runs wider.
- **A dark HTML template** with copy / PNG / PDF export buttons.

## Who is this for

Anyone whose coding agent needs to produce a diagram with **accurate labels** — project READMEs, architecture docs, internal explainers. Especially if you work in Chinese.

## Installation

Copy `SKILL.md` into your agent's skills directory:

```bash
# pi
mkdir -p ~/.pi/agent/skills/svg-infographic
cp SKILL.md ~/.pi/agent/skills/svg-infographic/

# Claude Code (project-level)
mkdir -p .claude/skills/svg-infographic
cp SKILL.md .claude/skills/svg-infographic/
```

Requirements:

```bash
Google Chrome              # rendering, screenshots, and measuring text bounds
python3
pip install pillow numpy   # pixel analysis + PNG compression
```

Then just ask: *"draw an architecture diagram for this README."*

## Trigger Phrases

- "给 README 配图"
- "画个架构图" / "做个流程图" / "画张对比图"
- "画图说明一下" / "整个图看看"
- "illustrate this in a diagram" / "make an infographic"

## Repository Layout

```
SKILL.md                      the methodology
scripts/
  svg2png.sh                  SVG → PNG (Chrome headless + Pillow)
  check_overflow.py           text overflow detection
  check_pixels.py             ink coverage, luminance, band analysis
references/
  dark-template.html          dark HTML template with export buttons
assets/                       example diagrams
```

Hard-won rules and pitfalls (pipeline flags, font stacks, compression, palette) live in [`RULES.md`](RULES.md).

## Quality checks it runs on itself

Before a diagram ships, it gets measured — not eyeballed. Real output from the scripts in this repo:

```
Labels overflowing the canvas   0 of 34
Blank regions                    none (6/6 bands have content)
File size                       138 KB → 51 KB, no visible colour shift
Renders on GitHub               yes (1800 × 930 loaded)
```

## Credits

- Structure techniques absorbed from [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT). Its dark-neon palette is not this skill's default.
- `references/dark-template.html` © Cocoon AI, MIT — see `references/dark-template-LICENSE`.
- Palette guardrails from `huashu-design`.

## License

MIT
