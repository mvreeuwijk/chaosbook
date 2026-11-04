"""Copy the hand-drawn schematics of the chapter from the Maple edition.

These figures have no generating script (drawn by hand):
  cont2d_phasespace, cont2d_phase_r1..r3, cont2d_phase_i1..i3,
  cont2d_classification, cont2d_zoo
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "maple" / "_static" / "cont2d"
OUT = ROOT / "python" / "_static" / "cont2d"
OUT.mkdir(parents=True, exist_ok=True)

NAMES = (["cont2d_phasespace", "cont2d_classification", "cont2d_zoo"]
         + [f"cont2d_phase_{k}{i}" for k in "ri" for i in (1, 2, 3)])
for name in NAMES:
    shutil.copy2(SRC / f"{name}.png", OUT / f"{name}.png")
print("copied", len(NAMES), "schematics to", OUT)
