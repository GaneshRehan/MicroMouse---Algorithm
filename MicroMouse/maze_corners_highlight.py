from convex_hull import convex_hull
import cv2
import numpy as np
import math 

# Load your image
image = cv2.imread('reconstructed_walls.jpg')  # Replace 'your_image.jpg' with your image path

# Your list of coordinates
coordinates = convex_hull

# Convert the list of coordinates to a NumPy array
points = np.array(coordinates)

# Fit the quadrilateral (4-sided polygon) around the points
if len(points) == 4:
    # If there are exactly 4 points, assume they form a quadrilateral
    quad = points
else:
    # If there are more than 4 points, you can use some method to find the 4 corners of the quadrilateral
    # For example, you can use the convex hull to find the outermost points and fit a quadrilateral around them
    hull = cv2.convexHull(points, returnPoints=False)
    indices = hull.squeeze()
    quad = points[indices]

# Draw the quadrilateral in white on the image
# cv2.polylines(image, [quad], isClosed=True, color=(255, 255, 255), thickness=2)  # Draw the quadrilateral in white

# Display the image with the quadrilateral
# cv2.imshow('Image with Quadrilateral', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

i = 0
while i < len(quad) - 1:
    x1, y1 = quad[i]
    x2, y2 = quad[i + 1]
    d = (x2 - x1) ** 2 + (y2 - y1) ** 2
    d = math.sqrt(d)
    if d <= 80:
        quad = np.delete(quad, i+1, axis=0)
    else:
        i += 1

cv2.polylines(image, [quad], isClosed=True, color=(255, 255, 255), thickness=2)  # Draw the quadrilateral in white
print(len(quad))

# Display the image with the quadrilateral
cv2.imshow('Image with Quadrilateral', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite('walls_with_edges_corners_in_white.jpg', image)



