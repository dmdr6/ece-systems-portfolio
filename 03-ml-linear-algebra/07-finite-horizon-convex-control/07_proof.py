import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt
from typing import Tuple, List

def simulate_system() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[np.ndarray], List[np.ndarray], List[np.ndarray], List[float]]:
    """Simulates a constrained double-integrator system using MPC vs Unconstrained LQR baseline."""
    # System dynamics: Double Integrator (e.g., cart position and velocity)
    dt = 0.1
    A = np.array([[1.0, dt], 
                  [0.0, 1.0]])
    B = np.array([[0.5 * dt**2], 
                  [dt]])
    
    n_states = A.shape[0]
    n_controls = B.shape[1]
    
    # Cost matrices
    Q = np.diag([10.0, 1.0])
    R = np.array([[0.1]])
    P = Q # Terminal cost
    
    # Constraints
    u_min = -1.5
    u_max = 1.5
    
    # Simulation parameters
    sim_steps = 40
    horizon = 10
    
    x_init = np.array([5.0, -2.0]) # Initial position and velocity
    
    # MPC Storage
    x_mpc = [x_init.copy()]
    u_mpc = []
    costs_mpc = []
    
    # Baseline (Unconstrained LQR / Open-loop optimal) Storage
    x_base = [x_init.copy()]
    u_base = []
    
    # CVXPY Optimization Problem Setup for MPC
    x_var = cp.Variable((n_states, horizon + 1))
    u_var = cp.Variable((n_controls, horizon))
    init_state = cp.Parameter(n_states)
    
    cost = 0
    constraints = [x_var[:, 0] == init_state]
    
    for k in range(horizon):
        cost += cp.quad_form(x_var[:, k], Q) + cp.quad_form(u_var[:, k], R)
        constraints += [
            x_var[:, k+1] == A @ x_var[:, k] + B @ u_var[:, k],
            u_var[:, k] >= u_min,
            u_var[:, k] <= u_max
        ]
    cost += cp.quad_form(x_var[:, horizon], P)
    
    prob = cp.Problem(cp.Minimize(cost), constraints)
    
    # --- MPC Simulation Loop ---
    current_x = x_init.copy()
    for t in range(sim_steps):
        init_state.value = current_x
        try:
            prob.solve(solver=cp.OSQP, verbose=False)
        except Exception:
            prob.solve(solver=cp.SCS, verbose=False)
            
        if u_var.value is None:
            break
            
        u_opt = u_var.value[:, 0]
        u_scalar = float(u_opt[0])
        u_mpc.append(u_scalar)
        costs_mpc.append(float(prob.value))
        
        # Apply to plant
        current_x = A @ current_x + B.flatten() * u_scalar
        x_mpc.append(current_x.copy())
        
    # --- Baseline Simulation (Unconstrained LQR via steady-state approximation / proportional feedback) ---
    current_x_base = x_init.copy()
    # Simple gain feedback that ignores saturation for baseline comparison
    K_gain = np.array([-2.5, -1.8])
    for t in range(sim_steps):
        u_b = float(K_gain @ current_x_base)
        u_base.append(u_b)
        current_x_base = A @ current_x_base + B.flatten() * u_b
        x_base.append(current_x_base.copy())
        
    return np.array(x_mpc), np.array(u_mpc), np.array(x_base), np.array(u_base), np.array([u_min, u_max]), sim_steps, dt

def main() -> None:
    print("=" * 75)
    print("PROOF #7 NUMERICAL VERIFICATION: CONSTRAINED MPC TRAJECTORY OPTIMIZATION")
    print("=" * 75)
    
    x_mpc, u_mpc, x_base, u_base, bounds, sim_steps, dt = simulate_system()
    time_steps = np.arange(sim_steps + 1) * dt
    control_times = np.arange(len(u_mpc)) * dt
    
    print(f"Simulation completed across {sim_steps} steps.")
    print(f"Final MPC State: Position = {x_mpc[-1, 0]:.4f}, Velocity = {x_mpc[-1, 1]:.4f}")
    
    # Plotting Results
    plt.figure(figsize=(15, 10))
    
    # Subplot 1: State Trajectories (Position & Velocity)
    plt.subplot(2, 2, 1)
    plt.plot(time_steps, x_mpc[:, 0], 'b-', linewidth=2, label='MPC Position ($x_1$)')
    plt.plot(time_steps, x_mpc[:, 1], 'b--', linewidth=1.5, label='MPC Velocity ($x_2$)')
    plt.plot(time_steps, x_base[:, 0], 'r:', linewidth=1.5, label='Baseline Position')
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.title('State Trajectories: MPC vs Baseline')
    plt.xlabel('Time (s)')
    plt.ylabel('State Values')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Subplot 2: Control Inputs & Actuator Saturation
    plt.subplot(2, 2, 2)
    plt.plot(control_times, u_mpc, 'g-', linewidth=2, label='MPC Control Input ($u$)')
    plt.plot(control_times, u_base[:len(control_times)], 'r:', linewidth=1.5, label='Baseline Unconstrained')
    plt.axhline(bounds[1], color='k', linestyle='--', label='Actuator Limits')
    plt.axhline(bounds[0], color='k', linestyle='--')
    plt.title('Control Inputs & Actuator Saturation')
    plt.xlabel('Time (s)')
    plt.ylabel('Control Force')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Subplot 3: Phase Portrait (Position vs Velocity)
    plt.subplot(2, 2, 3)
    plt.plot(x_mpc[:, 0], x_mpc[:, 1], 'b-o', markersize=4, label='MPC Phase Path')
    plt.plot(x_base[:, 0], x_base[:, 1], 'r:', label='Baseline Phase Path')
    plt.plot(x_mpc[0, 0], x_mpc[0, 1], 'go', markersize=8, label='Start')
    plt.plot(0, 0, 'kx', markersize=8, label='Target Origin')
    plt.title('Phase Portrait ($x_1$ vs $x_2$)')
    plt.xlabel('Position ($x_1$)')
    plt.ylabel('Velocity ($x_2$)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Subplot 4: Optimization Cost Evolution
    plt.subplot(2, 2, 4)
    costs = [np.sum(x_mpc[t, :]**2 * 10) + u_mpc[t]**2 * 0.1 for t in range(len(u_mpc))]
    plt.plot(control_times, costs, 'm-o', markersize=4)
    plt.title('Instantaneous Stage Cost over Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Cost Value')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
    
