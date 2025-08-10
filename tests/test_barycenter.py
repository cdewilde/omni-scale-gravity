import numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
import nbody_adv as nb

def test_binary_barycenter_stable():
    x, v, m = nb.circular_binary_ic(1.0e22, 1.0e22, 1.0e7)
    out = nb.leapfrog(x, v, m, dt=0.25, steps=800, record_every=40)
    Rmax = 0.0
    for s in out:
        Rc, Vc = nb.barycenter(s['x'], s['v'], m)
        Rmax = max(Rmax, float((Rc**2).sum())**0.5)
    assert Rmax < 1e-3  # near zero (COM frame)
