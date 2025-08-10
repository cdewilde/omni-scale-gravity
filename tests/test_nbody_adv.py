import math, numpy as np
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
import nbody_adv as nb

def test_binary_energy_near_constant():
    x,v,m = nb.circular_binary_ic(1e22, 1e22, 1e7)
    out = nb.leapfrog(x, v, m, dt=0.25, steps=2000, record_every=100)
    E0 = out[0]['E']; E1 = out[-1]['E']
    assert abs((E1-E0)/E0) < 1e-2
