from PIL import Image
import random

img=Image.open("bw_maze_red_walls.png")
siize=w,h=img.size
data=img.load()
pieces=[]
walls=[]
red_shades = ['#ff0000']
# r = 255
# g = 0
# b = 0
# num_shades=1500000
# # Calculate the increment to get to the next shade
# increment = 255 // (num_shades - 1)

# for _ in range(num_shades):
#     # Convert RGB values to hexadecimal code
#     hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)

#     # Append the hexadecimal color code to the list
#     red_shades.append(hex_color)

#     # Increment the intensity of red for the next shade
#     r -= increment

for x in range(w):
    for y in range(h):
        hex_color='#'+''.join([ hex(it)[2:].zfill(2).upper() for it in data[x,y] ])
        # print(hex_color)
        pieces.append((x,y,hex_color))
        
        if hex_color =='#FF0000FF':
            walls.append((x,y,hex_color))
        
        

random.shuffle(pieces)
# print(pieces)



with  open('coords_maze.txt','w') as handle:
    for piece in pieces:
        handle.write(str(piece).replace("'",'')+'\n')

with  open('walls_maze.txt','w') as handle:
    for piece in walls:
        handle.write(str(piece).replace("'",'')+'\n')