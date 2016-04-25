import sys
from graphviz import Digraph
class Node():
    def __init__(self,s,e,tree):
        self.start = s
        self.end = e
        self.link = None
        self.linked_to = None
        self.children = {}
        self.label = None
        self.tree = tree
    def __repr__(self):
        if self.start == None:
            return "root"
        return "string:"+self.tree.s[self.start:self.end] + "(%s,%s)" % (self.start, self.end)

class SuffixTree():
    def __init__(self,s,minlen):
        self.s = s
        self.root = Node(None,None,self)
        self.ap = [self.root, None, 0]
        self.remainder = 0
        self.dot = Digraph()
        self.lastinsert = None
        self.leaves = []
        self.nodes = [self.root]
        self.cur = None
        self.treeBuild(self.s)
        self.minlen = minlen


    def treeBuild(self,s):
        for i in xrange(len(s)):
            self.lastinsert = None
            self.addChar(i)
            self.__str__()
            if i < 10:
                self.dot = Digraph()
                self.__repr__(i)
            print self.ap

    def insertNew(self,i):
        newleave = Node(i,i+1,self)
        self.ap[0].children[self.s[i]] = newleave
        self.leaves.append(newleave)
        self.ap[1] = None
        self.linkMaker(self.ap[0])

    def linkMaker(self,node):
        if self.lastinsert != None:
            self.lastinsert.link = node
            node.linked_to = self.lastinsert
            print "made a link from", self.lastinsert, node
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
                print "link",self.ap[0].link
                if self.ap[0].link != None:
                    self.ap[0] = self.ap[0].link
                else:
                    self.ap[0] = self.root
            print "end loop==========="
            print self, self.ap
            print "end"


    def splitEdge(self,i):
        print "nodes pre",self.nodes
        print "leaves pre",self.leaves
        edge = self.ap[0].children[self.ap[1]]
        newnode = Node(edge.start, edge.start+self.ap[2],self)
        newchild = Node(edge.start+self.ap[2], edge.end,self)
        newleave = Node(i,i+1,self)
        newnode.children[self.s[newchild.start]] = newchild
        print "ap[0] children",self.ap[0].children
        self.ap[0].children[self.s[newnode.start]] = newnode
        newnode.children[self.s[newleave.start]] = newleave
        newchild.children = edge.children
        newleave.child = edge.children
        self.nodes.append(newnode)
        print "add new node", newnode
        if edge.linked_to != None:
            edge.linked_to.link = newnode
        if newleave.end == i+1:
            self.leaves.append(newleave) 
            print "add new leave", newleave
        if newchild.end == i+1:
            self.leaves.append(newchild)
            print "add new leave", newchild
        else:
            self.nodes.append(newchild)
            print "add new node", newchild
        if edge in self.nodes:
            for i,node in enumerate(self.nodes):
                if node is edge:
                    self.nodes.pop(i)
                    print edge, "removed"
                    break
        else:
            for leavei in xrange(len(self.leaves)):
                if self.leaves[leavei] is edge:
                    self.leaves.pop(leavei)
                    print edge, "removed"
                    break

        print "nodes post",self.nodes
        print "leaves post",self.leaves
        self.linkMaker(newnode)
        print self, self.ap

        
        
    def __str__(self):
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

    def __repr__(self, num):
        self.dot.node(str(self.nodes.index(self.root)) + "node","root")
        for node in self.leaves:
            self.dot.node(str(self.leaves.index(node))+"leave", label = str((node.start,node.end)),style="filled",color='blue', shape='circle',width = '0.07', height = '0.07',fontsize = '10')
        for node in self.nodes:
            if node != self.root:
                self.dot.node(str(self.nodes.index(node)) + "node", label = str((node.start,node.end)),style="filled",color='red', shape='circle', width = '0.07',height='0.07', fontsize = '10')
            if node.link != None:
                self.dot.edge(str(self.nodes.index(node)) + "node", str(self.nodes.index(node.link)) + "node", '' ,weigh = '1', arrowsize="0.4",fontsize = "10", style = 'dotted')

        stack = [self.root]
        while stack != []:
            cur = stack.pop()
            print cur.children.values()
            for child in cur.children.values():
                if child in self.nodes:
                    self.dot.edge(str(self.nodes.index(cur)) + "node", str(self.nodes.index(child)) + "node",self.s[child.start:child.end],weigh = '1', arrowsize="0.4",fontsize = "10")
                else:

                    self.dot.edge(str(self.nodes.index(cur)) + "node", str(self.leaves.index(child)) + "leave",self.s[child.start:child.end],weigh = '1', arrowsize="0.4",fontsize = "10")
                stack.append(child)

        self.dot.render('out_%s.txt' % num, view=True)
        return ''

f = open("suff.txt",'r')
s = f.readline()
s = "asdfasfasdfasdasdfsdsf"
a = SuffixTree(s,20)
f.close()
