# Maple Mono NF CN Symbols

A monospaced terminal font: **[Maple Mono NF CN](https://github.com/subframe7536/maple-font)** (rounded Latin + CJK + Nerd Font icons) with **half-width symbol glyphs** (circled numbers, geometric shapes, dingbats, Roman numerals …) grafted in from **[Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd)** so they align correctly in the terminal.

Family: `Maple Mono NF CN Symbols` · 4 weights (Regular / Bold / Italic / Bold Italic) · SIL OFL-1.1.

## Motivation

In Warp / Ghostty, characters like `①②③`, `●■▲`, `★`, `✓`, `Ⅰ Ⅱ Ⅲ` are missing from Maple Mono. The terminal then falls back to another installed font, and that font's **full-width (2-cell)** glyph gets crammed into the **1-cell** slot the terminal reserved — so it overflows and **overlaps the next character** (e.g. a following `:`). The result is misaligned, garbled symbol output.

```
broken:    ①:②:③:      ← fallback full-width glyph overflows into the colon
fixed:     ① : ② : ③ :  ← (each symbol sits cleanly in 1 cell)
```

## Key finding: terminals measure these as 1 cell, so the glyph must be half-width

Tested empirically in Warp, version by version:

> **Warp lays out `①` as 1 cell (half-width) per `wcwidth`, regardless of the width the font declares.** A full-width (2-cell) glyph stuffed into that 1-cell slot overflows to the right and overlaps. Only a **half-width** glyph fits exactly.

Control experiment: a full-width symbol build (made from LXGW WenKai) showed every `①` overlapping in Warp; a half-width build (made from Sarasa) aligned perfectly. So this font ports **Sarasa's half-width** symbol designs — Sarasa's half-width body is 500 units, scaled **×1.2** to land on Maple's **600-unit (1-cell)** grid, with advance widths snapped to multiples of 600 (`①` = 600 = exactly 1 cell).

This is a **symbol-glyph completion**, not a CJK completion — Maple's own Latin/CJK/Nerd glyphs are untouched.

## Coverage (grafted Unicode blocks)

Only code points that Maple **lacks** and Sarasa **has** are grafted (box-drawing/block-element ranges are listed in the build but auto-excluded because Maple already has them, so line-drawing is never disturbed):

| Block | Range | Examples |
|---|---|---|
| Enclosed Alphanumerics (circled) | `U+2460–24FF` | ① ② ③ ⑴ ⑵ ⒈ |
| Geometric Shapes | `U+25A0–25FF` | ● ■ ▲ ▶ ◆ ○ |
| Miscellaneous Symbols | `U+2600–26FF` | ★ ☆ ☀ ☁ ⚑ |
| Dingbats | `U+2700–27BF` | ✓ ✗ ✦ ➜ ❤ |
| Roman Numerals | `U+2160–217F` | Ⅰ Ⅱ Ⅲ Ⅳ Ⅴ |
| Degree signs | `U+2103`, `U+2109` | ℃ ℉ |

## Install

**Download** the four `.ttf` files in [`fonts/`](fonts/) and install them (double-click → *Install Font*, or copy to `~/Library/Fonts/` on macOS).

```sh
cp fonts/*.ttf ~/Library/Fonts/
```

**Or build it yourself** (downloads the upstream fonts via your proxy, then grafts and outputs to `fonts/`):

```sh
pip install -r requirements.txt
python build.py
```

## Configure your terminal

**Warp** — `~/.warp/settings.toml`:

```toml
[appearance.text]
font_name = "Maple Mono NF CN Symbols"
```

**Ghostty** — `~/.config/ghostty/config`:

```
font-family = Maple Mono NF CN Symbols
```

Then fully restart the terminal (⌘Q for Warp). Test string:

```
①:②:③:④:
A:中:1:B:
①①①①①
```

`①` should occupy exactly 1 cell, never overlap the colon, and line up with `A:中:1:`.

## How it's built

`build.py` (≈130 lines, fontTools only):

1. Open Sarasa, **delete its layout tables** (`GSUB/GPOS/GDEF/BASE/JSTF/MATH`) — the Nerd-patched GSUB contains a lookup fontTools can't parse, and we only want outlines.
2. **Subset** Sarasa down to the target code points that Maple is missing — *or* ships full-width (Maple's Roman numerals `Ⅰ Ⅱ Ⅲ` are 2-cell; those get overridden too so they align like everything else).
3. **Scale ×1.2** (simple glyphs, composite component offsets, advance/lsb) so 500 → 600.
4. Open Maple **lazily** (never touching its equally-unparseable GSUB) and **graft** the scaled glyphs into its `glyf/hmtx/cmap` — glyph names prefixed `sym_`, composite dependencies followed, `glyphOrder`/`maxp` updated, all Unicode cmap subtables mapped.
5. **Snap** advance widths to multiples of 600.
6. Rewrite the `name` table to the new family, keeping each weight's Maple-native bold/italic flags.

## License & Acknowledgements

Licensed under the **SIL Open Font License, Version 1.1** — see [`LICENSE.txt`](LICENSE.txt). It may be used, studied, modified and redistributed freely, but **not sold by itself**, and derivatives must stay under OFL.

Built on the work of, and with thanks to:

- **[Maple Mono](https://github.com/subframe7536/maple-font)** by subframe7536 — the base font.
- **[Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd)** by laishulu, built on **[Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic)** / **[Iosevka](https://github.com/be5invis/Iosevka)** by Belleve Invis — the half-width symbol source.
- **[Source Han Sans](https://github.com/adobe-fonts/source-han-sans)** by Adobe — the CJK design underlying Sarasa.

Neither Maple nor Sarasa declares a Reserved Font Name, so this derivative legally retains the `Maple` name.
