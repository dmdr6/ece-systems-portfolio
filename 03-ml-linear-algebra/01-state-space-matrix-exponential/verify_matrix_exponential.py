import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp

def system_dynamics(t, x, A):
    """Computes x_dot = A * x for numerical ODE integration."""
    return A @ x

def main():
    # 1. System setup (Double Integrator Model: 1D Position and Velocity)
    A = np.array([
        [0.0, 1.0],
        [0.0, 0.0]
    ])
    x0 = np.array([10.0, 5.0])  # Initial state: p(0) = 10m, v(0) = 5m/s

    t_start = 0.0
    t_end = 10.0
    t_span = (t_start, t_end)
    t_eval = p.linspace(t_start, t_end, 100)

    # -----------------------------------------------------------------
    # PART 1: Analytical Closed-Form Solution via Matrix Exponential
    # x(t) = e^(At) * x0
    # -----------------------------------------------------------------
    x_analytical = np.zeros((len(t_eval), len(x0)))

    for i, t in enumerate(t_eval):
        e_At = expm(A * t)
        x_analytical[i] = e_At @ x0
