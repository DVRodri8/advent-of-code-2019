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
    def __init__(self, program, stdin=[]):
        self.program = copy.copy(program) + [0 for i in range(9000000)]
        self.p       = 0
        self.ter     = set([1,2,7,8])
        self.bin     = set([5,6])
        self.stdin   = copy.copy(stdin)
        self.p_in    = 0
        self.stdout  = []
        self.halt    = False
        self.WAIT    = -1
        self.offset  = 0

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
                if(a == 0): a+=1
                op3 = self.readNext(a, w=1)
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
    
    def readNext(self, mode=1, w=0):
        r = self.program[self.p]
        self.p += 1
        if mode == 0 and w==1: return r
        if mode == 0:   r = self.program[r]
        elif mode == 2:
            r = self.offset+int(r)
            if w==0: r = self.program[r]
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
            d = self.readNext(c, w=1)
            if self.p_in < len(self.stdin):
                a = self.stdin[self.p_in]
                self.p_in += 1
            else: 
                return self.WAIT
            self.writeTo(d, a) 
            
        elif mode == 4:
            d = self.readNext(c) 
            self.stdout += [d]
        elif mode == 9:
            d = self.readNext(c)
            self.offset += d
        else:
            print("algo ha ido mal en io",file=sys.stderr)
        
        return 0
