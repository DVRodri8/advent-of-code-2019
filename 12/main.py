class Moon():
    def __init__(self, position, id, velocity=[0,0,0]):
        self.x, self.y, self.z = position
        self.velocity = velocity[:]
        self.id = id

    def getID(self):
        return self.id

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y 
    
    def getZ(self):
        return self.z 

    def apX(self, ac):
        self.velocity[0] += ac

    def apY(self, ac):
        self.velocity[1] += ac

    def apZ(self, ac):
        self.velocity[2] += ac
    
    def move(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.z += self.velocity[2]


    def __str__(self):
        return f"pos=<x={self.x}, y={self.y}, z={self.z}>, vel={self.velocity}"
    
    def __repr__(self):
        return self.__str__()

    def energy(self):
        s = abs(self.x) + abs(self.y) + abs(self.z) 
        return s * sum([abs(i) for i in self.velocity])

with open("input", "r") as f:
    moons = [Moon([int(j.split('=')[-1]) for j in i.replace(">","").split(',')], ix) for ix,i in enumerate(f.readlines())]

ts = 0
lon = len(moons)

gs = [Moon.getX, Moon.getY, Moon.getZ]
aps = [Moon.apX, Moon.apY, Moon.apZ]

xstates = set()
ystates = set()
zstates = set()

# Part 1
while ts < 1000000:
    for i in range(3):
        get = gs[i]
        ap = aps[i]
        moons.sort(key=get)
        cpy = [get(i) for i in moons]
        rcpy = cpy[::-1]
        for m in moons:
            s = rcpy.index(get(m)) - cpy.index(get(m)) 
            ap(m,s)
        
    for m in moons:
        m.move()
    ts+=1
print(sum([m.energy() for m in moons]))

# Part 2
# A dirty way to find the patterns

xc = {}
yc = {}
zc = {}
ts = 0

while ts < 750000:
    
    for i in range(3):
        get = gs[i]
        ap = aps[i]

        moons.sort(key=get)
        for i,m in enumerate(moons):
            s = lon - i-1 - i
            for m2 in moons[i+1:]:
                if get(m2) == get(m): s-=1
                else: break
            for m2 in moons[:i][::-1]:
                if get(m2) == get(m): s+=1
                else: break
            ap(m,s)
    for m in moons: m.move()
    
    moons.sort(key=Moon.getID)
    ko = ":".join([str(i.getX()) for i in moons])+"p"+":".join([str(i.velocity[0]) for i in moons])
    l=len(xstates)
    xstates.add(ko)
    if len(xstates) == l:
        xc[ko].append(ts)
    else:
        xc[ko] = [ts]

    ko = ":".join([str(i.getY()) for i in moons])+"p"+":".join([str(i.velocity[1]) for i in moons])
    l=len(ystates)
    ystates.add(ko)
    if len(ystates) == l:
        yc[ko].append(ts)
    else:
        yc[ko] = [ts]

    ko = ":".join([str(i.getZ()) for i in moons])+"p"+":".join([str(i.velocity[2]) for i in moons])
    l=len(zstates)
    zstates.add(ko)
    if len(zstates) == l:
        zc[ko].append(ts)
    else:
        zc[ko] = [ts]

    ts+=1

a=0
for k,v in xc.items():
    if len(v) == 1: a+=1
print(a)

a=0
for k,v in yc.items():
    if len(v) == 1: a+=1
print(a)

a=0
for k,v in zc.items():
    if len(v) == 1: a+=1
print(a)

o=0
g=[]
for k,v in yc.items():
    for i in v:
        g.append([o, i])
    o+=1
g.sort(key=lambda x: x[1])
b=[i[0] for i in g]
ry = b.index(0, 1) 

o=0
g=[]
for k,v in zc.items():
    for i in v:
        g.append([o, i])
    o+=1
g.sort(key=lambda x: x[1])
b=[i[0] for i in g]
rz = b.index(0, 1) 

o=0
g=[]
for k,v in xc.items():
    for i in v:
        g.append([o, i])
    o+=1
g.sort(key=lambda x: x[1])
b=[i[0] for i in g]
rx = b.index(0, 1)

def mcd(num1, num2):
    a = max(num1, num2)
    b = min(num1, num2)
    while b!=0:
        mcd = b
        b = a%b
        a = mcd
    return mcd
 
def mcm(num1, num2):
    a = max(num1, num2)
    b = min(num1, num2)
    mcm = (a / mcd(a, b)) * b
    return mcm
print(rx, ry, rz)
print(mcm(rx,mcm(ry,rz)))

