# Vatsal Vinod Rathod
# student-id:801259046
# Graph.py
# Computes 'Shortest Path','Reachable Nodes'.
# Executes 'Add edge','delete edge', 'edge down', 'edge up', 'vertex down' and 'vertex up'.
# Prints connected nodes and their weights in the graph

import sys
import heapq
from collections import deque

#  Represents a vertex in the graph.
class Vertex:
    def __init__(self, nm):
        self.name = nm    #  Vertex name
        self.adj =  []    #  Adjacent vertices
        self.status = 1   #  status of the vertex

    def Vertex(self, nm):
        self.name = nm
        adj = []

# Graph class: evaluate shortest paths and reachable.

class Graph:
    def __init__(self):
        self.vertexMap =  dict()

    # Add a new edge to the graph via .txt file.
    def addEdge(self, sourceName,  destName, weight):
        v = self.getVertex(sourceName)
        w = self.getVertex(destName)
        v.adj.append([w, weight,'up'])
        w.adj.append([v,weight,'up'])
    
    # Add a new edge to the graph via query
    def addEdge_func(self, sourceName,  destName, weight):
        v = self.getVertex(sourceName)
        w = self.getVertex(destName)
        for i in range(len(v.adj)):
            if(v.adj[i][0]==w):
                cost = v.adj[i][1]
                break
        v.adj.pop(i)
        v.adj.append([w, weight,'up'])

    # deletes edge form the mentoned source node to destination node
    def deleteedge(self, sourcename, destname):
        v=self.getVertex(sourcename)
        w=self.getVertex(destname)
        for i in range(len(v.adj)):
            if(v.adj[i][0]==w):
                break
        v.adj.pop(i)
        
    # updates edge status as down for the source and destination vertex
    def edgedown(self, sourcename,destname):
        v=self.getVertex(sourcename)
        w=self.getVertex(destname)
        for i in range(len(v.adj)):
            if(v.adj[i][0]==w):
                v.adj[i][2]='down'
    
    # updates edge status as up for the source and destination vertex
    def edgeup(self, sourcename,destname):
        v=self.getVertex(sourcename)
        w=self.getVertex(destname)
        for i in range(len(v.adj)):
            if(v.adj[i][0]==w):
                v.adj[i][2]='up' 
    # updates vertex status to down
    def vertexdown(self, sourcename):
        v=self.getVertex(sourcename)
        v.status = 0
    
    # updates vertex status to up
    def vertexup(self, sourcename):
        v=self.getVertex(sourcename)
        v.status = 1

    # below functions are to print the node and their edges with weight
    # printvertexmap iterates over each node
    # printvertex iterates over each node in adjacency list 
    def printvertexmap(self):
        v=dict(sorted(self.vertexMap.items(), key=lambda item: item[1].name))
        for i in v:
            k=self.vertexMap[i]
            if (k.status == 0):
                print(i+" DOWN")
            else:
                print(i)
            self.printvertex(i)

    def printvertex(self, sourcename):
        v=self.getVertex(sourcename)
        v.adj.sort(key = lambda x:x[0].name)
        for i in range(len(v.adj)):
            if (v.adj[i][2] == "down"):
                print(" "+v.adj[i][0].name+ " "+ v.adj[i][1] +" DOWN")
            else:
                print(" "+v.adj[i][0].name+ " "+ v.adj[i][1])

    # If vertexName is not present, add it to vertexMap.
    # In either case, return the Vertex.
    def  getVertex(self, vertexName):
        if vertexName not in self.vertexMap:
            v = Vertex(vertexName)
            self.vertexMap[vertexName] = v
        v = self.vertexMap[vertexName]
        return  v
    
    #dijkstras implementation
    #using printPath_ to print the shortest route and distance between 2 vertex
    def dijkstras(self,sourcename, destname):
        start = self.vertexMap[sourcename]
        if start is None:
            print("Start vertex not found")
        distance = {v : float('inf')  for v in self.vertexMap}
        parent = {v : 'nil' for v in self.vertexMap}
        distance[sourcename]=0
        priorityq = [(0,sourcename)]
        while(len(priorityq)!=0):
            currmin = priorityq[0][0]
            currentnode = priorityq[0][1]
            heapq.heappop(priorityq)
            v = self.getVertex(currentnode) 
            for adjacentnode, weight, status in v.adj : 
                if distance[adjacentnode.name]> float(weight)+float(currmin) and status == 'up' and adjacentnode.status==1 : 
                    distance[adjacentnode.name] = float(currmin) + float(weight)
                    parent[adjacentnode.name] = currentnode
                    heapq.heappush(priorityq,(distance[adjacentnode.name],adjacentnode.name))
        self.printPath_(parent,destname)
        print(" " + str(round(distance[destname],2))) 
    
    def printPath_(self, parent,dest):
        if parent[dest]!='nil':
           self.printPath_(parent, parent[dest])
           print(" ", end ="")
        print(dest,end ="")
    
    # Iterating over each node
    # BFS function prints all the reachable nodes
    def BFSvertex(self):
        v=dict(sorted(self.vertexMap.items(), key=lambda item: item[1].name))
        for i in v:
            k=self.vertexMap[i]
            if (k.status==1):
                print(i)
                self.BFS(i)
    
    def BFS(self,sourcename):
        distance = {v : float('inf')  for v in self.vertexMap}
        parent = {v : 'nil' for v in self.vertexMap}
        colour = {v : 'white' for v in self.vertexMap}
        colour[sourcename] = 'gray'
        q=deque()
        q.append(sourcename)
        while(len(q)!=0):
            curr = q[0]
            q.popleft()
            v = self.getVertex(curr)
            for adjacentnode, weight, status in v.adj : 
                if(colour[adjacentnode.name]=='white' and adjacentnode.status==1 and status == 'up'):
                    colour[adjacentnode.name]='gray'
                    parent[adjacentnode.name] = curr
                    q.append(adjacentnode.name)
            if curr!=sourcename:
                print(" "+curr)

# A main routine that:
# 1. Reads a file containing edges (supplied as a command-line parameter);
# 2. Forms the graph;
# 3. Waits for new query and calls the function as mentioned;

def main():
    g = Graph()
    fin = sys.argv[1]
    with open(fin) as f:
        lines = f.readlines()
    #  Read the edges and insert
    for line in lines:
        line = line.strip().split(" ")
        if (len(line) != 3):
            print("Skipping ill-formatted line " + line)
            continue
        source = line[0]
        dest = line[1]
        weight = line[2]
        g.addEdge(source, dest, weight)
    print("File read...")
    print(str(len(g.vertexMap)) + " vertices")
    quit=1
    while quit==1:
        try:
            cin = input().split()
            if(cin[0] == 'addedge'):
                g.addEdge_func(cin[1],cin[2],cin[3])
                
            elif(cin[0] == 'deleteedge'):
                g.deleteedge(cin[1],cin[2])
                
            elif(cin[0] == 'edgedown'):
                g.edgedown(cin[1],cin[2])

            elif(cin[0] == 'edgeup'):
                g.edgeup(cin[1],cin[2])

            elif(cin[0] == 'vertexdown'):
                g.vertexdown(cin[1])

            elif(cin[0] == 'vertexup'):
                g.vertexup(cin[1])

            elif(cin[0] == 'path'):
                g.dijkstras(cin[1],cin[2])

            elif(cin[0] == 'print'):
                g.printvertexmap()

            elif(cin[0] == 'reachable'):
                g.BFSvertex()

            elif(cin[0]=='quit'):
                quit=0

            else:
                print("invalid input")

        except IndexError:
            print("invalid number of inputs")
    

    

if __name__=="__main__":
    main()
