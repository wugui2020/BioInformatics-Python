import sys
#orig_stdout = sys.stdout
out = open("out.txt",'w')
#sys.stdout = out
class Node():
    def __init__(self,s,e,tree):
        self.start = s
        self.end = e
        self.link = None
        self.children = {}
        self.label = None
        self.tree = tree
    def __repr__(self):
        if self.start == None:
            return "root"
        return "string:"+self.tree.s[self.start:self.end]

class SuffixTree():
    def __init__(self,s,minlen):
        self.s = s
        self.root = Node(None,None,self)
        self.ap = [self.root, None, 0]
        self.remainder = 1
        self.lastinsert = None
        self.leaves = []
        self.nodes = []
        self.cur = None
        self.treeBuild(self.s)
        self.minlen = minlen


    def treeBuild(self,s):
        for i in xrange(len(s)):
            print "============================"
            print self
            print s[i] * 20
            self.lastinsert = None
            print self.ap, self.remainder
            self.addChar(i)
            print "post",self
            print "post",self.ap, self.remainder
            print "============================"

    def insertNew(self,i):
        print "new edge"
        newleave = Node(i,i+1,self)
        self.ap[0].children[self.s[i]] = newleave
        self.leaves.append(newleave)
        if self.apkeeper != None:
            self.ap = self.apkeeper
            self.apkeeper = None
        self.ap[1] = None
        self.ap[2] = 0 
        if self.ap[0] != self.root:
            self.linkMaker()

    def linkMaker(self):
        if self.lastinsert != None:
            print "made a link"
            print "from",self.s[self.lastinsert.start:self.lastinsert.end],
            print " to",self.s[self.ap[0].start:self.ap[0].end]
            self.lastinsert.link = self.ap[0]
        self.lastinsert = self.ap[0]


    def updateApEdge(self):
        print "updateApEdge"
        edge = self.ap[0].children[self.ap[1]]
        if edge.start + self.ap[2] == edge.end:
            self.ap[0] = self.ap[0].children[self.ap[1]]
            self.ap[1] = None
            self.ap[2] = 0

    def matchFinder(self,i):
        if self.ap[2] == 0:
            if self.s[i] in self.ap[0].children:
                print "new match"
                if self.ap[1] == None:
                    self.ap[1] = self.s[i]
                self.ap[2] += 1
                self.remainder += 1
                self.updateApEdge()
                print self.ap
                return True
        else:
            edge = self.ap[0].children[self.ap[1]]
            print "string", self.s[edge.start:edge.end]

            if edge.start + self.ap[2] < edge.end:
                if self.s[edge.start + self.ap[2]] == self.s[i]:
                    self.ap[2] += 1
                    self.updateApEdge()
                    self.remainder += 1
                    return True
            else:
                if self.s[edge.start] == self.ap[1] and self.ap[2] > 0:
                    if self.apkeeper == None:
                        self.apkeeper = self.ap
                    print self.ap
                    self.ap[0] = edge
                    self.ap[2] -= 1
                    self.ap[1] = self.s[i-self.ap[2]]
                    print self.ap
                    return self.matchFinder(i)



        return False 


    def mismatchFixer(self,i):
        # fix the new mixmatch
        count = self.remainder
        self.remainder = 1
        print "count", count 
        while count != 0:
            if self.ap[1] == None:
                if self.matchFinder(i) != True:
                    self.insertNew(i)
                    if self.ap[0].link:
                        self.ap[0] = self.ap[0].link
                    else:
                        self.ap[0] = self.root
            else:
                if self.matchFinder(i) != True:
                    if self.ap[2] == 0:
                        self.insertNew(i)
                    else:
                        print "spliting",self.ap
                        child = self.ap[0].children[self.ap[1]]
                        print self.s[child.start:child.end]
                        self.splitEdge(i)
            count -= 1 

    def addChar(self,i):
        print self.ap[0].children
        for node in self.leaves:
            node.end += 1
        if self.ap[1] == None:

            print "no existing match"
            if self.matchFinder(i) == False:
                print "mismatch"
                if self.remainder == 1:
                    self.insertNew(i)
                else:
                    self.mismatchFixer(i)


        else: # has existing match
            if self.matchFinder(i) == False:
                self.mismatchFixer(i)
                pass
        print "Done"

    def splitEdge(self,i):
        edge = self.ap[0].children[self.ap[1]]
        newnode = Node(edge.start, edge.start+self.ap[2],self)
        newchild = Node(edge.start+self.ap[2], edge.end,self)
        newleave = Node(i,i+1,self)
        newnode.children[self.s[newchild.start]] = newchild
        self.ap[0].children[self.s[newnode.start]] = newnode
        newnode.children[self.s[newleave.start]] = newleave

        print newnode.children
        self.nodes.append(newnode)
        self.leaves.append(newleave) 
        self.leaves.append(newchild)
        for leavei in xrange(len(self.leaves)):
            if self.leaves[leavei] == edge:
                self.leaves.pop(leavei)
                print "poped!!"
                pop = True
                break
        if self.lastinsert != None:
            print "made a link"
            print "from",self.s[self.lastinsert.start:self.lastinsert.end],
            print " to",self.s[newnode.start:newnode.end]
            self.lastinsert.link = newnode
        self.lastinsert = newnode
        print "testing ap for jump",self.ap
        print self
        if self.ap[0] != self.root: #and self.ap[0].link != None:
            print "it's me!"
            if self.ap[0].link:
                print "follow link"
                print self.ap[0].link
                self.ap[0] = self.ap[0].link
                return
            else:
                print "back to root"
                self.ap[0] = self.root
                return
        if self.apkeeper != None:
            self.ap = self.apkeeper
            self.apkeeper = None
        self.ap[2] -= 1
        print "updateing ap 1 ", self.s[i-self.ap[2]]
        self.ap[1] = self.s[i-self.ap[2]]
        print self.ap

    def __repr__(self):
        stack = [(0,self.root)]
        while stack != []:
            cur = stack.pop()
            if cur[1] != self.root:
                print "_."*cur[0],self.s[cur[1].start:cur[1].end],"(",cur[1].start,":",cur[1].end,")"
                print "_."*cur[0],"|"
            else:
                print "root"
                print "_."*cur[0],"|"
            for child in cur[1].children.values():
                stack.append((cur[0]+1,child))
        return ""

f = open("rosalind_suff.txt",'r')
s = f.readline()
print s
a = SuffixTree(s,20)
f.close()
out.close()
