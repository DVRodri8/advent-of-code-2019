from time import sleep
from intMachine import intMachine
from os import system
from time import sleep

class Arcade():
    
    def __init__(self, program, ws=[], animation=False):
        self.__computer = intMachine(program)
        self.__mblock = [ ' ', '#', 'B', '-', 'O']
        self.__screen = [['%' for i in range(23)] for i in range(37)]
        self.__score = 0
        self.__ws = ws[:]
        self.__ANIMATION = animation
    
    def __nextFrame(self):
        output = self.__computer.run()
        return [output[i:i+3] for i in range(0,len(output),3)]

    def __updateScreen(self):
        for t in self.__nextFrame():
            x,y,c = t
            if x==-1 and y == 0:
                self.__score = c
            else:
                self.__screen[x][y] = self.__mblock[c]

    def __print(self):
        system("clear")
        print("score:",self.__score)
        for i in range(len(self.__screen[0])):
            for j in range(len(self.__screen)):
                print(self.__screen[j][i], end='')
            print()
        sleep(0.01)

    
    def __interact(self):
        if len(self.__ws) > 0:
            i = self.__ws.pop(0)
        else:
            i = input()
        d=0
        if i=='a': d=-1
        elif i=='d': d=1
        self.__computer.appendStdin(d)

    def print(self):
        self.__updateScreen()
        self.__print()

    def run(self):
        while True:
            self.__updateScreen()
            if self.__ANIMATION: self.__print()
            self.__interact()
            if self.__computer.isHalted(): break
            else: self.__computer.run()
        if not self.__ANIMATION: print(self.__score)


with open("input", "r") as f:
    program = list(map(int, f.readline().strip().split(",")))

# Part 1
G=intMachine(program)
output = G.run()
print(len([i for i in output[2::3] if i==2]))

# Part 2

# My way to find which part of memory store the board
# in order to don't wait for inputs raise an Exception on
# io instructions on the intMachine class
'''
zeros = []
for i,v in enumerate(program):
    if v==0: zeros.append(i)

for i in zeros:
    break
    p = program[:]
    p[i] = 3
    try:
        Arcade(p).print()
    except:
        print("no")
    print(i)
    sleep(0.0001)
'''

# Replace floor space with wall
for i in range(1416, 1416+36):
    program[i]=1

G = Arcade(program, ['n']*5000, True)
G.run()
