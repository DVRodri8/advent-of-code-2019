import sys

# Adjacent List
orbits = {}
for orbit in sys.stdin:
    A, B = [i.strip() for i in orbit.split(")")]
    orb = orbits.get(A, [])
    orb.append(B)
    orbits[A] = orb
    
    # This 3 lines make graph bidirectional
    # Only needed in part 2
    orb = orbits.get(B, [])
    orb.append(A)
    orbits[B] = orb

# Part 1
# Start from COM, is the head of the tree with value 0
# calculate the distance to his childs and do this
# until there is no more childs
# then sum the values 
'''
heads = set(["COM"])
next_iter = set()

orbCountDict = {"COM":0}
while len(heads) > 0:
    next_iter = set()
    for i in heads:
        head_v = orbCountDict[i]
        for child in orbits.get(i,[]):
            actual = orbCountDict.get(child, 0)
            orbCountDict[child] = actual + head_v + 1
            next_iter.add(child)
    heads = next_iter

res = sum(orbCountDict.values())
print(res)
'''

# Part 2
# Dijkstra
# There is no cycle so apply dijkstra and show
# Santa's distance, substract 2 because YOU and SAN
# aren't orbital transfers

distances = {"YOU":0}
heads = ["YOU"]
next_iter = []

while len(heads) > 0:
    next_iter = []
    for i in heads:
        head_v = distances[i]
        for neig in orbits.get(i, []):
            actual = distances.get(neig, float("inf"))
            if actual < float("inf"): continue
            if actual > head_v+1:
                distances[neig] = head_v+1
            next_iter.append(neig)
    heads = next_iter
print(distances["SAN"]-2)