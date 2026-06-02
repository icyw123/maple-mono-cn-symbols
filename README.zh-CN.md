# Maple Mono NF CN Symbols

[English](README.md) | 简体中文

给 [Maple Mono NF CN](https://github.com/subframe7536/maple-font) 补上一批**半角符号字形**（圆圈数字、几何图形、星标、Dingbats、罗马数字……），让它们在终端里正确对齐。符号取自 [Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd)。

字族 `Maple Mono NF CN Symbols` · 四个字重（Regular / Bold / Italic / Bold Italic）· SIL OFL-1.1。

## 为什么

Maple Mono 缺少 `①②③`、`●■▲`、`★`、`✓`、`Ⅰ Ⅱ Ⅲ` 这类字符。终端会回退到别的字体，而那些字体的**全角（2 格）**字形被塞进终端预留的**1 格**里，于是溢出、跟后面的字符重叠，排版错乱。

Warp / Ghostty 把这些字符按 **1 格**排版，所以字形必须是**半角**才装得下。本字体把 Sarasa 的半角符号缩放贴到 Maple 的 600 单位（1 格）网格上，Maple 自带的拉丁 / 中文 / Nerd 字形原样保留。

## 覆盖范围

只补 Maple 缺、而 Sarasa 有的码位（制表符、块元素 Maple 已有，不动）：

| 区块 | 范围 | 示例 |
|---|---|---|
| 圆圈数字等 | U+2460–24FF | ① ② ⑴ ⒈ |
| 几何图形 | U+25A0–25FF | ● ■ ▲ ◆ ○ |
| 杂项符号 | U+2600–26FF | ★ ☆ ☀ ⚑ |
| Dingbats | U+2700–27BF | ✓ ✗ ➜ ❤ |
| 罗马数字 | U+2160–217F | Ⅰ Ⅱ Ⅲ Ⅳ |
| 度数符号 | U+2103 / 2109 | ℃ ℉ |

罗马数字在 Maple 里是全角（会重叠），这里一并换成半角。

## 安装

从 [Releases](https://github.com/icyw123/maple-mono-cn-symbols/releases/latest) 下载，或直接用仓库里的 `fonts/`：

```sh
cp fonts/*.ttf ~/Library/Fonts/
```

## 配置终端

**Warp** —— `~/.warp/settings.toml`：

```toml
[appearance.text]
font_name = "Maple Mono NF CN Symbols"
```

**Ghostty** —— `~/.config/ghostty/config`：

```
font-family = Maple Mono NF CN Symbols
grapheme-width-method = unicode
```

改完**完全重启**终端（Warp 用 ⌘Q）。

## 自行构建

```sh
pip install -r requirements.txt
python build.py
```

会下载上游字体，用 fontTools 把 Sarasa 的符号 ×1.2 缩放后移植进 Maple，输出四个字重到 `fonts/`。细节见 `build.py`。

## 许可与致谢

SIL Open Font License 1.1，见 [LICENSE.txt](LICENSE.txt)。可自由使用、研究、修改、再分发，但不得单独售卖，衍生品须保持 OFL。

基于 [Maple Mono](https://github.com/subframe7536/maple-font)（subframe7536）、[Sarasa Term SC Nerd](https://github.com/laishulu/Sarasa-Term-SC-Nerd) / [Sarasa Gothic](https://github.com/be5invis/Sarasa-Gothic)（Belleve Invis）、[Source Han Sans](https://github.com/adobe-fonts/source-han-sans)（Adobe）构建。
