import cv2
import numpy as np
from final_corners import final_coords

# Load your image
image = cv2.imread('reconstructed_walls.jpg')

# Define the source points (coordinates in the original image)
source_points = np.array(final_coords, dtype=np.float32)

# Define the destination points (where the source points will be mapped)
# You can adjust these points to define the desired perspective transformation
# Here, we assume a rectangular region for demonstration purposes
width, height = 400, 300  # Define the width and height of the output region
destination_points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32)

# Calculate the perspective transformation matrix
matrix = cv2.getPerspectiveTransform(source_points, destination_points)

# Perform the perspective warp
warped_image = cv2.warpPerspective(image, matrix, (width, height))

# Display the original and warped images
cv2.imshow('Original Image', image)
cv2.imshow('Warped Image', warped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite('final_wrapped_image.jpg', warped_image)
