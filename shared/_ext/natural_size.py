"""Show images in HTML at their printed size.

The Python edition's figures are saved at the size they are printed (the PNG
carries its dpi) and included without a :width:. LaTeX then places them at
exactly that size. A browser, however, shows a PNG at its pixel size, so a
300 dpi figure would come out three times too large.

This extension gives every image that has no explicit width or scale a CSS
width equal to its physical width (pixels / dpi), times
``natural_size_html_scale``. The factor accounts for the web body text being
larger relative to a page than the printed 11 pt: with the default 1.1 a
figure's 10 pt labels keep about the same size relative to the body text on
screen as on paper. Images wider than the content column still shrink to fit
(the theme sets max-width: 100%).

Only the HTML builders are affected; images without dpi metadata are left
alone.
"""

from pathlib import Path

from docutils import nodes

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    Image = None


def _natural_width_in(path):
    with Image.open(path) as im:
        dpi = im.info.get("dpi")
        if not dpi or not dpi[0]:
            return None
        return im.size[0] / float(dpi[0])


def _resolve(app, docname, uri):
    if uri.startswith(("http:", "https:", "data:")):
        return None
    src_dir = Path(app.srcdir)
    cand = [src_dir / uri.lstrip("/"),
            (src_dir / Path(app.env.doc2path(docname)).parent / uri)]
    for c in cand:
        if c.is_file():
            return c
    return None


def size_images(app, doctree, docname):
    if Image is None or app.builder.format != "html":
        return
    scale = app.config.natural_size_html_scale
    for node in doctree.findall(nodes.image):
        if node.get("width") or node.get("height") or node.get("scale"):
            continue
        uri = node.get("uri", "")
        if not uri.lower().endswith(".png"):
            continue
        path = _resolve(app, docname, uri)
        if path is None:
            continue
        try:
            w = _natural_width_in(path)
        except OSError:
            continue
        if w is None or w > 20:   # no dpi, or not a figure (e.g. a photo at 1 dpi)
            continue
        node["width"] = f"{w * scale:.2f}in"


def setup(app):
    app.add_config_value("natural_size_html_scale", 1.1, "html")
    app.connect("doctree-resolved", size_images)
    return {"version": "1.0", "parallel_read_safe": True,
            "parallel_write_safe": True}
