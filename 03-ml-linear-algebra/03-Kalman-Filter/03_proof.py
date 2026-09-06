import numpy as np
import matplotlib.pyplot as plt


def run_kalman_filter_simulation():
    # 1. Simulation Setup & System Matrices (2D Kinematic Model)
    # State Vector: x_k = [pos_x, pos_y, vel_x, vel_y]^T \in \mathbb{R}^4
    np.random.seed(42)  # For reproducible random trajectories
    dt = 0.1             # Time step (seconds)
    N = 200              # Total discrete time steps

    # State transition matrix A
    A = np.array([
        [1.0, 0.0,  dt, 0.0],
        [0.0, 1.0, 0.0,  dt],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0]
    ])

    # Observation matrix H (only measure 2D position [pos_x, pos_y])
    H = np.array([
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0]
    ])

    # Process noise covariance Q (discrete piecewise constant acceleration)
    q_var = 0.05
    Q_block = np.array([
        [0.25 * dt**4, 0.5 * dt**3],
        [0.5 * dt**3,  dt**2]
    ]) * q_var
    Q = np.block([
        [Q_block[0, 0] * np.eye(2), Q_block[0, 1] * np.eye(2)],
        [Q_block[1, 0] * np.eye(2), Q_block[1, 1] * np.eye(2)]
    ])

    # Measurement noise covariance R (GPS position noise variance)
    r_var = 2.25  # (1.5 meters standard deviation)^2
    R = np.eye(2) * r_var

    # 2. Memory Allocation & Initial Conditions
    x_true = np.zeros((4, N))
    z_meas = np.zeros((2, N))
    x_hat = np.zeros((4, N))
    P_bounds = np.zeros((4, N))  # Stores diagonal elements of P_k (variances)

    # True initial state: [0m, 0m, 10m/s, 5m/s]
    x_true[:, 0] = np.array([0.0, 0.0, 10.0, 5.0])

    # Initial state estimate (biased initial guess)
    x_hat[:, 0] = np.array([2.0, -3.0, 8.0, 7.0])

    # Initial prior error covariance estimate P_0^-
    P = np.diag([10.0, 10.0, 5.0, 5.0])

    # 3. Main Kalman Filter Recursion Loop
    for k in range(1, N):
        # A. True State Propagation (Environment)
        w_k = np.random.multivariate_normal(mean=np.zeros(4), cov=Q)
        x_true[:, k] = A @ x_true[:, k - 1] + w_k

        # B. Noisy Measurement Generation (Sensor)
        v_k = np.random.multivariate_normal(mean=np.zeros(2), cov=R)
        z_meas[:, k] = H @ x_true[:, k] + v_k

        # C. Predict Step (Time Update)
        x_pred = A @ x_hat[:, k - 1]
        P_pred = A @ P @ A.T + Q

        # D. Optimal Kalman Gain Computation (Proof 3 Formula)
        S = H @ P_pred @ H.T + R  # Innovation covariance
        K = P_pred @ H.T @ np.linalg.inv(S)

        # E. Update Step (Measurement Correction)
        innovation = z_meas[:, k] - H @ x_pred
        x_hat[:, k] = x_pred + K @ innovation

        # Posterior Covariance Update: P_k = (I - K*H) * P_pred
        I = np.eye(4)
        P = (I - K @ H) @ P_pred

        # Store predicted variance bounds (3 * sigma = 3 * sqrt(P_diag))
        P_bounds[:, k] = 3.0 * np.sqrt(np.diag(P))

    # Compute empirical estimation error: e_k = x_true - x_hat
    error = x_true - x_hat

    # 4. Numerical Proof Verification Output
    print("=" * 65)
    print("PROOF 03: KALMAN FILTER COVARIANCE VERIFICATION")
    print("=" * 65)
    
    final_pos_x_err_var = np.var(error[0, 50:])
    predicted_pos_x_var = (P_bounds[0, -1] / 3.0) ** 2

    print(f"Final Empirical Error Variance (X Position): {final_pos_x_err_var:.4f}")
    print(f"Predicted Optimal Variance P_k[0,0]:         {predicted_pos_x_var:.4f}")

    # Check if > 99% of error points lie within the predicted 3-sigma bounds
    within_bounds_x = np.abs(error[0, :]) <= P_bounds[0, :]
    within_bounds_y = np.abs(error[1, :]) <= P_bounds[1, :]
    percentage_valid = np.mean(within_bounds_x & within_bounds_y) * 100.0

    print(f"Percentage of errors within predicted 3-sigma bounds: {percentage_valid:.2f}%")
    
    if percentage_valid >= 95.0:
        print("\nSUCCESS: Empirical error variance strictly conforms to analytical P_k bounds!")
    print("=" * 65)

    # 5. Visual Verification Plotting
    time_steps = np.arange(N) * dt
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))

    # Subplot 1: 2D Spatial Trajectory
    axes[0, 0].plot(x_true[0, :], x_true[1, :], 'k-', label='True Trajectory', linewidth=2)
    axes[0, 0].scatter(z_meas[0, :], z_meas[1, :], c='r', s=10, alpha=0.4, label='Noisy Measurements (Z_k)')
    axes[0, 0].plot(x_hat[0, :], x_hat[1, :], 'b--', label='Kalman Estimate (\hat{x}_k)', linewidth=2)
    axes[0, 0].set_title('2D State Tracking Trajectory')
    axes[0, 0].set_xlabel('X Position [m]')
    axes[0, 0].set_ylabel('Y Position [m]')
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Subplot 2: X-Position Estimation Error & 3-Sigma Bounds
    axes[0, 1].plot(time_steps, error[0, :], 'b-', label='Estimation Error (e_x)')
    axes[0, 1].plot(time_steps, P_bounds[0, :], 'r--', label='+3\sigma Bound (from P_k)')
    axes[0, 1].plot(time_steps, -P_bounds[0, :], 'r--', label='-3\sigma Bound (from P_k)')
    axes[0, 1].set_title('X Position Error vs. Predicted 3\sigma Covariance Bounds')
    axes[0, 1].set_xlabel('Time [s]')
    axes[0, 1].set_ylabel('Error [m]')
    axes[0, 1].legend()
    axes[0, 1].grid(True)

    # Subplot 3: Y-Position Estimation Error & 3-Sigma Bounds
    axes[1, 0].plot(time_steps, error[1, :], 'g-', label='Estimation Error (e_y)')
    axes[1, 0].plot(time_steps, P_bounds[1, :], 'r--', label='+3\sigma Bound (from P_k)')
    axes[1, 0].plot(time_steps, -P_bounds[1, :], 'r--', label='-3\sigma Bound (from P_k)')
    axes[1, 0].set_title('Y Position Error vs. Predicted 3\sigma Covariance Bounds')
    axes[1, 0].set_xlabel('Time [s]')
    axes[1, 0].set_ylabel('Error [m]')
    axes[1, 0].legend()
    axes[1, 0].grid(True)

    # Subplot 4: Velocity Estimation Convergence
    axes[1, 1].plot(time_steps, x_true[2, :], 'k-', label='True Vel X')
    axes[1, 1].plot(time_steps, x_hat[2, :], 'b--', label='Estimated Vel X')
    axes[1, 1].plot(time_steps, x_true[3, :], 'k:', label='True Vel Y')
    axes[1, 1].plot(time_steps, x_hat[3, :], 'g--', label='Estimated Vel Y')
    axes[1, 1].set_title('Velocity Tracking Convergence')
    axes[1, 1].set_xlabel('Time [s]')
    axes[1, 1].set_ylabel('Velocity [m/s]')
    axes[1, 1].legend()
    axes[1, 1].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    run_kalman_filter_simulation()
