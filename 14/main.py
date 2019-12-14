
from math import ceil
import networkx as nx

class Element():
    def __init__(self, name, amount):
        self.name   = name
        self.amount = amount

    def __str__(self):
        return str(self.amount)+" "+self.name
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(hash(self.name)+hash(self.amount))

class Reaction():
    def __init__(self, reactivs, product):
        self.reactivs = reactivs
        self.product  = product
    
    def __str__(self):
        r=' + '.join([str(i) for i in self.reactivs]) + " => " + str(self.product)
        return r
    
    def __repr__(self):
        return self.__str__()

reactions = {'ORE':Reaction([], Element('ORE', 1))}
G=nx.DiGraph()
with open("input", 'r') as f:
    for r in f.readlines():
        r=r.strip()
        reactivs = []
        rs, p = r.split('=>')
        rs=rs.split(',')
        for react in rs:
            react=list(filter(lambda x: x!='', react.split(' ')))
            reactivs.append(Element(react[1], int(react[0])))
        
        p = list(filter(lambda x: x!='', p.split(' ')))
        product = Element(p[1], int(p[0]))
        reactions[product.name] = Reaction(reactivs, product)
        for v in reactivs:
            G.add_weighted_edges_from([(product.name, v.name, str(v.amount))])

needs = {}
def clear():
    global needs
    for i in reactions.keys():
        needs[i] = 0

def necesidades():
    global needs

    for name in nx.topological_sort(G):
        for reactiv in reactions[name].reactivs:
            np = ceil(needs[name] / reactions[name].product.amount)
            needs[reactiv.name] +=  np*reactiv.amount

def ore4fuel(f):
    clear()
    needs['FUEL'] = f
    necesidades()
    return needs['ORE']

# Part 1
print(ore4fuel(1))

# Part 2
upper = 1e12
lower = 1
while upper-lower > 1:
    m = (upper + lower)//2
    if ore4fuel(m) > 1e12: upper = m
    else: lower = m

if(ore4fuel(upper) <= 1e12): lower=upper
print(int(lower))


