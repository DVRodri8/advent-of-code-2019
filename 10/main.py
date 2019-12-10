from math import sqrt, atan2, degrees
import numpy as np
from copy import copy
import sys
from time import sleep, perf_counter as pc
from os import system

# Function getPointsBetween by @antooro
# https://raw.githubusercontent.com/antooro/advent-of-code-2019/master/day10/day10.py
# is a really fast way to solve part 1 (1.59s on my i7)
# my first aproach took 47s with 3 nested loops

ANIMATION  = True
LINUX      = True
DELAY      = 0.2
INPUT_FILE = "input"

class P():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def asList(self):
        return [self.x, self.y]

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class AsteroidMap():

    def __init__(self, area):
        self.area = area
        self.asteroids = []
        for y,row in enumerate(self.area):
            for x, value in enumerate(row):
                if value == '#':
                    self.asteroids.append(P(x,y))
    
    def __str__(self):
        r = ""
        for a in self.area: r+=" ".join(a)+"\n"
        return r

    def setStation(self, location):
        self.station = location
        self.area[location.y][location.x] = '\033[32m#\033[0m'

    def destroy(self, point):
        self.asteroids.remove(point)
        self.area[point.y][point.x] = '.'

    def angle(self, p1, p2):
        d = degrees(atan2(p1.y-p2.y, p1.x-p2.x))
        d = (270 + d) % 360
        return d

    def getDegNearbyOf(self, me):
        nearby = self.getFullNearbyOf(me)
        degNearby = [[self.angle(me, i[1]), *i] for i in nearby]
        return degNearby

    def getFullNearbyOf(self, me):
        tmp = []
        for i in self.asteroids:
            tmp.append([self._distance(me, i), i])

        tmp = sorted(tmp, key=lambda x: x[0])
        return tmp

    def getNearbyOf(self, me):
        return [i[1] for i in self.getFullNearbyOf(me)]

    def _distance(self, A, B):
        return sqrt((A.x - B.x)**2 + (A.y - B.y)**2)

    def getPointsBetween(self, A, B):
        
        a = B.y - A.y 
        b = A.x - B.x  
        c = a*(A.x) + b*(A.y)  

        min_x = min(B.x,A.x)
        min_y = min(B.y,A.y)
        max_x = max(B.x,A.x)
        max_y = max(B.y,A.y)

        range_a = range(min_y, max_y+1)
        range_b = range(min_x, max_x+1)

        for y_val in range_a:
            try:
                x = (c-b*y_val)/a
            except:
                x = 0.0
            if x.is_integer():
                if x >= min_x and x <= max_x:
                    p = P(int(x), y_val)
                    if p!=A and p!=B:
                        yield p

        for x_val in range_b:
            try:
                y = (c-a*x_val)/b
            except:
                y = 0.0
            if y.is_integer():
                if y >= min_y and y <= max_y:
                    p = P(x_val, int(y))
                    if p!=A and p!=B:
                        yield p


    def colorBetween(self, A,B, color):
        for p in list(self.getPointsBetween(A,B)) + [A,B]:
            printable = '#' if '#' in self.area[p.y][p.x] else '.'
            self.area[p.y][p.x] = f'\033[{color}m{printable}\033[0m' 

    def myView(self, asteroid):
        nearby = self.getNearbyOf(asteroid)
        cov = nearby.pop(0)
        visionRange = set()
        for asteroid in nearby:
            for i in self.getPointsBetween(cov, asteroid):
                if i in visionRange: break
            else:
                visionRange.add(asteroid)

        return visionRange
    
    def countViews(self, nearby):
        return len(self.myView(nearby))

command = "clear" if LINUX else "cls"

area = []
with open("input", "r") as f:
    for i in f.readlines():
        area.append([a for a in i.strip()])

best = [-1, []]

# Part 1
AM = AsteroidMap(area)
tot = pc()
nearby = 0
couvw = 0
for asteroid in AM.asteroids:
    v=AM.countViews(asteroid)
    if v > best[0]:
        best = [v, asteroid]
print("total", pc()-tot)

# Part 2

location = best[-1]
AM.setStation(location)
myView = AM.myView(location)
info = sorted(AM.getDegNearbyOf(location), key=lambda x: x[0])
counter = 0
print(AM)
while len(myView) > 0:
    
    for i in info:
        asteroid = i[-1]
        if asteroid in myView:
            counter+=1
            if(counter==200): print("WIN", asteroid, "result: ", asteroid.x*100+asteroid.y)
            if ANIMATION:
                AM.colorBetween(location, asteroid, 31)
                system(command)
                print(AM)
                sleep(0.2)
                AM.colorBetween(location, asteroid, 0)
            AM.destroy(asteroid)
            
    
    myView = AM.myView(location)
    info = sorted(AM.getDegNearbyOf(location), key=lambda x: x[0])

print("END")
