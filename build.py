#!/usr/bin/env python3
"""Build "Maple Mono NF CN Symbols" = Maple Mono NF CN + symbol glyphs grafted
from Sarasa Term SC Nerd (half-width, scaled 1.2x to Maple's 600 cell)."""
import os, sys, tarfile, zipfile, urllib.request
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.subset import Subsetter, Options as SubOptions

HERE   = os.path.dirname(os.path.abspath(__file__))
CACHE  = os.path.join(HERE, "build")
FONTS  = os.path.join(HERE, "fonts")
os.makedirs(CACHE, exist_ok=True); os.makedirs(FONTS, exist_ok=True)

MAPLE_URL  = "https://github.com/subframe7536/maple-font/releases/download/v7.9/MapleMono-NF-CN-unhinted.zip"
SARASA_URL = "https://github.com/laishulu/Sarasa-Term-SC-Nerd/releases/download/v2.3.1/SarasaTermSCNerd-Unhinted.ttf.tar.gz"

FAMILY, PSFAMILY, VERSION = "Maple Mono NF CN Symbols", "MapleMonoNFCNSymbols", "1.000"
COPYRIGHT = ("Copyright 2024 The Maple Mono Project Authors (https://github.com/subframe7536/maple-font). "
             "Portions Copyright Belleve Invis and Sarasa Gothic project (https://github.com/be5invis/Sarasa-Gothic), "
             "Iosevka project, and Source Han Sans (Copyright 2014-2021 Adobe). "
             "This derivative 'Maple Mono NF CN Symbols' assembled 2026.")
LICENSE_DESC = ("This Font Software is licensed under the SIL Open Font License, Version 1.1. "
                "This license is available with a FAQ at: https://openfontlicense.org")
LICENSE_URL = "https://openfontlicense.org"

# (maple_style_in_filename, sarasa_style_in_filename, subfamily, ps_style)
WEIGHTS = [
    ("Regular",    "Regular",    "Regular",     "Regular"),
    ("Bold",       "Bold",       "Bold",        "Bold"),
    ("Italic",     "Italic",     "Italic",      "Italic"),
    ("BoldItalic", "BoldItalic", "Bold Italic", "BoldItalic"),
]
TARGET_RANGES = [(0x2460,0x24FF),(0x2500,0x257F),(0x2580,0x259F),(0x25A0,0x25FF),
                 (0x2600,0x26FF),(0x2700,0x27BF),(0x2103,0x2103),(0x2109,0x2109),(0x2160,0x217F)]
SCALE, CELL, PREFIX = 1.2, 600, "sym_"

def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        print("  cached:", os.path.basename(dest)); return
    print("  downloading:", url)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=600) as r, open(dest, "wb") as f:
        f.write(r.read())

def ensure_sources():
    """下载并解压上游, 返回 (maple_dir, sarasa_dir)。自动走环境里的 http(s)_proxy。"""
    mzip = os.path.join(CACHE, "maple.zip"); star = os.path.join(CACHE, "sarasa.tar.gz")
    download(MAPLE_URL, mzip); download(SARASA_URL, star)
    mdir = os.path.join(CACHE, "maple_fonts"); sdir = os.path.join(CACHE, "sarasa_fonts")
    if not os.path.isdir(mdir):
        os.makedirs(mdir, exist_ok=True)
        with zipfile.ZipFile(mzip) as z: z.extractall(mdir)
    if not os.path.isdir(sdir):
        os.makedirs(sdir, exist_ok=True)
        with tarfile.open(star) as t: t.extractall(sdir)
    # 容错: 文件可能在子目录里, 用 find 平铺定位
    def find(root, name):
        for dp, _, fns in os.walk(root):
            if name in fns: return os.path.join(dp, name)
        raise FileNotFoundError(name)
    return mdir, sdir, find

def scale_glyphs(font, scale):
    glyf, hmtx = font["glyf"], font["hmtx"]
    for gname in glyf.keys():
        g = glyf[gname]
        if g.numberOfContours == 0:
            pass
        elif g.isComposite():
            for c in g.components:
                c.x = round(c.x*scale); c.y = round(c.y*scale)
        elif hasattr(g, "coordinates"):
            g.coordinates = GlyphCoordinates([(round(x*scale), round(y*scale)) for x,y in g.coordinates])
        adv, lsb = hmtx[gname]; hmtx[gname] = (round(adv*scale), round(lsb*scale))

