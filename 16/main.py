pattern = [0,1,0,-1]
simple = "59768092839927758565191298625215106371890118051426250855924764194411528004718709886402903435569627982485301921649240820059827161024631612290005106304724846680415690183371469037418126383450370741078684974598662642956794012825271487329243583117537873565332166744128845006806878717955946534158837370451935919790469815143341599820016469368684893122766857261426799636559525003877090579845725676481276977781270627558901433501565337409716858949203430181103278194428546385063911239478804717744977998841434061688000383456176494210691861957243370245170223862304663932874454624234226361642678259020094801774825694423060700312504286475305674864442250709029812379"
offset = int(simple[:7])
simple *= 10000
print(len(simple))
simple = simple[offset:]
seq = [int(i) for i in simple]
cpy = seq[:]
F = 100

print(len(seq))

# Part 2
# we can eliminate left part
# offset is bigger than sequence length / 2
# so pos i is sum from i to end
for phase in range(F):
    neg = 0
    suma = sum(seq)
    new_seq = []
    print(phase)
    for i in range(len(seq)):

        new_seq.append( int(str(suma-neg)[-1]) )
        neg += seq[i] 

    seq = new_seq
naseq = seq[:]

seq = cpy[:]

'''
# Trivial part 1
apats = []
for c in range(1,len(seq)+1):
    apat = []
    for i in pattern: apat.extend([i]*c)
    apats.append(apat)


for phase in range(1,F+1):
    new_seq = []
    for c in range(1,len(seq)+1):
        apat = apats[c-1]
        sa = 1
        digits = []
        for n in seq:
            digits.append( n*(apat[sa]) )
            sa = (sa+1) % len(apat)
        # if c==2: print(digits)
        new_seq.append(int(str(sum(digits))[-1]))
    seq = new_seq
print(*seq[:8], sep='')
'''
print(*naseq[:8], sep='')

    
        