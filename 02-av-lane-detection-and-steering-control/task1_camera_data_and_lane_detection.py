import cv2
import numpy as np

def detect_lane_lines(image):
    """
    Processes an input road image to detect lane lines using 
    grayscale conversion, Gaussian blur, Canny edge detection, 
    a Region of Interest (ROI) mask, and Hough Line Transform.
    """
    # 1. Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 2. Gaussian Blur to reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Canny Edge Detection
    edges = cv2.Canny(blur, 50, 150)
    
    # 4. Define Region of Interest (ROI) - trapezoid covering lower half of image
    height, width = edges.shape
    roi_vertices = np.array([[
        (int(width * 0.1), height),
        (int(width * 0.45), int(height * 0.6)),
        (int(width * 0.55), int(height * 0.6)),
        (int(width * 0.9), height)
    ]], dtype=np.int32)
    
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, roi_vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    # 5. Probabilistic Hough Line Transform
    lines = cv2.HoughLinesP(
        masked_edges,
        rho=1,             # Distance resolution in pixels
        theta=np.pi / 180, # Angle resolution in radians
        threshold=20,      # Minimum number of intersections
        minLineLength=20,  # Minimum line length to detect
        maxLineGap=100     # Maximum gap between line segments
    )
    
    return lines, masked_edges

# Example Usage:
if __name__ == "__main__":
    # Load an image or video frame
    img = cv2.imread("road_test.jpg")
    
    if img is not None:
        lines, masked_edges = detect_lane_lines(img)
        
        # Visualize detected line segments
        output = img.copy()
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
        cv2.imshow("Detected Lines", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
