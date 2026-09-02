import numpy as np

class VehicleModel:
    """
    Simple kinematic bicycle model representing vehicle dynamics.
    State: [x, y, yaw]
    Control input: steering_angle (delta)
    """
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=10.0, wheel_base=2.5):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v  # Constant forward velocity (m/s)
        self.L = wheel_base

    def update(self, delta, dt):
        # Kinematic equations of motion
        self.x += self.v * np.cos(self.yaw) * dt
        self.y += self.v * np.sin(self.yaw) * dt
        self.yaw += (self.v / self.L) * np.tan(delta) * dt
        return self.x, self.y, self.yaw


class PIDController:
    """
    PID Steering Controller.
    Computes steering angle: delta = - (Kp * e_y + Ki * integral(e_y) + Kd * de_y/dt)
    """
    def __init__(self, Kp, Ki, Kd, max_steer_angle=np.radians(30)):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.max_steer_angle = max_steer_angle
        
        self.integral = 0.0
        self.prev_error = 0.0

    def compute_steering(self, e_y, dt):
        # Accumulate integral error
        self.integral += e_y * dt
        
        # Calculate derivative error
        derivative = (e_y - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = e_y
        
        # Calculate control signal
        raw_delta = - (self.Kp * e_y + self.Ki * self.integral + self.Kd * derivative)
        
        # Saturate output to physical steering limits
        delta = np.clip(raw_delta, -self.max_steer_angle, self.max_steer_angle)
        return delta


def simulate_controller(controller, initial_offset=1.0, total_time=10.0, dt=0.05):
    """
    Simulates lateral control loop over time and measures performance metrics.
    """
    vehicle = VehicleModel(x=0.0, y=initial_offset, yaw=0.0, v=10.0)
    
    time_steps = np.arange(0, total_time, dt)
    lateral_errors = []
    steering_angles = []
    
    for t in time_steps:
        # Lateral error e_y (distance from reference trajectory y=0)
        e_y = vehicle.y
        lateral_errors.append(e_y)
        
        # Compute control input
        delta = controller.compute_steering(e_y, dt)
        steering_angles.append(delta)
        
        # Update vehicle position
        vehicle.update(delta, dt)
        
    # Analyze Performance Metrics
    lateral_errors = np.array(lateral_errors)
    max_overshoot = np.max(np.abs(lateral_errors)) if np.any(np.sign(lateral_errors) != np.sign(initial_offset)) else 0.0
    
    # Settling time: time taken to permanently stay within 2% of target threshold
    settle_threshold = 0.02 * abs(initial_offset)
    settled_indices = np.where(np.abs(lateral_errors) <= settle_threshold)[0]
    
    settling_time = None
    for idx in settled_indices:
        if np.all(np.abs(lateral_errors[idx:]) <= settle_threshold):
            settling_time = time_steps[idx]
            break
            
    return {
        "time": time_steps,
        "errors": lateral_errors,
        "steering": steering_angles,
        "max_overshoot": max_overshoot,
        "settling_time": settling_time
    }

# Example Usage & Benchmark comparison:
if __name__ == "__main__":
    # 1. Proportional Control Only
    p_controller = PIDController(Kp=0.5, Ki=0.0, Kd=0.0)
    p_res = simulate_controller(p_controller, initial_offset=1.0)
    
    # 2. PID Control
    pid_controller = PIDController(Kp=0.5, Ki=0.01, Kd=0.25)
    pid_res = simulate_controller(pid_controller, initial_offset=1.0)

    print("Proportional-Only Settling Time:", p_res["settling_time"])
    print("PID Settling Time:", pid_res["settling_time"])
  