def set_names(font, subfamily, ps_style):
    name = font["name"]; full = f"{FAMILY} {subfamily}"; ps = f"{PSFAMILY}-{ps_style}"
    for plat, enc, lang in [(3,1,0x409),(1,0,0)]:
        name.setName(COPYRIGHT, 0, plat, enc, lang)
        name.setName(FAMILY,    1, plat, enc, lang)
        name.setName(subfamily, 2, plat, enc, lang)
        name.setName(full,      4, plat, enc, lang)
        name.setName(f"Version {VERSION}", 5, plat, enc, lang)
        name.setName(ps,        6, plat, enc, lang)
        name.setName(LICENSE_DESC, 13, plat, enc, lang)
        name.setName(LICENSE_URL,  14, plat, enc, lang)
        name.setName(FAMILY,    16, plat, enc, lang)
        name.setName(subfamily, 17, plat, enc, lang)
    font["head"].fontRevision = float(VERSION)

def build_weight(maple_path, sarasa_path, subfamily, ps_style, out):
    src = TTFont(sarasa_path)
    for tag in ("GSUB","GPOS","GDEF","BASE","JSTF","MATH"):
        if tag in src: del src[tag]
    maple = TTFont(maple_path, lazy=True)
    mcmap = maple.getBestCmap(); mc = set(mcmap); sc = src.getBestCmap()
    mhmtx0 = maple["hmtx"]
    def overflows(cp):
        # Maple HAS this code point but as a full-width (>1 cell) glyph (e.g. Roman
        # numerals at 1200). Terminals lay these out as 1 cell (East Asian Ambiguous),
        # so the full-width glyph overflows and overlaps -> override with Sarasa half-width.
        sn = mcmap.get(cp)
        return sn is not None and mhmtx0[sn][0] > CELL
    # graft Sarasa's half-width glyph when Maple lacks the code point OR ships it full-width
    miss = [cp for lo,hi in TARGET_RANGES for cp in range(lo,hi+1)
            if cp in sc and (cp not in mc or overflows(cp))]
    opts = SubOptions(); opts.glyph_names=True; opts.layout_features=[]; opts.name_IDs=[]; opts.notdef_outline=True
    ss = Subsetter(options=opts); ss.populate(unicodes=miss); ss.subset(src)
    scale_glyphs(src, SCALE)

    mglyf, mhmtx = maple["glyf"], maple["hmtx"]
    sglyf, shmtx, scmap = src["glyf"], src["hmtx"], src.getBestCmap()
    need, cp2sn = set(), {}
    def collect(sn):
        if sn in need: return
        need.add(sn); g = sglyf[sn]
        if g.isComposite():
            for c in g.components: collect(c.glyphName)
    for cp in miss:
        sn = scmap.get(cp)
        if sn: cp2sn[cp] = sn; collect(sn)
    order = maple.getGlyphOrder()
    for sn in need:
        new = PREFIX+sn; g = sglyf[sn]
        if g.isComposite():
            for c in g.components: c.glyphName = PREFIX+c.glyphName
        mglyf[new] = g; mhmtx[new] = shmtx[sn]
        if new not in order: order.append(new)
    maple.setGlyphOrder(order); maple["maxp"].numGlyphs = len(order)
    for t in maple["cmap"].tables:
        if t.isUnicode():
            for cp, sn in cp2sn.items(): t.cmap[cp] = PREFIX+sn
    for cp, sn in cp2sn.items():
        new = PREFIX+sn; adv, lsb = mhmtx[new]
        mhmtx[new] = (max(round(adv/CELL)*CELL, CELL), lsb)

    set_names(maple, subfamily, ps_style)
    maple.save(out); maple.close(); src.close()
    print(f"  [{subfamily}] 补 {len(cp2sn)} 字形 -> {out}")

def verify():
    for _,_,sub,ps in WEIGHTS:
        p = os.path.join(FONTS, f"{PSFAMILY}-{ps}.ttf"); f = TTFont(p, lazy=True)
        hmtx = f["hmtx"]; cmap = f.getBestCmap()
        a = lambda ch: hmtx[cmap[ord(ch)]][0] if ord(ch) in cmap else None
        fam = f["name"].getName(1,3,1,0x409); psn = f["name"].getName(6,3,1,0x409)
        print(f"  {ps:11s} family={fam} ps={psn} M={a('M')} 中={a('中')} ①={a('①')}(={round(a('①')/600)}格)")
        f.close()

def main():
    print("== 下载/准备上游 =="); mdir, sdir, find = ensure_sources()
    print("== 生成 4 字重 ==")
    for mstyle, sstyle, sub, ps in WEIGHTS:
        mp = find(mdir, f"MapleMono-NF-CN-{mstyle}.ttf")
        sp = find(sdir, f"SarasaTermSCNerd-{sstyle}.ttf")
        build_weight(mp, sp, sub, ps, os.path.join(FONTS, f"{PSFAMILY}-{ps}.ttf"))
    print("== 验证 =="); verify()

if __name__ == "__main__":
    main()
