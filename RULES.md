# Rules & Pitfalls

Hard-won rules for the SVG → PNG pipeline. Kept out of the README; read this before you debug a broken diagram.

## Render pipeline

| Rule | Why |
|---|---|
| `--window-size` must be ≥ viewBox size | Otherwise Chrome crops the image |
| Use absolute paths with `file://` | Relative paths are unreliable |
| `SCALE=1.5` is the sweet spot | 2× is too heavy, 1× is blurry on retina |
| Don't use cairosvg | Missing `libcairo.2.dylib` on macOS; can't be made to work |
| `fonts.googleapis.com` is blocked in China | Webfonts silently fall back |

## Text

| Rule | Why |
|---|---|
| Always write the full font stack | Otherwise Chinese becomes tofu boxes on Windows/Linux |
| Don't mix CJK and ASCII alignment | CJK glyphs are double-width; ASCII-tuned columns break |
| Measure English separately from Chinese | English runs wider — a translated diagram overflows |
| `<text>` needs `role="img"` + `aria-label` on the parent | Accessibility + SEO |

Full font stack:
```
ui-sans-serif,-apple-system,'PingFang SC','Microsoft YaHei',sans-serif
```
`PingFang SC` (macOS) → `Microsoft YaHei` (Windows) → `sans-serif` (Linux).

## Drawing order

SVG paints in document order — **later elements cover earlier ones.**

- Draw arrows **before** boxes, if arrows pass through boxes
- Better: route arrows so they don't pass through boxes at all
- Semi-transparent boxes do **not** hide arrows behind them

## PNG compression

| Rule | Why |
|---|---|
| `colors=128` is enough | Flat illustration palettes have few layers; 256 saves almost nothing |
| `dither=Image.NONE` **is mandatory** | Dithering *increases* file size and adds noise |
| Always verify pixel error afterwards | Don't ship colour drift |

```python
q = im.quantize(colors=128, method=Image.MEDIANCUT, dither=Image.NONE)
err = np.abs(a - b).mean()   # must be < 1.5
```

## Verifying without eyes

Most models can't see images. Never assume — measure.

| Check | Method |
|---|---|
| Text overflow | `getBBox()` on every `<text>` inside Chrome |
| Render succeeded | Ink coverage > 0, darkest luminance < 90 |
| Blank regions | Split into horizontal bands; middle bands must not be empty |
| Palette drift | Sample known coordinates |
| GitHub actually loads it | `naturalWidth !== 0` |

## Reading a diagram in a browser

| Symptom | Cause | Fix |
|---|---|---|
| `naturalWidth = 0`, blank preview | Chrome blocks `file://` images | Inline images as base64 |
| Injected script can't read the SVG | `fetch()` blocked by CORS | Inline the SVG into the HTML |
| Script reports arrows as occluded, but they aren't | Cross-`<g>` coordinate mismatch | Use `getBoundingClientRect()` |

## Palette guardrails

From `huashu-design`'s no-go list:

- ❌ Neon on dark navy
- ❌ Purple gradients
- ❌ Emoji as icons

Default palette: warm sand background, terracotta accents, ink-teal text.

## Layout reference

| Element | Spacing |
|---|---|
| Component boxes | 24 px gap minimum |
| Section groups | 48 px |
| Legend | Must sit **outside** the bounding box of the content it describes |

## ASCII diagrams

Don't draw ASCII art in a diagram that contains Chinese — the double-width glyphs break every alignment you tuned.

## Provenance

2026-09-30, while making README illustrations for `pi-web-extensions`. Result: 3 Chinese diagrams with 86 text elements, zero overflow; English versions re-laid-out and also zero overflow; all 6 diagrams passed 4 programmatic checks before shipping.
