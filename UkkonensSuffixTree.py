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
        self.remainder = 0
        self.lastinsert = None
        self.leaves = []
        self.nodes = []
        self.cur = None
        self.treeBuild(self.s)
        self.minlen = minlen


    def treeBuild(self,s):
        for i in xrange(len(s)):
            self.lastinsert = None
            self.addChar(i)

    def insertNew(self,i):
        newleave = Node(i,i+1,self)
        self.ap[0].children[self.s[i]] = newleave
        self.leaves.append(newleave)
        self.ap[1] = None
        self.linkMaker(self.ap[0])

    def linkMaker(self,node):
        if self.lastinsert != None:
            self.lastinsert.link = node
        self.lastinsert = node


    def updateApEdge(self,i):
        edge = self.ap[0].children[self.ap[1]]
        self.ap[0] = edge
        self.ap[2] -= edge.end - edge.start
        if self.ap[2] != 0:
            self.ap[1] = self.s[i-self.ap[2]]
        else:
            self.ap[1] = None

    def addChar(self,i):
        for node in self.leaves:
            node.end += 1
        self.remainder += 1
        while self.remainder != 0:
            if self.ap[2] == 0:
                self.ap[1] = self.s[i]
            if self.ap[1] in self.ap[0].children:
                edge = self.ap[0].children[self.ap[1]]
                if edge.start + self.ap[2] >= edge.end:
                    self.updateApEdge(i)
                    continue
                if self.s[edge.start + self.ap[2]] == self.s[i]:
                    self.ap[2] += 1
                    self.linkMaker(self.ap[0])
                    break
                else:
                    self.splitEdge(i)
            else:
                self.insertNew(i)

                
                
            self.remainder -= 1
            if self.ap[0] == self.root and self.ap[2] > 0:
                self.ap[2] -= 1
                self.ap[1] = self.s[i-self.ap[2]]
            else:
                if self.ap[0].link != None:
                    self.ap[0] = self.ap[0].link
                else:
                    self.ap[0] = self.root

    def splitEdge(self,i):
        print "splitEdge"
        edge = self.ap[0].children[self.ap[1]]
        newnode = Node(edge.start, edge.start+self.ap[2],self)
        newchild = Node(edge.start+self.ap[2], edge.end,self)
        newleave = Node(i,i+1,self)
        newnode.children[self.s[newchild.start]] = newchild
        self.ap[0].children[self.s[newnode.start]] = newnode
        newnode.children[self.s[newleave.start]] = newleave
        newchild.children = edge.children
        newleave.child = edge.children

        self.nodes.append(newnode)
        print newchild.end , i
        if newleave.end == i+1:
            self.leaves.append(newleave) 
        if newchild.end == i+1:
            self.leaves.append(newchild)
        for leavei in xrange(len(self.leaves)):
            if self.leaves[leavei] == edge:
                self.leaves.pop(leavei)
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
a = SuffixTree(s,20)
print a
f.close()
