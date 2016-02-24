def alignCost(xs,ys):
    x = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    y = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    m = [[0]*(len(ys)+1) for c in range(len(xs)+1)]
    gapstart = 11
    gapextend = 1
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
        m[0][i] = -1000000
        x[0][i] = gapstart + gapextend * i 
        y[0][i] = -1000000 
    for i in xrange(len(xs)+1):
        m[i][0] = -1000000
        x[i][0] = -1000000 
        y[i][0] = gapstart + gapextend * i 
    for i in xrange(len(xs)):
        for j in xrange(len(ys)):
            m[i+1][j+1] = max(
                    cost(xs[i],ys[j]) + m(i,j),
                    x(i,j),
                    y(i,j)
                    )
            x[i+1][j+1] = max(
                    gapstart + gapextend + m[i+1][j],
                    gapextend + x[i+1][j],
                    gapstart + gapextend + y[i+1][j]
                    )
            y[i+1][j+1] = max(
                    gapstart + gapextend + m[i][j+1],
                    gapstart + gapextend + x[i][j+1],
                    gapextend + y[i][j+1]
                    )
    return max(x[-1][-1],y[-1][-1],m[-1][-1])

def cost(x,y,mp):
    a = ord(x)-ord('A')
    b = ord(y)-ord('A')
    return mp[a][b]

"""
main program
"""

f = open("rosalind_glob.txt",'r')
x = ""
r = f.readline()
r = f.readline()
r = r.strip()
while r[0] != '>':
    x += r
    r = f.readline()
    r = r.strip()
r = f.readline()
r = r.strip()
y = ""
while r != "":
    y += r
    r = f.readline()
    r = r.strip()
f.close()

score = alignCost(x,y)
print score