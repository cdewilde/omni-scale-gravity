import numpy as np

def mu_simple(y):
    # y >= 0
    return y / (1.0 + y + 1e-30)

def mu_soft(y):
    return y / np.sqrt(1.0 + y*y)

def solve_nl_poisson(rho, dx, G=6.67430e-11, a0=1.2e-10,
                     mu=mu_soft, phi0=None, n_iter=2000, omega=0.8, tol=1e-8):
    """
    Solve div[ mu(|grad phi|/a0) * grad phi ] = 4 pi G rho
    on a uniform 2-D grid using Picard iterations + under-relaxation (omega).
    Inputs:
      rho  : mass density [kg/m^3], shape (Ny, Nx)
      dx   : grid spacing [m] (assume dx=dy)
      a0   : acceleration scale [m/s^2]
      mu   : function y -> mu(y)
    Returns:
      phi  : potential [m^2/s^2], same shape as rho
    """
    Ny, Nx = rho.shape
    phi = np.zeros_like(rho) if phi0 is None else phi0.copy()
    rhs = 4.0*np.pi*G*rho

    def grad(phi):
        dphix = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) / (2*dx)
        dphiy = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) / (2*dx)
        return dphix, dphiy

    def divergence(Ax, Ay):
        divx = (np.roll(Ax, -1, 1) - np.roll(Ax, 1, 1)) / (2*dx)
        divy = (np.roll(Ay, -1, 0) - np.roll(Ay, 1, 0)) / (2*dx)
        return divx + divy

    for k in range(n_iter):
        gx, gy = grad(phi)
        g = np.sqrt(gx*gx + gy*gy) + 1e-30
        mu_loc = mu(g / a0)

        # linearized update: solve approx Laplacian( phi_new ) = div( mu * grad phi_old ) + rhs
        Ax = mu_loc * gx
        Ay = mu_loc * gy
        target = rhs - divergence(Ax, Ay)

        # one Jacobi step for Laplacian(phi_new) = target
        phi_new = (np.roll(phi,1,0)+np.roll(phi,-1,0)+np.roll(phi,1,1)+np.roll(phi,-1,1) - (dx*dx)*target)/4.0

        # Dirichlet boundary (phi=0) — modify as needed
        phi_new[0,:]=phi_new[-1,:]=phi_new[:,0]=phi_new[:,-1]=0.0

        # under-relax
        phi = (1-omega)*phi + omega*phi_new

        # convergence
        res = np.max(np.abs(phi_new - phi))
        if res < tol:
            break
    return phi

# Example usage:
# rho_map = ...  # kg/m^3 on a 2-D grid
# phi = solve_nl_poisson(rho_map, dx=100*3.086e16, a0=1.2e-10)  # dx=100 pc
# Then compute rotation curve or lensing from phi.
