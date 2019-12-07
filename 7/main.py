import sys
import copy
from itertools import permutations

class Opcode():
    def __init__(self, full_opcode):
        self.full_opcode = "{:05d}".format(int(full_opcode))
        self.op_code = int(self.full_opcode[-2:])
        self.modes   = list(map(int, self.full_opcode[:3]))

    def getOC(self):
        return self.op_code
    
    def getModes(self):
        return self.modes

class intMachine():
    def __init__(self, program, stdin):
        self.program = copy.copy(program)
        self.p       = 0
        self.ter     = set([1,2,7,8])
        self.bin     = set([5,6])
        self.stdin   = copy.copy(stdin)
        self.p_in    = 0
        self.stdout  = None
        self.halt    = False
        self.WAIT    = -1

    def isHalted(self):
        return self.halt

    def run(self):
        while True:
            foc = self.readOC()
            if foc.getOC() == 99:
                self.halt = True
                return self.stdout
                
            a,b,c = foc.getModes()
            
            if foc.getOC() in self.ter:
                op1 = self.readNext(c)
                op2 = self.readNext(b)
                op3 = self.readNext()
                self.writeTo(op3, self.calc2(foc.getOC(), op1, op2))
            elif foc.getOC() in self.bin:
                op1 = self.readNext(c)
                op2 = self.readNext(b)
                self.p = self.calc(foc.getOC(), op1, op2)
            else:
                if(self.io(foc.getOC(),c) == self.WAIT):
                    return self.stdout
            
    def appendStdin(self, data):
        self.stdin += [data]
    
    def re_run(self):
        self.p -= 2
        return self.run()

    def readOC(self):
        raw = self.readNext(1)
        return Opcode(raw)
    
    def readNext(self, mode=1):
        r = self.program[self.p]
        self.p += 1
        if mode == 0: r = self.program[r]
        return int(r)
    
    def calc(self, mode, a, p):
        if (mode == 5):  return p if a!=0 else self.p
        elif(mode == 6): return p if a==0 else self.p
        else:            print("Algo ha ido mal", file = sys.stderr)


    def calc2(self, mode, a, b):
        if(mode == 1):   return a+b
        elif(mode == 2): return a*b
        elif(mode == 7): return 1 if a<b else 0
        elif(mode == 8): return 1 if a==b else 0
        else:            print("algo ha ido mal",file=sys.stderr)
    
    def writeTo(self, d, v):
        self.program[d] = v

    def io(self, mode, c):
        if mode == 3:
            d = self.readNext(1)
            if self.p_in < len(self.stdin):
                a = self.stdin[self.p_in]
                self.p_in += 1
            else: 
                return self.WAIT
            self.writeTo(d, a) 
            
        elif mode == 4:
            d = self.readNext(c) 
            self.stdout = d
        else:
            print("algo ha ido mal en io",file=sys.stderr)
        
        return 0

nums  = [3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,94,175,256,337,418,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,2,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99]
better = [[], -1]
for p in permutations([5,6,7,8,9]):

    stdout = 0
    machines = []
    for i in p:
        m = intMachine(nums, [i, stdout])
        machines.append(m)
        stdout = m.run()

    while not machines[0].isHalted():
        for m in machines:
            m.appendStdin(stdout)
            stdout = m.re_run()
        

    if stdout > better[-1]:
        better = [p, stdout]
    
print(*better[0], "with thruster = ", better[1])