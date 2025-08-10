"""
OSG N-body (vectorized, GPU-optional).
- CuPy if available, else NumPy.
- Leapfrog integrator with softening.
- Energy diagnostics.
"""
from __future__ import annotations
try:
    import cupy as xp
    BACKEND = "cupy"
except Exception:
    import numpy as xp
    BACKEND = "numpy"

G = 6.67430e-11

def pairwise_accel(x, m, eps=1e3):
    dx = x[:, None, :] - x[None, :, :]
    r2 = (dx*dx).sum(axis=2) + eps**2
    invr3 = 1.0 / (r2 * xp.sqrt(r2))
    xp.fill_diagonal(invr3, 0.0)
    a = -G * (dx * invr3[:, :, None]) @ (m[:, None])
    return a

def energy(x, v, m, eps=1e3):
    K = 0.5 * (m[:, None] * v * v).sum()
    dx = x[:, None, :] - x[None, :, :]
    r = xp.sqrt((dx*dx).sum(axis=2) + eps**2)
    invr = 1.0 / xp.where(r>0, r, xp.inf)
    U = -G * 0.5 * ((m[:, None] * m[None, :]) * invr).sum()
    return float(K), float(U), float(K+U)

def leapfrog(x, v, m, dt, steps, eps=1e3, record_every=1):
    x = x.copy(); v = v.copy()
    a = pairwise_accel(x, m, eps)
    v += 0.5*dt*a
    out = []
    for s in range(steps):
        x += dt*v
        a = pairwise_accel(x, m, eps)
        v += 0.5*dt*a
        if s % record_every == 0:
            K,U,E = energy(x, v, m, eps)
            out.append({"step": s, "x": xp.asnumpy(x), "v": xp.asnumpy(v), "E": E})
    return out

def circular_binary_ic(M1, M2, separation):
    m = xp.asarray([M1, M2], dtype=float)
    r = separation
    x = xp.asarray([[-r*M2/(M1+M2), 0, 0],
                    [ r*M1/(M1+M2), 0, 0]], dtype=float)
    vmag = (G*(M1+M2)/r)**0.5
    v1 =  vmag * M2/(M1+M2); v2 = vmag * M1/(M1+M2)
    v = xp.asarray([[0,  v1, 0],
                    [0, -v2, 0]], dtype=float)
    return x, v, m

def restricted_three_body_sun_earth_test(m_sun, m_earth, a_au, test_mass, r_test, v_test):
    AU = 1.495978707e11
    a = a_au * AU
    x_sun = xp.asarray([0.0, 0.0, 0.0]); x_earth = xp.asarray([a, 0.0, 0.0])
    v_e = xp.asarray([0.0, (G*(m_sun+m_earth)/a)**0.5, 0.0])
    v_s = - (m_earth/(m_sun)) * v_e
    x = xp.stack([x_sun, x_earth, r_test], axis=0)
    v = xp.stack([v_s, v_e, v_test], axis=0)
    m = xp.asarray([m_sun, m_earth, test_mass])
    return x, v, m

def barycenter(x, v, m):
    """Return (R_cm, V_cm) barycenter for positions x, velocities v, masses m."""
    M = m.sum()
    R = (m[:,None] * x).sum(axis=0) / M
    V = (m[:,None] * v).sum(axis=0) / M
    return R, V

def plummer_sphere(N, Mtot, a, seed=42):
    """
    Sample a toy Plummer sphere:
      - Positions sampled from exact Plummer CDF.
      - Velocities drawn from an isotropic Gaussian tuned to virial equilibrium (approx).
    NOTE: This is a quick initializer for visualization/calibration, not a high-fidelity DF sampler.
    """
    try:
        import cupy as xp
        rng = xp.random.RandomState(seed)
    except Exception:
        import numpy as xp
        rng = xp.random.RandomState(seed)
    m = xp.full((N,), Mtot/N, dtype=float)

    # Positions (Plummer): r = a * u^(1/3) / sqrt(1 - u^(2/3)), with u in (0,1)
    u = rng.uniform(0.0, 1.0, size=N)
    r = a * (u**(1.0/3.0)) / xp.sqrt(1.0 - u**(2.0/3.0) + 1e-12)

    # Random directions
    phi = 2.0*xp.pi*rng.uniform(size=N)
    cost = rng.uniform(-1.0, 1.0, size=N)
    sint = xp.sqrt(1.0 - cost*cost)
    x = xp.stack([r*sint*xp.cos(phi), r*sint*xp.sin(phi), r*cost], axis=1)

    # Velocities: isotropic Gaussian; sigma tuned so that <v^2> ~ GM/(6a)
    G = 6.67430e-11
    sigma2 = G*Mtot/(6.0*a + 1e-12)
    v = rng.normal(0.0, xp.sqrt(sigma2), size=(N,3))

    # Remove any net drift
    Rcm, Vcm = barycenter(x, v, m)
    x = x - Rcm
    v = v - Vcm
    return x, v, m
