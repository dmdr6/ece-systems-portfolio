import numpy as np
import cv2

def process_lane_geometry(lines, image_shape):
    """
    Determines left and right lane boundaries, calculates lane center,
    computes vehicle lateral offset (e_y = x_vehicle - x_lane_center),
    and estimates road curvature using a 2nd-degree polynomial fit.
    """
    height, width = image_shape[:2]
    left_fit_x, right_fit_x = [], []
    left_fit_y, right_fit_y = [], []
    
    if lines is None:
        return None
    
    # 1. Separate line segments into Left and Right lanes based on slope
    for line in lines:
        for x1, y1, x2, y2 in line:
            if x1 == x2:
                continue  # Avoid vertical line division by zero
            slope = (y2 - y1) / (x2 - x1)
            
            # Filter by slope threshold to ignore horizontal noise
            if slope < -0.5:  # Left lane (negative slope in image coordinates)
                left_fit_x.extend([x1, x2])
                left_fit_y.extend([y1, y2])
            elif slope > 0.5:  # Right lane (positive slope in image coordinates)
                right_fit_x.extend([x1, x2])
                right_fit_y.extend([y1, y2])

    if not left_fit_x or not right_fit_x:
        return None

    # 2. Fit 2nd-degree polynomials to left and right lane points (x = f(y))
    left_poly = np.polyfit(left_fit_y, left_fit_x, 2)
    right_poly = np.polyfit(right_fit_y, right_fit_x, 2)
    
    # Evaluate at the bottom of the image (y = height)
    y_eval = height
    x_left_base = left_poly[0] * (y_eval ** 2) + left_poly[1] * y_eval + left_poly[2]
    x_right_base = right_poly[0] * (y_eval ** 2) + right_poly[1] * y_eval + right_poly[2]
    
    # 3. Calculate Lane Center & Vehicle Lateral Offset
    x_lane_center = (x_left_base + x_right_base) / 2.0
    x_vehicle = width / 2.0  # Assuming camera is mounted at vehicle center
    
    # e_y = x_vehicle - x_lane_center
    lateral_offset_px = x_vehicle - x_lane_center
    
    # Optional pixel-to-meter scaling (e.g., assuming lane width is ~3.7m wide / ~700px)
    xm_per_pix = 3.7 / abs(x_right_base - x_left_base)
    lateral_offset_m = lateral_offset_px * xm_per_pix
    
    # 4. Estimate Approximate Road Curvature (R = (1 + (2Ay + B)^2)^(3/2) / |2A|)
    # Averaging A and B coefficients of left and right polynomials
    A = (left_poly[0] + right_poly[0]) / 2.0
    B = (left_poly[1] + right_poly[1]) / 2.0
    
    if abs(A) > 1e-6:
        curvature_radius_px = ((1 + (2 * A * y_eval + B) ** 2) ** 1.5) / abs(2 * A)
        curvature_radius_m = curvature_radius_px * xm_per_pix
    else:
        curvature_radius_m = float('inf')  # Straight road
        
    return {
        "x_left_base": x_left_base,
        "x_right_base": x_right_base,
        "x_lane_center": x_lane_center,
        "lateral_offset_px": lateral_offset_px,
        "lateral_offset_m": lateral_offset_m,
        "curvature_radius_m": curvature_radius_m,
        "left_poly": left_poly,
        "right_poly": right_poly
    }
