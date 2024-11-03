import cv2
import numpy as np

img = cv2.imread('reconstructed_walls.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Harris corner detection

corners = cv2.goodFeaturesToTrack(gray_img, maxCorners=500, qualityLevel=0.001, minDistance=1, useHarrisDetector=True, k= 0.1)
corners = np.int0(corners)
count = 0
corners_coords = []
for c in corners:
       corners_coords.append(c)
       count += 1
       x, y = c.ravel()
       cv2.circle(img, center=(x, y), radius=2, color=(0, 255, 0), thickness=-1, )

     

for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), radius=2, color=(0, 255, 0), thickness=-1)

# Save the image with marked corners
cv2.imwrite('walls_with_corners_harris_initial_pass.jpg', img)
# cv2.namedWindow("Maze with Corners", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Maze with Corners", 800, 600)
# cv2.imshow('Maze with Corners', img)

# cv2.waitKey(0)
# print(count)
# print(corners)