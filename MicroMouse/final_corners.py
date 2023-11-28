import cv2
import numpy as np
import math

img = cv2.imread('walls_with_edges_corners_in_white.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Harris corner detection

corners = cv2.goodFeaturesToTrack(gray_img, maxCorners=10, qualityLevel=0.1, minDistance=200, useHarrisDetector=True, k= 0.05)
corners = np.int0(corners)
count = 0
corners_coords = []
for c in corners:
       corners_coords.append(c)
       count += 1
       x, y = c.ravel()
       cv2.circle(img, center=(x, y), radius=4, color=(0, 255, 0), thickness=-1, )

     
# cv2.namedWindow("Maze with Corners", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Maze with Corners", 800, 600)
# cv2.imshow('Maze with Corners', img)

# cv2.waitKey(0)
# print(count)
# print(corners)



def dist(p1, p2):
    x1, x2, y1, y2 = *p1, *p2
    d = ((x2 - x1) ** 2) + ((y2 - y1) ** 2)
    d = math.sqrt(d)
    return d
        
       
       
def orentation(p1, p2, p3):
    x1, y1, x2, y2, x3, y3 = *p1, *p2, *p3
    a = (y3 - y2) * (x2 - x1) - (y2 - y1) * (x3 - x2)
    # if a > 120:
        # return -1
    if a > 80:
        return 1
    return -1
       
       

def gift_wrapping(points):
    # Convert the points to a list of NumPy arrays
    points = [point[0] for point in points]

    # Find the point with the minimum x-coordinate
    on_hull = min(points, key=lambda p: p[0])

    hull = []
    while True:
        hull.append(on_hull)
        next_point = points[0]
        for point in points:
            o = orentation(on_hull, next_point, point)
            dist_comparison = (dist(on_hull, point) > dist(on_hull, next_point))
            if (next_point == on_hull).all() or o == 1 or (o == 0 and dist_comparison):
                next_point = point
        on_hull = next_point
        if np.array_equal(on_hull, hull[0]):
            break
        
    
    return hull



convex_hull = gift_wrapping(corners_coords)

img = cv2.imread('reconstructed_walls.jpg')
count = 0
final_coords= []
for i in convex_hull:
       count += 1
       x, y = i.ravel()
       final_coords.append([x, y])
       cv2.circle(img, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)

cv2.imshow('Maze with Corners', img)
# # 
cv2.waitKey(0)
# print(count)
# print(final_coords)

# cv2.imwrite('final_4_corners.jpg', img)