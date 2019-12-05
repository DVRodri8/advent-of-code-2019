cont = 0
for n in range(372304, 847061):

    incr   = True
    now    = [-1, 1]
    d_nums  = set()
    for i, e in enumerate( str(n)[:-1] ):
        
        now[0] = int(e)
        if int(e) == int(str(n)[i+1]):
            now[1] += 1
        else:
            now[1] = 1
        
        if now[1] == 2:
            d_nums.add(now[0])
        elif now[1] == 3:
            d_nums.remove(now[0])

        if int(e) > int(str(n)[i+1]):
            incr = False
            break
            
    if len(d_nums) > 0 and incr:
        cont += 1

print(cont)
    