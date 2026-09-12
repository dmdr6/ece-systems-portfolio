import numpy as np
import matplotlib.pyplot as plt

# --- Re-generate Task 1 Data ---
TRUE_A, TRUE_B, NOISE_STD, N_SAMPLES, SEED = 0.05, 0.50, 0.15, 100, 42
np.random.seed(SEED)

T = np.linspace(0, 100, N_SAMPLES)
noise = np.random.normal(0.0, NOISE_STD, N_SAMPLES)
V = TRUE_A * T + TRUE_B + noise

# --- Task 2: Closed-Form OLS Implementation ---

# 1. Construct the Design Matrix X: shape (N, 2)
# Column 1 = Temperature T, Column 2 = Bias/Intercept terms (1s)
X = np.vstack([T, np.ones(N_SAMPLES)]).T

# 2. Compute normal equations: theta = (X^T * X)^(-1) * X^T * V
# Using np.linalg.inv for explicit derivation matching:
theta_ols = np.linalg.inv(X.T @ X) @ X.T @ V

a_hat, b_hat = theta_ols[0], theta_ols[1]

# 3. Compute error metrics
a_error = abs(TRUE_A - a_hat)
b_error = abs(TRUE_B - b_hat)

print("=== Task 2: OLS Calibration Results ===")
print(f"True Parameters      : a = {TRUE_A:.6f}, b = {TRUE_B:.6f}")
print(f"Estimated Parameters : â = {a_hat:.6f}, b̂ = {b_hat:.6f}")
print(f"Absolute Errors      : |Δa| = {a_error:.6f}, |Δb| = {b_error:.6f}")

# 4. Plot Calibration Curve vs. Measurements
plt.figure(figsize=(8, 5))
plt.scatter(T, V, color='tab:blue', alpha=0.6, edgecolors='k', label='Measured Voltage (V)')
plt.plot(T, TRUE_A * T + TRUE_B, color='tab:green', linestyle='--', linewidth=2, label='True Line')
plt.plot(T, X @ theta_ols, color='tab:red', linewidth=2, label=f'OLS Fit (â={a_hat:.4f}, b̂={b_hat:.4f})')

plt.title('Task 2: Sensor Calibration via Closed-Form OLS', fontsize=12)
plt.xlabel('Temperature T (°C)', fontsize=10)
plt.ylabel('Voltage V (V)', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
