from PIL import Image
import cv2

walls=[]
max_x=max_y=0
c = 0
with open('walls_maze.txt') as handle:
       for line in handle.readlines():
              c+=1
              x,y,color=line.strip().split()
              x=int(x[1:-1])
              y=int(y[:-1])
              
              r=int(color[1:3],16)
              g=int(color[3:5],16)
              b=int(color[5:7],16)
              
              walls.append([x,y,r,g,b])
              
              max_x=max([x,max_x])
              max_y=max([y,max_y])
              
w=max_x+1
h=max_y+1
size=w,h
img=Image.new('RGB',size)

data=img.load()

for coord in walls:
       x,y,r,g,b=coord
       data[x,y]=(r,g,b)
       
       
img.show()
img.save('reconstructed_walls.jpg')
print(c)


