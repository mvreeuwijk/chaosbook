"""Printed font size of every figure image in a Sphinx LaTeX build.

For each \\sphinxincludegraphics in main.tex: the printed width follows from
the width/height option or, without one, from the PNG's natural size
(pixels / dpi), capped at the containing width (\\linewidth, a 0.495
subfigure box, or a box inside an admonition). The image's own fonts were
set in points at natural size (book.mplstyle before the house style: tick
labels 11 pt, axis labels 13 pt), so on paper they are 11 * scale and
13 * scale, with scale = printed width / natural width.

Usage: python fontsize.py <latex dir> <out.csv>
"""
import csv
import re
import sys
from pathlib import Path

from PIL import Image

TW = 6.378          # text width, in (A4, hmargin 2.4 cm)
TH = 9.33           # text height, in (23.7 cm)
BOXW = TW - 20 / 72.27 - 20 / 72.27 * 0  # admonition: 10 pt padding each side
UNITS = {"mm": 1 / 25.4, "cm": 1 / 2.54, "in": 1.0, "pt": 1 / 72.27}

d = Path(sys.argv[1])
tex = (d / "main.tex").read_text(encoding="utf8")

tok = re.compile(r"(?m)" +
    r"(?m)\\chapter\{|^\\appendix\s*$|\\begin\{figure\}|\\end\{figure\}|"
    r"\\begin\{subfigure\}\{([\d.]+)\\(?:textwidth|linewidth)\}|\\end\{subfigure\}|"
    r"\\begin\{sphinxadmonition\}|\\end\{sphinxadmonition\}|"
    r"\\caption\{|\\sphinxincludegraphics(\[[^\]]*\])?\{\{([^}]*)\}(\.\w+)\}")

chap, appendix, fignum = 0, False, 0
in_fig = in_sub = False
sub_w = None
adm = 0
cur = None
rows = []


def length(v):
    m = re.match(r"([\d.]+)\\(linewidth|textwidth)", v)
    if m:
        return float(m.group(1)), "rel"
    m = re.match(r"([\d.]+)(mm|cm|in|pt)", v)
    if m:
        return float(m.group(1)) * UNITS[m.group(2)], "abs"
    return None, None


for m in tok.finditer(tex):
    t = m.group(0)
    if t.startswith("\\chapter"):
        chap += 1; fignum = 0
        continue
    if t.strip() == "\\appendix":
        appendix, chap = True, 0
        continue
    if t.startswith("\\begin{figure}"):
        in_fig, cur = True, []
        continue
    if t.startswith("\\end{figure}"):
        in_fig = False
        continue
    if t.startswith("\\begin{subfigure}"):
        in_sub, sub_w = True, float(m.group(1))
        continue
    if t.startswith("\\end{subfigure}"):
        in_sub = False
        continue
    if t.startswith("\\begin{sphinxadmonition}"):
        adm += 1; continue
    if t.startswith("\\end{sphinxadmonition}"):
        adm -= 1; continue
    if t.startswith("\\caption{"):
        if in_fig and not in_sub:
            fignum += 1
            label = (chr(64 + chap) if appendix else str(chap)) + f".{fignum}"
            for r in cur:
                r["fig"] = label
        continue
    # an image
    opts, base, ext = m.group(2) or "", m.group(3), m.group(4)
    f = d / f"{base}{ext}"
    try:
        im = Image.open(f)
        px, py = im.size
        dpi = (im.info.get("dpi") or (72, 72))[0] or 72
    except Exception:
        continue
    nw, nh = px / dpi, py / dpi
    lw = BOXW if adm else TW
    cont = sub_w * lw if in_sub else lw
    w = None
    o = opts.strip("[]")
    for part in o.split(","):
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        val, kind = length(v)
        if val is None:
            continue
        if k == "width":
            w = val * cont if kind == "rel" else val
        elif k == "height":
            h = val * TH if kind == "rel" else val
            w = h * nw / nh
    if w is None:
        w = nw
    w = min(w, cont)
    if w * nh / nw > TH:
        w = TH * nw / nh
    s = w / nw
    row = dict(chapter=(chr(64 + chap) if appendix else chap), fig="",
               image=base, option=o or "none", subfig=sub_w or "",
               in_box=bool(adm), dpi=round(dpi), natural_in=f"{nw:.2f}x{nh:.2f}",
               printed_cm=f"{w*2.54:.1f}x{w*nh/nw*2.54:.1f}", scale=round(s, 2),
               tick_pt=round(11 * s, 1), label_pt=round(13 * s, 1))
    rows.append(row)
    if in_fig and cur is not None:
        cur.append(row)

with open(sys.argv[2], "w", newline="", encoding="utf8") as fh:
    wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
    wr.writeheader(); wr.writerows(rows)
print(len(rows), "images")
