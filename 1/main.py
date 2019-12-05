import sys

def recursiveCalc(i):
    a = calc(i)
    res = a
    while(a != 0):
        a = calc(a)
        res+=a
    return res

def calc(i):
    return max(0, i//3 - 2)
    
all =[]

for i in sys.stdin:

    i = i.strip()
    if(i != ''):
        i = int(i)

        all.append( recursiveCalc(i) )

print(sum(all))
