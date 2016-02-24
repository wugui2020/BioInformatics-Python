"""
===================
   BoyerMooore
===================
"""
def boyerMoore(t,p):
    occur = rComputing(p)
    L,zlist = LProcessing(p)
    k = 0
    result = []
    while k < len(t)-len(p)+1:
        j = len(p)-1
        while j >= 0:
            if t[k+j] == p[j]:
                j -= 1
            else:
                break
        if j == -1:
            result.append(k+1)
        b = badChar(k+j,j,t,occur,p)
        g = goodChar(j+1,p,L,zlist)
        s = max (b, g, 1)
        k += s
    return result 

def badChar(k,j,t,occur,p):
    if j == -1:
        return 0
    target = R(j, t[k], occur)
    return j-target 
def goodChar(j,p,L,zlist):
    if j == len(p):
        return 0 
    if j == 0 or L[j] == 0:
        beta = 0
        a = 0
        while a < len(p)-j:
            if a + 1 == zlist[a]:
                beta = a + 1
            a += 1
        return len(p) - beta
    else:
        return len(p) - (L[j] + 1) 

def LProcessing(p):
    rp = p[::-1]
    zlist = preProcessing(rp,rp)
    zlist = zlist[len(rp)+1:]
    nlist = zlist[::-1]
    Llist = [0]*(len(p)+1)
    for j in xrange(0,len(p)-1):
        Llist[len(p) - nlist[j]] = j
    return Llist,nlist

"""
=========================
   z-algorithm start
=========================
"""

def preProcessing(t,p):
    s = p + "$" + t
    l = 0
    r = 0
    zlist = [len(p)]
    for i in xrange(1,len(s)):
        if i > r:
            zlist.append(zcompute(i,0,s,zlist))
            if zlist[i] > 0:
                l = i
                r = i + zlist[i] - 1
        else:
            if zlist[i-l] < r-i+1:
                zlist.append(zlist[i-l])
            else:
                postr = zcompute(r+1,r-i+1,s,zlist)
                zlist.append(r-i+1+postr)
                l = i
                r = r + postr
    return zlist

def zcompute(x, y, s, zlist):
    p = x
    while x < len(s):
        if s[x] == s[y+x-p]:
            x += 1
        else:
            break
    return x - p

def zmatch(t,p):
    zlist = preProcessing(t,p)
    result = []
    for i in xrange(1,len(zlist)):
        if zlist[i] >= len(p):
            result.append(i-len(p))
    return result
"""
=============================
     z-algorithm end
=============================
"""


def R(i,x,occur):
    if x not in occur:
        return i
    alist = occur[x]
    rvalue = 0
    while rvalue < len(alist):
        if alist[rvalue] >= i:
            rvalue += 1
        else:
            return alist[rvalue]
    return 0

def rComputing(p):
    occur = {}
    for i in xrange(len(p)-1,-1,-1):
        if p[i] not in occur:
            occur[p[i]] = [i]
        else:
            occur[p[i]].append(i)
    return occur

"""
=================
   Main program 
=================
"""


f = open("rosalind_subs.txt","r")
s = f.readline()
t = f.readline()
s = s.strip()
t = t.strip()
result = boyerMoore(s,t)
for i in result:
    print i,
