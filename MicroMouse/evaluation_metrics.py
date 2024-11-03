import numpy as np
import cv2
from sklearn.metrics import mean_squared_error

def evaluate_maze_transformation(input_image, warped_image):
    """
    Evaluates maze transformation quality between original and perspective-wrapped image
    
    Parameters:
    input_image: Original input image (numpy array, BGR format)
    warped_image: Perspective-transformed bird's-eye view image (numpy array, BGR format)
    
    Returns:
    Dictionary containing evaluation metrics
    """
    metrics = {}
    
    # 1. Maze Structure Analysis
    def analyze_maze_structure(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to get binary image
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Calculate corridor width consistency
        horizontal_profile = np.mean(binary, axis=0)
        vertical_profile = np.mean(binary, axis=1)
        
        corridor_width_var_h = np.var(horizontal_profile)
        corridor_width_var_v = np.var(vertical_profile)
        
        return {
            'corridor_consistency_h': corridor_width_var_h,
            'corridor_consistency_v': corridor_width_var_v
        }
    
    # Analyze structure for warped image
    structure_metrics = analyze_maze_structure(warped_image)
    metrics.update(structure_metrics)
    
    # 2. Wall Straightness Analysis (for warped image)
    def analyze_wall_straightness(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect edges
        edges = cv2.Canny(gray, 50, 150)
        
        # Save edges image for visualization
        cv2.imwrite('detected_edges.jpg', edges)
        
        # Detect lines using Hough Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, 
                               minLineLength=100, maxLineGap=10)
        
        # Create a copy of the image to draw detected lines
        line_image = image.copy()
        
        if lines is not None:
            # Calculate angles of detected lines
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                # Draw the detected lines
                cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                angle = np.abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)) % 90)
                angles.append(angle)
            
            # Save the image with detected lines
            cv2.imwrite('detected_lines.jpg', line_image)
            
            # Lines should be either vertical (close to 90°) or horizontal (close to 0°)
            angles = np.array(angles)
            vertical_lines = angles[angles >= 45]
            horizontal_lines = angles[angles < 45]
            
            vert_straightness = np.std(np.abs(vertical_lines - 90))
            horiz_straightness = np.std(horizontal_lines)
            
            return {
                'vertical_straightness': vert_straightness,
                'horizontal_straightness': horiz_straightness,
                'num_lines_detected': len(lines)
            }
        else:
            return {
                'vertical_straightness': float('inf'),
                'horizontal_straightness': float('inf'),
                'num_lines_detected': 0
            }
    
    wall_metrics = analyze_wall_straightness(warped_image)
    metrics.update(wall_metrics)
    
    # 3. Perpendicularity Analysis
    def analyze_perpendicularity(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Get corners using Harris corner detector
        corners = cv2.cornerHarris(gray, blockSize=2, ksize=3, k=0.04)
        
        # Create a copy of the image to mark corners
        corner_image = image.copy()
        corner_image[corners > 0.01 * corners.max()] = [0, 0, 255]  # Mark corners in red
        
        # Save the image with detected corners
        cv2.imwrite('detected_corners.jpg', corner_image)
        
        # Calculate corner density in quadrants
        height, width = image.shape[:2]
        quadrants = [
            corners[:height//2, :width//2],
            corners[:height//2, width//2:],
            corners[height//2:, :width//2],
            corners[height//2:, width//2:]
        ]
        
        corner_densities = [np.sum(quad > 0.01 * quad.max()) for quad in quadrants]
        corner_density_variance = np.var(corner_densities)
        
        return {
            'corner_density_variance': corner_density_variance,
            'total_corners': sum(corner_densities),
            'corner_densities': corner_densities
        }
    
    perp_metrics = analyze_perpendicularity(warped_image)
    metrics.update(perp_metrics)
    
    # 4. Grid Regularity
    def analyze_grid_regularity(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        # Save binary image for visualization
        cv2.imwrite('binary_image.jpg', binary)
        
        # Calculate row and column profiles
        row_profile = np.sum(binary, axis=1)
        col_profile = np.sum(binary, axis=0)
        
        # Calculate regularity scores
        row_regularity = np.std(row_profile) / np.mean(row_profile)
        col_regularity = np.std(col_profile) / np.mean(col_profile)
        
        return {
            'row_regularity': row_regularity,
            'col_regularity': col_regularity
        }
    
    grid_metrics = analyze_grid_regularity(warped_image)
    metrics.update(grid_metrics)
    
    return metrics

def print_evaluation_report(metrics):
    """
    Prints a formatted report of the evaluation metrics
    """
    print("\n=== Maze Transformation Evaluation Report ===\n")
    
    print("Corridor Consistency:")
    print(f"Horizontal Variance: {metrics['corridor_consistency_h']:.2f}")
    print(f"Vertical Variance: {metrics['corridor_consistency_v']:.2f}")
    
    print("\nWall Straightness:")
    print(f"Vertical Lines Deviation: {metrics['vertical_straightness']:.2f}°")
    print(f"Horizontal Lines Deviation: {metrics['horizontal_straightness']:.2f}°")
    print(f"Number of Lines Detected: {metrics['num_lines_detected']}")
    
    print("\nCorner Analysis:")
    print(f"Corner Density Variance: {metrics['corner_density_variance']:.2f}")
    print(f"Total Corners Detected: {metrics['total_corners']}")
    print("Corner Densities by Quadrant:", metrics['corner_densities'])
    
    print("\nGrid Regularity:")
    print(f"Row Regularity Score: {metrics['row_regularity']:.3f}")
    print(f"Column Regularity Score: {metrics['col_regularity']:.3f}")

def main():
    # Load the images
    input_image = cv2.imread('bw_maze_red_walls.png')
    warped_image = cv2.imread('final_wrapped_image.jpg')
    
    if input_image is None:
        raise ValueError("Could not load input image 'bw_maze_red_walls.png'")
    if warped_image is None:
        raise ValueError("Could not load warped image 'final_wrapped_image.jpg'")
    
    # Get metrics
    metrics = evaluate_maze_transformation(input_image, warped_image)
    
    # Print the report
    print_evaluation_report(metrics)

if __name__ == "__main__":
    main()