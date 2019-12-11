from intMachine import intMachine
import sys
from time import sleep
from PIL import Image
from os import system
import imageio


ANIMATION = False


black_points = set()
new_points   = set()
position = [0,5]
direction = 90
TX = 43
TY = 6
cont = 0
pics = []

def paintPoint(position, paint):
    global black_points, new_points

    new_points.add(tuple(position))
    if paint == 0:
        black_points.add(tuple(position))
    else:
        black_points.discard(tuple(position))

def move_robot(vector, steps=1):
    global position, direction
    direction += 90 if vector==0 else 270
    direction %= 360
    
    x,y = position
    if   direction == 0  : x+=steps
    elif direction == 90 : y+=steps
    elif direction == 180: x-=steps
    elif direction == 270: y-=steps
    else: print("mala direccion", direction); sys.exit()
    position = [x,y]

def save_pic():
    global black_points, cont, pics
    wall = Image.new("1", (TX,TY))
    for y in range(TY):
        for x in range(TX):
            c = 0 if (x,y) in black_points else 1
            wall.putpixel((x,TY-1-y), c)
    wall = wall.resize((wall.width * 50, wall.height*50))
    wall.save(f"tmp/matricula{cont}.png")
    pics.append(imageio.imread(f"tmp/matricula{cont}.png"))
    cont += 1

with open("input", "r") as f:
    program = [int(i) for i in f.readline().strip().split(',')]


color = 1
computer = intMachine(program, [color])
paint, vector = computer.run()
paintPoint(position, paint)
move_robot(vector)
if ANIMATION:
    system("mkdir tmp")
    save_pic()

while not computer.isHalted():
    color = 0 if tuple(position) in black_points else 1
    computer.appendStdin(color)
    paint, vector = computer.re_run()[-2:]
    paintPoint(position, paint)
    move_robot(vector)
    if ANIMATION: save_pic()

# Part 1
print(len(new_points))

# Part 2

wall = Image.new("1", (TX,TY))
for y in range(TY):
    for x in range(TX):
        c = 0 if (x,y) in black_points else 1
        wall.putpixel((x,TY-1-y), c)
wall = wall.resize((wall.width * 50, wall.height*50))
wall.save("matricula.png")

if ANIMATION:
    imageio.mimsave("animation.gif", pics, fps=10)
    system("rm -rf tmp")
