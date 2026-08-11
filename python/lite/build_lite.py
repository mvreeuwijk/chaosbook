"""Build the JupyterLite lab layer (sub-project 3 of the vision spec).

Stages the lab contents, builds the chaosbook wheel for piplite, and runs
``jupyter lite build``. One entry point for the Makefile and CI:

    python python/lite/build_lite.py [output_dir]

output_dir defaults to build/lite at the repo root. The staged contents are
the committed files/ tree (lab notebooks plus the exercise datasets under
data/, so np.loadtxt("data/set1.txt") works inside the browser and under
local nbconvert execution alike) and a launchable copy of the cookbook
notebook with a %pip setup cell inserted.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

LITE = Path(__file__).resolve().parent
REPO = LITE.parents[1]

SETUP_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Run this cell first: it installs the book's package into the\n",
        "# in-browser Python (takes a few seconds, needs to run once per visit).\n",
        "%pip install -q chaosbook ipywidgets",
    ],
}


def make_cookbook_copy(dest):
    """Copy app_cookbook.ipynb with a setup cell and without site chrome."""
    nb = json.loads((REPO / "python" / "app_cookbook.ipynb").read_text(encoding="utf-8"))
    title = nb["cells"][0]
    # The PDF-download button block is site chrome (and MyST directives do
    # not render in JupyterLab markdown); drop it from the title cell.
    src = "".join(title["source"])
    src = re.sub(r"\n:::\{only\} html\n.*?\n:::\n", "\n", src, flags=re.DOTALL)
    title["source"] = src.splitlines(keepends=True)
    nb["cells"].insert(1, SETUP_CELL)
    dest.write_text(json.dumps(nb, indent=1), encoding="utf-8")


def main():
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else REPO / "build" / "lite"
    # A sibling marker (jupyter lite build wipes the output dir itself, so
    # nothing inside it survives a failed build) guards against clobbering a
    # directory this script did not create.
    marker = output.parent / (output.name + ".chaosbook-lite")
    if output.exists() and any(output.iterdir()) and not marker.exists():
        sys.exit(f"refusing to build into non-empty {output}: not a prior lite build")
    output.mkdir(parents=True, exist_ok=True)
    marker.touch()

    # Stage the contents afresh (ignore_errors: Windows can hold a transient
    # lock on the directory root; copytree overwrites whatever survives).
    stage = output.parent / (output.name + "-stage")
    if stage.exists():
        shutil.rmtree(stage, ignore_errors=True)
    shutil.copytree(LITE / "files", stage, dirs_exist_ok=True)
    make_cookbook_copy(stage / "cookbook.ipynb")

    # Build the pure-python wheel where the piplite addon bundles it, so
    # `%pip install chaosbook` resolves in the browser without PyPI.
    pypi = LITE / "pypi"
    pypi.mkdir(exist_ok=True)
    for old in pypi.glob("*.whl"):
        old.unlink()
    subprocess.run(
        [sys.executable, "-m", "build", "--wheel", "--outdir", str(pypi)],
        cwd=REPO, check=True,
    )

    subprocess.run(
        [sys.executable, "-m", "jupyter", "lite", "build",
         "--contents", str(stage), "--output-dir", str(output)],
        cwd=LITE, check=True,
    )
    print(f"\nJupyterLite lab built into {output}")


if __name__ == "__main__":
    main()
