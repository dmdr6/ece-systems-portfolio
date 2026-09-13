import numpy as np
import scipy.linalg as la
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def setup_inverted_pendulum():
    # State vector x = [cart position, cart velocity, pole angle, pole angular velocity]
    m = 0.1     # Pendulum mass (kg)
    M = 1.0     # Cart mass (kg)
    L = 0.5     # Pole half-length (m)
    g = 9.81    # Gravity (m/s^2)
    d = 0.1     # Cart friction coefficient

    denominator = M + m

    # Linearized state-space around upright equilibrium (x = 0)
    A = np.array([
        [0, 1, 0, 0],
        [0, -d / M, -(m * g) / M, 0],
        [0, 0, 0, 1],
        [0, d / (M * L), (M + m) * g / (M * L), 0]
    ])

    B = np.array([
        [0],
        [1 / M],
        [0],
        [-1 / (M * L)]
    ])

    # Weight matrices Q (state penalty) and R (control effort penalty)
    Q = np.diag([10.0, 1.0, 100.0, 10.0])
    R = np.array([[0.1]])

    return A, B, Q, R

def compute_lqr(A, B, Q, R):
    # Solve Continuous Algebraic Riccati Equation (CARE)
    P = la.solve_continuous_are(A, B, Q, R)

    # Compute optimal feedback gain matrix K
    R_inv = la.inv(R)
    K = R_inv @ B.T @ P

    return P, K

def simulate_dynamics(A, B, K, x0, t_span, t_eval):
    # Closed-loop dynamics: dx/dt = (A - B*K)*x
    A_cl = A - B @ K

    def closed_loop_ode(t, x):
        return A_cl @ x

    # Baseline uncontrolled / naive feedback dynamics for comparison
    def open_loop_ode(t, x):
        return A @ x

    res_cl = solve_ivp(closed_loop_ode, t_span, x0, t_eval=t_eval, rtol=1e-8, atol=1e-10)
    res_ol = solve_ivp(open_loop_ode, t_span, x0, t_eval=t_eval, rtol=1e-8, atol=1e-10)

    return res_cl, res_ol

def compute_cost_and_control(res, K, Q, R):
    t_vals = res.t
    X = res.y
    N = len(t_vals)

    u_vals = np.zeros((1, N))
    J_cumulative = np.zeros(N)

    running_cost = 0.0
    for i in range(N):
        x_i = X[:, i:i+1]
        u_i = -K @ x_i
        u_vals[:, i] = u_i.flatten()

        state_cost = (x_i.T @ Q @ x_i)[0, 0]
        control_cost = (u_i.T @ R @ u_i)[0, 0]
        stage_cost = state_cost + control_cost

        if i > 0:
            dt = t_vals[i] - t_vals[i-1]
            running_cost += stage_cost * dt

        J_cumulative[i] = running_cost

    return u_vals, J_cumulative

def main():
    A, B, Q, R = setup_inverted_pendulum()
    P, K = compute_lqr(A, B, Q, R)

    # Calculate eigenvalues
    open_loop_eigs = la.eigvals(A)
    closed_loop_eigs = la.eigvals(A - B @ K)

    print("======================================================")
    print(" LQR Optimality & CARE Verification (Proof #4) ")
    print("======================================================")
    print("\nAlgebraic Riccati Matrix P:")
    print(np.array2string(P, precision=4, suppress_small=True))
    print("\nOptimal Control Feedback Gain K:")
    print(np.array2string(K, precision=4, suppress_small=True))

    # Verify CARE Residual
    care_residual = A.T @ P + P @ A - P @ B @ la.inv(R) @ B.T @ P + Q
    print("\nCARE Residual Norm ||A^T P + P A - P B R^-1 B^T P + Q||:")
    print(f"{la.norm(care_residual):.2e}")

    print("\nOpen-Loop System Eigenvalues:")
    for ep in open_loop_eigs:
        print(f"  {ep.real:+.4f} + {ep.imag:+.4f}j")

    print("\nClosed-Loop System Eigenvalues (A - BK):")
    is_hurwitz = True
    for ep in closed_loop_eigs:
        print(f"  {ep.real:+.4f} + {ep.imag:+.4f}j")
        if ep.real >= 0:
            is_hurwitz = False

    print(f"\nHurwitz Stability Verified: {is_hurwitz}")

    # Simulation setup
    x0 = np.array([0.2, 0.0, 0.15, 0.0])  # Initial displacement: 20cm cart position, ~8.6 deg pole angle
    t_span = (0.0, 8.0)
    t_eval = np.linspace(t_span[0], t_span[1], 1000)

    res_cl, res_ol = simulate_dynamics(A, B, K, x0, t_span, t_eval)
    u_cl, J_cl = compute_cost_and_control(res_cl, K, Q, R)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

    # Subplot 1: State Trajectories
    axs[0].plot(res_cl.t, res_cl.y[0], label="Cart Position $x$ (m)", color="crimson", linewidth=2)
    axs[0].plot(res_cl.t, res_cl.y[2], label="Pole Angle $\\theta$ (rad)", color="royalblue", linewidth=2)
    axs[0].plot(res_ol.t, res_ol.y[2], "--", label="Uncontrolled $\\theta$ (Divergent)", color="gray", alpha=0.7)
    axs[0].set_ylabel("States")
    axs[0].set_title("LQR Closed-Loop State Regulation vs. Uncontrolled Response")
    axs[0].grid(True, linestyle=":", alpha=0.6)
    axs[0].legend(loc="upper right")
    axs[0].set_ylim([-0.5, 0.5])

    # Subplot 2: Optimal Control Input
    axs[1].plot(res_cl.t, u_cl[0], label="Control Input $u^*(t)$ (N)", color="darkgreen", linewidth=2)
    axs[1].set_ylabel("Force (N)")
    axs[1].set_title("Optimal Control Effort")
    axs[1].grid(True, linestyle=":", alpha=0.6)
    axs[1].legend(loc="upper right")

    # Subplot 3: Cumulative Quadratic Cost
    axs[3 - 1].plot(res_cl.t, J_cl, label="Cumulative Cost $J(t)$", color="purple", linewidth=2)
    axs[3 - 1].axhline(y=(x0.T @ P @ x0), color="black", linestyle="--", label="Theoretical $x_0^T P x_0$")
    axs[3 - 1].set_xlabel("Time (s)")
    axs[3 - 1].set_ylabel("Cost $J$")
    axs[3 - 1].set_title("Convergence of Performance Index J(t) to Theoretical Minimum $x_0^T P x_0$")
    axs[3 - 1].grid(True, linestyle=":", alpha=0.6)
    axs[3 - 1].legend(loc="lower right")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
