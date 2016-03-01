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
        self.cur[0].children[self.s[i]] = newleave
        self.leaves.append(newleave)
        self.cur[1] = None
        if self.cur[0] != self.root:
            self.linkMaker(self.cur[0])

    def linkMaker(self,node):
        print "linkMaker"
        if self.lastinsert != None:
            print "made a link"
            print "from",self.s[self.lastinsert.start:self.lastinsert.end],
            print " to",self.s[node.start:node.end]
            self.lastinsert.link = node
        print "lastinsert updated"
        self.lastinsert = node


    def updateApEdge(self,i):
        print "updateApEdge"
        edge = self.cur[0].children[self.cur[1]]
        if edge.start + self.cur[2] >= edge.end:
            self.cur[0] = edge
            self.cur[2] -= edge.end - edge.start
            if self.cur[2] != 0:
                self.cur[1] = self.s[i-self.cur[2]]
            else:
                self.cur[1] = None

    def matchFinder(self,i,count = 0):
        print "match with cur", self.cur
        if self.cur[2] == 0:
            if self.s[i] in self.cur[0].children:
                print "new match"
                if self.cur[1] == None:
                    self.cur[1] = self.s[i]
                self.cur[2] += 1
                self.remainder += 1
                self.updateApEdge(i)
                print "cur before return",self.cur
                return True
        else:
            edge = self.cur[0].children[self.cur[1]]
            print "string", self.s[edge.start:edge.end]

            if edge.start + self.cur[2] < edge.end:
                print "long enough edge"
                if self.s[edge.start + self.cur[2]] == self.s[i]:
                    self.cur[2] += 1
                    self.updateApEdge(i)
                    self.remainder += 1
                    return True
            else:
                print "short edge"
                if self.cur[2] > 0:
                    print self.cur
                    self.updateApEdge(i)
                    print self.cur
                    if self.s[edge.end-1] != self.s[i]:
                        print "matchFinder recurse"
                        return self.matchFinder(i)
                    else:
                        print "Matched"
                        self.remainder += 1
                        return True
        print "match False"



        return False 

    def linkTracker(self):
        print "linkTracker"
        if self.cur[0].link:
            print "follow the link", self.s[self.cur[0].link.start:self.cur[0].link.end]
            self.cur[0] = self.cur[0].link
        else:
            print "get back to root"
            self.cur[0] = self.root

    def apUpdate(self,i,update):
        self.ap[2] -= 1
        print "updateing ap", self.s[i-self.ap[2]]
        self.ap[1] = self.s[i-self.ap[2]]
        print self.ap

    def mismatchFixer(self,i):
        # fix the new mixmatch
        count = self.remainder
        remainder = self.remainder
        self.remainder = 1
        while count != 0:
            self.cur = self.ap[:]
            print "count", count 
            print "inserting", self.s[i-count+1:i+1]
            print "cur",self.cur
            print "ap",self.ap
            if self.cur[1] == None:
                if self.matchFinder(i,count) != True:
                    print "an new edge inserted"
                    self.insertNew(i)
                    self.linkTracker()
                    self.ap = self.cur[:]
                else:
                    if count == 1:
                        print "last insert"
                        self.ap = self.cur[:]
                    else:
                        print "inserting"
                        self.remainder -= 1
                        self.linkTracker()
                        self.apUpdate(i,count)

                    
            else:
                if self.matchFinder(i,count) != True:
                    if self.cur[2] == 0:
                        print "an new edge inserted"
                        self.insertNew(i)
                        self.linkTracker()
                        self.ap = self.cur[:]

                    else:
                        print "spliting",self.cur
                        child = self.cur[0].children[self.cur[1]]
                        print self.s[child.start:child.end]
                        self.splitEdge(i)
                        if self.cur[0] != self.root: #and self.ap[0].link != None:
                            self.linkTracker()
                            self.ap = self.cur[:]
                        else:
                            self.apUpdate(i,count)
                else:
                    if count == 1:
                        self.ap = self.cur[:]
                    else:
                        self.remainder -= 1
                        self.linkTracker()
                        self.apUpdate(i,count)
            print self.cur
            print self.ap
            print self
            count -= 1 

    def addChar(self,i):
        print self.ap[0].children
        for node in self.leaves:
            node.end += 1
        self.cur = self.ap
        if self.cur[1] == None:

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
        edge = self.cur[0].children[self.cur[1]]
        newnode = Node(edge.start, edge.start+self.cur[2],self)
        newchild = Node(edge.start+self.cur[2], edge.end,self)
        newleave = Node(i,i+1,self)
        newnode.children[self.s[newchild.start]] = newchild
        self.cur[0].children[self.s[newnode.start]] = newnode
        newnode.children[self.s[newleave.start]] = newleave
        newchild.children = edge.children
        newleave.child = edge.children

        print newnode.children
        self.nodes.append(newnode)
        print newchild.end , i
        if newleave.end == i+1:
            self.leaves.append(newleave) 
        if newchild.end == i+1:
            self.leaves.append(newchild)
        for leavei in xrange(len(self.leaves)):
            if self.leaves[leavei] == edge:
                self.leaves.pop(leavei)
                print "poped!!"
                pop = True
                break
        self.linkMaker(newnode)
        
        
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
s = "ATAAATG$"
a = SuffixTree(s,20)
print a
f.close()
out.close()
