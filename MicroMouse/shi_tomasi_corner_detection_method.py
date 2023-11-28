import numpy as np
import cv2 as cv

img = cv.imread('reconstructed_walls.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

corners = cv.goodFeaturesToTrack(gray, 400, 0.1, 1)

corners   = np.int0(corners)

for i in corners:
       x, y = i.ravel()
       print(f'x = {x}   y = {y}')
       cv.circle(img, (x, y), 3, 255, -1)
       
cv.namedWindow("Maze with Corners", cv.WINDOW_NORMAL)
cv.resizeWindow("Maze with Corners", 800, 600)
cv.imshow('Maze with Corners', img)

if cv.waitKey(0) and 0xff == 27:
       cv.destroyAllWindows()