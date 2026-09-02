import numpy as np
import matplotlib.pyplot as plt

class DynamicRoadScenario:
    """
    Generates dynamic ground truth road profiles (straight/curved)
    and simulates camera/lane detection noise.
    """
    def __init__(self, scenario_type="curved"):
        self.scenario_type = scenario_type

    def get_lane_center(self, x_pos):
        if self.scenario_type == "straight":
            return 0.0
        elif self.scenario_type == "curved":
            # Curved road modeled as a sine wave drift
            return 1.5 * np.sin(0.05 * x_pos)

    def measure_lateral_offset(self, vehicle_x, vehicle_y, noise_std=0.05):
        true_center = self.get_lane_center(vehicle_x)
        true_error = vehicle_y - true_center
        # Inject Gaussian noise simulating visual detection jitter
        visual_noise = np.random.normal(0, noise_std)
        return true_error + visual_noise


def benchmark_pipeline(controller_type="PID", speed=15.0, initial_offset=1.2, noise_level=0.08, road_type="curved"):
    """
    Simulates and measures controller performance across different speeds,
    initial offsets, and detection noise levels.
    """
    dt = 0.05
    total_time = 15.0
    time_steps = np.arange(0, total_time, dt)
    
    # Initialize components
    scenario = DynamicRoadScenario(scenario_type=road_type)
    
    # Simple Vehicle Model
    v_x, v_y, yaw = 0.0, initial_offset, 0.0
    L = 2.5  # wheelbase (m)
    
    # Controller Initialization
    if controller_type == "P":
        Kp, Ki, Kd = 0.4, 0.0, 0.0
    else:  # PID
        Kp, Ki, Kd = 0.5, 0.02, 0.2
        
    integral = 0.0
    prev_error = 0.0
    max_steer = np.radians(30)
    
    # Storage arrays for benchmarking metrics
    errors = []
    steer_cmds = []
    
    for t in time_steps:
        # 1. Vision Geometry Step (Simulated offset with lane noise)
        e_y_measured = scenario.measure_lateral_offset(v_x, v_y, noise_std=noise_level)
        errors.append(v_y - scenario.get_lane_center(v_x))  # Record TRUE error
        
        # 2. Control Step
        integral += e_y_measured * dt
        derivative = (e_y_measured - prev_error) / dt
        prev_error = e_y_measured
        
        delta = - (Kp * e_y_measured + Ki * integral + Kd * derivative)
        delta = np.clip(delta, -max_steer, max_steer)
        steer_cmds.append(delta)
        
        # 3. Vehicle Kinematic Step
        v_x += speed * np.cos(yaw) * dt
        v_y += speed * np.sin(yaw) * dt
        yaw += (speed / L) * np.tan(delta) * dt

    # 4. Compute Benchmark Metrics
    true_errors = np.array(errors)
    steer_cmds = np.array(steer_cmds)
    
    mae_tracking_error = np.mean(np.abs(true_errors))
    
    # Overshoot calculation
    peak_err = np.max(np.abs(true_errors))
    overshoot = max(0.0, peak_err - abs(initial_offset))
    
    # Settling time (2% of initial offset threshold)
    threshold = 0.05
    settled_indices = np.where(np.abs(true_errors) <= threshold)[0]
    settling_time = None
    for idx in settled_indices:
        if np.all(np.abs(true_errors[idx:]) <= threshold):
            settling_time = time_steps[idx]
            break
            
    # Steering Smoothness (Mean Squared Steering Derivative / Roughness)
    steer_rate = np.diff(steer_cmds) / dt
    steering_smoothness = np.mean(steer_rate ** 2)

    return {
        "time": time_steps,
        "true_errors": true_errors,
        "steering": steer_cmds,
        "mae_error": mae_tracking_error,
        "settling_time": settling_time,
        "overshoot": overshoot,
        "smoothness": steering_smoothness
    }


# Run Benchmark Suite
if __name__ == "__main__":
    results_p = benchmark_pipeline(controller_type="P", speed=15.0, noise_level=0.05, road_type="curved")
    results_pid = benchmark_pipeline(controller_type="PID", speed=15.0, noise_level=0.05, road_type="curved")

    print(f"--- Benchmark Results (Curved Road with Visual Noise) ---")
    print(f"P-Controller   | MAE Error: {results_p['mae_error']:.3f}m | Settling Time: {results_p['settling_time']}s | Smoothness: {results_p['smoothness']:.4f}")
    print(f"PID-Controller | MAE Error: {results_pid['mae_error']:.3f}m | Settling Time: {results_pid['settling_time']}s | Smoothness: {results_pid['smoothness']:.4f}")
