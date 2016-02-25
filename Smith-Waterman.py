test = False
def alignCost(xs,ys,gapstart,gapextend):
    x = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    y = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    m = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    INFINITY = 100000
    mp = [
            [4,'#',0,-2,-1,-2, 0,-2,-1,'#',-1,-1,-1,-2,'#',-1,-1,-1, 1, 0,'#',0,-3,'#',-2],
            [],
            [0,'#',9,-3,-4,-2,-3,-3,-1,'#',-3,-1,-1,-3,'#',-3,-3,-3,-1,-1,'#',-1,-2,'#',-2],
            [-2,'#',-3,6,2,-3,-1,-1,-3,'#',-1,-4,-3,1,'#',-1,0,-2,0,-1,'#',-3,-4,'#',-3],
            [-1,'#',-4,2,5,-3,-2,0,-3,'#',1,-3,-2,0,'#',-1,2,0,0,-1,'#',-2,-3,'#',-2],
            [-2,'#',-2,-3,-3,6,-3,-1,0,'#',-3,0,0,-3,'#',-4,-3,-3,-2,-2,'#',-1,1,'#',3],
            [0,'#',-3,-1,-2,-3,6,-2,-4,'#',-2,-4,-3,0,'#',-2,-2,-2,0,-2,'#',-3,-2,'#',-3],
            [-2,'#',-3,-1,0,-1,-2,8,-3,'#',-1,-3,-2,1,'#',-2,0,0,-1,-2,'#',-3,-2,'#',2],
            [-1,'#',-1,-3,-3,0,-4,-3,4,'#',-3,2,1,-3,'#',-3,-3,-3,-2,-1,'#',3,-3,'#',-1],
            [],
            [-1,'#',-3,-1,1,-3,-2,-1,-3,'#',5,-2,-1,0,'#',-1,1,2,0,-1,'#',-2,-3,'#',-2],
            [-1,'#',-1,-4,-3,0,-4,-3,2,'#',-2,4,2,-3,'#',-3,-2,-2,-2,-1,'#',1,-2,'#',-1],
            [-1,'#',-1,-3,-2,0,-3,-2,1,'#',-1,2,5,-2,'#',-2,0,-1,-1,-1,'#',1,-1,'#',-1],
            [-2,'#',-3,1,0,-3,0,1,-3,'#',0,-3,-2,6,'#',-2,0,0,1,0,'#',-3,-4,'#',-2],
            [],
            [-1,'#',-3,-1,-1,-4,-2,-2,-3,'#',-1,-3,-2,-2,'#',7,-1,-2,-1,-1,'#',-2,-4,'#',-3],
            [-1,'#',-3,0,2,-3,-2,0,-3,'#',1,-2,0,0,'#',-1,5,1,0,-1,'#',-2,-2,'#',-1],
            [-1,'#',-3,-2,0,-3,-2,0,-3,'#',2,-2,-1,0,'#',-2,1,5,-1,-1,'#',-3,-3,'#',-2],
            [1,'#',-1,0,0,-2,0,-1,-2,'#',0,-2,-1,1,'#',-1,0,-1,4,1,'#',-2,-3,'#',-2],
            [0,'#',-1,-1,-1,-2,-2,-2,-1,'#',-1,-1,-1,0,'#',-1,-1,-1,1,5,'#',0,-2,'#',-2],
            [],
             [0,'#',-1,-3,-2,-1,-3,-3,3,'#',-2,1,1,-3,'#',-2,-2,-3,-2,0,'#',4,-3,'#',-1],
             [-3,'#',-2,-4,-3,1,-2,-2,-3,'#',-3,-2,-1,-4,'#',-4,-2,-3,-3,-2,'#',-3,11,'#',2],
             [],
             [-2,'#',-2,-3,-2,3,-3,2,-1,'#',-2,-1,-1,-2,'#',-3,-1,-2,-2,-2,'#',-1,2,'#',7]
             ]
    # matrices initialization
    for i in xrange(len(ys)+1):
        m[0][i] = -INFINITY
        x[0][i] = 0 #gapstart + gapextend * i 
        y[0][i] = 0 #-INFINITY 
    for i in xrange(len(xs)+1):
        m[i][0] = -INFINITY
        x[i][0] = 0# -INFINITY 
        y[i][0] = 0#gapstart + gapextend * i 
    m[0][0] = 0
    for i in xrange(len(xs)):
        for j in xrange(len(ys)):
            m[i+1][j+1] = cost(xs[i],ys[j],mp) + max(
                    m[i][j],
                    x[i][j],
                    y[i][j]
                    )
            x[i+1][j+1] = max(
                    gapstart + m[i+1][j],
                    gapextend + x[i+1][j],
                    gapstart + y[i+1][j]
                    )
            y[i+1][j+1] = max(
                    gapstart + m[i][j+1],
                    gapstart + x[i][j+1],
                    gapextend + y[i][j+1]
                    )
    return x,y,m

def cost(x,y,mp):
    a = ord(x)-ord('A')
    b = ord(y)-ord('A')
    return mp[a][b]

def traceback(xs,ys,x,y,m,gapstart,gapextend):
    a = []
    b = []
    xi = -1
    yi = -1
    i = -1
    j = -1
    currentMatrix = None
    flag = False
    maxitem = None
    for array in m:
        if max(array) > maxitem:
            maxitem = max(array)
    while i > -len(xs)-1 and j > -len(ys)-1:
        if currentMatrix != None and flag == True and currentMatrix[i][j] == 0:
            break
        if m[i][j] == maxitem or x[i][j] == maxitem or y[i][j] == maxitem:
            flag = True
        if currentMatrix == None or currentMatrix == m:
            candidates = (m[i][j],x[i][j],y[i][j])
        elif currentMatrix == x:
            candidates = (
                     gapstart + m[i][j],
                     gapextend + x[i][j],
                     gapstart + y[i][j]
                     )
        else:
            candidates = (
                     gapstart + m[i][j],
                     gapstart + x[i][j],
                     gapextend + y[i][j]
                     )
        ma = max(candidates)
        if ma == candidates[0]:
            currentMatrix = m
            if flag:
                a.append(xs[xi])
                b.append(ys[yi])
            xi -= 1
            yi -= 1
            i -= 1
            j -= 1
        elif ma == candidates[1]:
            currentMatrix = x
            if flag:
                b.append(ys[yi])
            yi -= 1
            j -= 1
        else:
            currentMatrix = y
            if flag:
                a.append(xs[xi])
            xi -= 1
            i -= 1
    return a,b,maxitem


"""
main program
"""

f = open("rosalind_laff.txt",'r')
xs = ""
r = f.readline()
r = f.readline()
r = r.strip()
while r[0] != '>':
    xs += r
    r = f.readline()
    r = r.strip()
r = f.readline()
r = r.strip()
ys = ""
while r != "":
    ys += r
    r = f.readline()
    r = r.strip()
f.close()
if test == True:
    xs = "PLEASANTLY"
    ys =  "MEANLY"

x,y,m = alignCost(xs,ys,-11,-1)
a,b,maxitem = traceback(xs,ys,x,y,m,-11,-1)
a.reverse()
b.reverse()
a = ''.join(a)
b = ''.join(b)
if test:
    for c in x:
        print c
    for c in y:
        print c
    for c in m:
        print c
print maxitem
print a
print b

