# Maple Mono NF CN Symbols

English | [简体中文](README.zh-CN.md)

[Maple Mono NF CN](https://github.com/subframe7536/maple-font) with **half-width symbol glyphs** (circled numbers, geometric shapes, stars, dingbats, Roman numerals …) grafted in from [Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd), so they line up in the terminal.

Family `Maple Mono NF CN Symbols` · 4 weights (Regular / Bold / Italic / Bold Italic) · SIL OFL-1.1.

## Why

Maple Mono lacks `①②③`, `●■▲`, `★`, `✓`, `Ⅰ Ⅱ Ⅲ`. The terminal falls back to another font, whose **full-width (2-cell)** glyph gets crammed into the **1-cell** slot the terminal reserved — so it overflows and overlaps the next character.

Warp / Ghostty lay these out as **1 cell**, so the glyph has to be **half-width** to fit. This font scales Sarasa's half-width symbols onto Maple's 600-unit (1-cell) grid. Maple's own Latin / CJK / Nerd glyphs are untouched.

## Coverage

Only code points Maple lacks and Sarasa has (box-drawing and block elements are left alone — Maple already has them):

| Block | Range | Examples |
|---|---|---|
| Enclosed Alphanumerics | U+2460–24FF | ① ② ⑴ ⒈ |
| Geometric Shapes | U+25A0–25FF | ● ■ ▲ ◆ ○ |
| Misc Symbols | U+2600–26FF | ★ ☆ ☀ ⚑ |
| Dingbats | U+2700–27BF | ✓ ✗ ➜ ❤ |
| Roman Numerals | U+2160–217F | Ⅰ Ⅱ Ⅲ Ⅳ |
| Degree signs | U+2103 / 2109 | ℃ ℉ |

Roman numerals are full-width in Maple (so they overlap) — those get overridden with the half-width versions too.

## Install

Download from [Releases](https://github.com/icyw123/maple-mono-cn-symbols/releases/latest), or use the `fonts/` in this repo:

```sh
cp fonts/*.ttf ~/Library/Fonts/
```

## Configure

**Warp** — `~/.warp/settings.toml`:

```toml
[appearance.text]
font_name = "Maple Mono NF CN Symbols"
```

**Ghostty** — `~/.config/ghostty/config`:

```
font-family = Maple Mono NF CN Symbols
grapheme-width-method = unicode
```

Then fully restart the terminal (⌘Q for Warp).

## Build

```sh
pip install -r requirements.txt
python build.py
```

Downloads the upstream fonts, then uses fontTools to scale Sarasa's symbols ×1.2 and graft them into Maple, writing the 4 weights to `fonts/`. Details are in `build.py`.

## License & Credits

SIL Open Font License 1.1 — see [LICENSE.txt](LICENSE.txt). Free to use, study, modify and redistribute; not to be sold by itself; derivatives stay under OFL.

Built on [Maple Mono](https://github.com/subframe7536/maple-font) (subframe7536), [Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) / [Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic) (Belleve Invis), and [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) (Adobe).
