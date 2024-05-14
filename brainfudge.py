r = [0 for i in range(36000)]; cr = 0
def chanr(d=1):
    global cr; cr += d; r[cr] = r[cr] if len(r) > cr else 0
def inr(d=1):
    global cr; r[cr] += d
    if r[cr] > 255: r[cr] = 0
    elif r[cr] < 0: r[cr] = 255
i = input(); loops = []; ind = 0; ch = i[ind]
while ch != '' and ch != None:
    if ch == '>': chanr()
    elif ch == '<':chanr(d=-1)
    elif ch == '+': inr()
    elif ch == '-': inr(d=-1)
    elif ch == '.': print(chr(r[cr]), end='')
    elif ch == ',': r[cr] = ord(input()[0])
    elif ch == '[': loops.append(ind)
    elif ch == ']':
        if r[cr] != 0: ind = loops[-1]
        else: del loops[-1]
    ind += 1; ch = i[ind] if ind < len(i) else None