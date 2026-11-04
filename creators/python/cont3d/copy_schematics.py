"""Copy the hand-drawn cont3d schematics (no Maple script) from the Maple
edition into the Python edition.

  cont3d_poincaresection.png  Poincare section sketch (after Strogatz)
  cont3d_doublewell.png       sketch of the forced double-well beam
  cont3d_lyap_formal.png      sketch of a perturbation along a trajectory
  cont3d_rosslertopology.png  sketch of the Rossler attractor's band topology
"""

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "maple" / "_static" / "cont3d"
DST = ROOT / "python" / "_static" / "cont3d"
DST.mkdir(parents=True, exist_ok=True)

for name in ["cont3d_poincaresection", "cont3d_doublewell",
             "cont3d_lyap_formal", "cont3d_rosslertopology"]:
    shutil.copy2(SRC / f"{name}.png", DST / f"{name}.png")
    print("copied", name)
