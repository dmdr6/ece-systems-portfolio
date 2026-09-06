import numpy as np
import matplotlib.pyplot as plt

# 1. Define true sensor parameters and configuration
TRUE_A = 0.05        # Sensor sensitivity (V/°C)
TRUE_B = 0.50        # Sensor offset (V)
NOISE_STD = 0.15     # Standard deviation of measurement noise (V)
N_SAMPLES = 100      # Number of measurements
SEED = 42            # Random seed for reproducibility

# Set seed for reproducible synthetic datsa
np.random.seed(SEED)

# 2. Generate clean temperature range: T in [0, 100] °C
temperature = np.linspace(0, 100, N_SAMPLES)

# 3. Generate zero-mean Gaussian noise: epsilon ~ N(0, noise_std^2)
noise = np.random.normal(loc=0.0, scale=NOISE_STD, size=N_SAMPLES)

# 4. Compute noisy voltage measurements: V = a*T + b + epsilon
voltage = TRUE_A * temperature + TRUE_B + noise

# 5. Document true parameters
print("=== Task 1: Synthetic Sensor Setup ===")
print(f"True Sensitivity (a) : {TRUE_A:.4f} V/°C")
print(f"True Offset (b)      : {TRUE_B:.4f} V")
print(f"Noise Std Dev (sigma): {NOISE_STD:.4f} V")
print(f"Sample Count (N)     : {N_SAMPLES}")

# 6. Generate Temperature vs. Measured Voltage Scatter Plot
plt.figure(figsize=(8, 5))
plt.scatter(temperature, voltage, color='tab:blue', alpha=0.7, edgecolors='k', label='Measured Voltage (V)')
plt.plot(temperature, TRUE_A * temperature + TRUE_B, color='tab:red', linestyle='--', linewidth=2, label='True Linear Response')

plt.title('Sensor Calibration: Temperature vs. Voltage', fontsize=12)
plt.xlabel('True Temperature T (°C)', fontsize=10)
plt.ylabel('Measured Voltage V (V)', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

# Display plot
plt.tight_layout()
plt.show()
