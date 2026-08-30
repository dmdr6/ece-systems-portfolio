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
    t_eval = np.linspace(t_start, t_end, 100)

    # ===============================================================
    # 1. Analytical Closed-Form Solution via Matrix Exponential
    # x(t) = e^(At) * x0
    # ===============================================================
    x_analytical = np.zeros((len(t_eval), len(x0)))

    for i, t in enumerate(t_eval):
        e_At = expm(A * t)
        x_analytical[i] = e_At @ x0

    # ===============================================================
    # 2. Numerical Integration via scipy.integrate.solve_ivp
    # Solves dx/dt = Ax(t) step-by-step
    # ===============================================================
    sol = solve_ivp(
        fun=system_dynamics,
        t_span=t_span,
        y0=x0,
        t_eval=t_eval,
        args=(A,),
        method='RK45',
        rtol=1e-8,
        atol=1e-10
    )
    x_numerical = sol.y.T    # Shape: (N_samples, N_states)

    # ===============================================================
    # 3. Automated Proof Verification (Assertion Check)
    # ===============================================================
    # Compare position and velocity across all time steps
    max_error = np.max(np.abs(x_analytical - x_numerical))

    print("=" * 65)
    print("STATE-SPACE MATRIX EXPONENTIAL PROOF VERIFICATION")
    print("=" * 65)
    print(f"Initial State x0:            Position = {x0[0]} m, Velocity = {x0[1]} m/s")
    print(f"Simulation Window:           t = {t_start}s to t = {t_end}s")
    print(f"Maximum Absolute Error:      {max_error:.2e}")

    # Assert equivalence within numerical precision
    np.testing.assert_allclose(x_analytical, x_numerical, rtol=1e-5, atol=1e-8)

    print("-" * 65)
    print("SUCCESS: Analytical x(t) = e^(At)*x0 matches numerical ODE solver!")
    print("-" * 65)

if __name__ == "__main__":
    main()
