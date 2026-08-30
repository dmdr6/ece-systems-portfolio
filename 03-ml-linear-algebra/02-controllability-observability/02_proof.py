import numpy as np
from scipy.linalg import expm
from scipy.integrate import solve_ivp


def build_controllability_matrix(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Constructs the Controllability Matrix C = [B  AB  A^2B ... A^{n-1}B]."""
    n = A.shape[0]
    blocks = [np.linalg.matrix_power(A, i) @ B for i in range(n)]
    return np.hstack(blocks)


def build_observability_matrix(A: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Constructs the Observability Matrix O = [C; CA; CA^2; ...; CA^{n-1}]."""
    n = A.shape[0]
    blocks = [C @ np.linalg.matrix_power(A, i) for i in range(n)]
    return np.vstack(blocks)


def verify_system_properties():
    # ==================================================================
    # 1. System Setup (2D Mass-Spring-Damper / Kinematic System)
    # ==================================================================
    # States: x = [position, velocity]^T
    # System dimensions: n = 2 states, m = 1 input, p = 1 output
    n = 2
    A = np.array([[0.0, 1.0], [-2.0, -3.0]])
    B = np.array([[0.0], [1.0]])
    C = np.array([[1.0, 0.0]])

    print("=== Continuous LTI System Matrices ===")
    print(f"A Matrix:\n{A}\n")
    print(f"B Matrix:\n{B}\n")
    print(f"C Matrix:\n{C}\n")

    # ==================================================================
    # 2. Algebraic Rank Condition Verification
    # ==================================================================
    C_mat = build_controllability_matrix(A, B)
    O_mat = build_observability_matrix(A, C)

    rank_C = np.linalg.matrix_rank(C_mat)
    rank_O = np.linalg.matrix_rank(O_mat)

    print("=== Rank Conditions Check ===")
    print(f"Controllability Matrix C:\n{C_mat}")
    print(f"Rank of C: {rank_C} / {n} -> Controllable: {rank_C == n}\n")

    print(f"Observability Matrix O:\n{O_mat}")
    print(f"Rank of O: {rank_O} / {n} -> Observable: {rank_O == n}\n")

    # ==================================================================
    # 3. Reachability Numerical Validation (Controllability Gramian)
    # ==================================================================
    # Numerical integration to verify that arbitrary states x_f are reachable via Gramian
    tf = 2.0
    # Controllability Gramian W_c(0, tf) = integral_0^tf (e^{A tau} B B^T e^{A^T tau}) dtau
    def gramian_integrand(t):
        e_At = expm(A * t)
        return e_At @ B @ B.T @ e_At.T

    # Simpson's rule numerical integration for the Gramian
    steps = 1000
    t_vals = np.linspace(0, tf, steps)
    dt = tf / (steps - 1)
    W_c = sum(gramian_integrand(t) * dt for t in t_vals)

    # Solve for optimal control input energy to reach target state x_f from x0 = 0
    x_target = np.array([[1.5], [-0.5]])
    # Control signal trajectory u(t) = B^T e^{A^T (tf - t)} W_c^{-1} x_target
    W_c_inv = np.linalg.inv(W_c)

    def dynamics(t, x):
        e_term = expm(A.T * (tf - t))
        u = B.T @ e_term @ W_c_inv @ x_target
        return (A @ x.reshape(-1, 1) + B @ u).flatten()

    sol = solve_ivp(dynamics, [0, tf], [0.0, 0.0], t_eval=[tf])
    x_achieved = sol.y[:, -1].reshape(-1, 1)

    print("=== Controllability Dynamic Simulation ===")
    print(f"Target State x_f:\n{x_target.ravel()}")
    print(f"Achieved State via Dynamic Control:\n{x_achieved.ravel()}")
    print(
        f"Reaching Error Norm: {np.linalg.norm(x_target - x_achieved):.6e}\n"
    )

    # ==================================================================
    # 4. Observability Numerical Validation (Initial State Recovery)
    # ==================================================================
    # Recover x_0 from output derivatives [y(0); y'(0)] = O * x_0
    x0_true = np.array([[2.5], [-1.2]])

    # Measure initial output and its analytical derivative at t=0
    y0 = C @ x0_true
    dy0 = C @ A @ x0_true
    Y_derivatives = np.vstack([y0, dy0])

    # Reconstruct x0 via matrix inversion of full-rank Observability Matrix
    x0_reconstructed = np.linalg.inv(O_mat) @ Y_derivatives

    print("=== Observability State Reconstruction ===")
    print(f"True Initial State x(0):\n{x0_true.ravel()}")
    print(f"Reconstructed Initial State xhat(0):\n{x0_reconstructed.ravel()}")
    print(
        f"Reconstruction Error Norm: {np.linalg.norm(x0_true - x0_reconstructed):.6e}"
    )


if __name__ == "__main__":
    verify_system_properties()
