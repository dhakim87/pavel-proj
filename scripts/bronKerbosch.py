from collections import defaultdict

#input .graph
#output .cliques

class Node:
    def __init__(self, sequence, happysad):
        self.edges = set([])
        self.happysad = happysad
        self.sequence = sequence

    def addEdge(self, n):
        self.edges.add(n)

    def __str__(self):
        return self.sequence

    def __repr__(self):
        return "(" + self.sequence + "," + self.happysad + ")"

def union(setA, setB):
    return set(list(setA) + list(setB))

def setof(val):
    return set([val])

def difference(S, valSet):
    for v in valSet:
        S.remove(v)
    return S

def intersect(setA, setB):
    count = defaultdict(int)
    for val in setA:
        count[val] += 1
    for val in setB:
        count[val] += 1

    finalSet = []
    for key in count:
        if count[key] == 2:
            finalSet.append(key)
    return set(finalSet)

def BronKerbosch(R, P, X):
    if len(P) == 0 and len(X) == 0:
        print(R)
    for v in list(P):
        BronKerbosch(union(R, setof(v)), intersect(P, neighbors(v)), intersect(X, neighbors(v)))
        P = difference(P, setof(v))
        X = union(X, setof(v))

def neighbors(n):
    neigh = set([])
    for nn in n.edges:
        neigh.add(nn)
    return neigh;

with open("../data/Sample.graph") as f:
    data = f.read().splitlines()
    delimeter = data.index("---")
    
    nodes = [Node(x.split(", ")[0], x.split(", ")[1]) for i,x in data[:delimeter]]
    edges = [(int(x.split(" -> ")[0]), int(x.split(" -> ")[1])) for x in data[delimeter+1:]]
    
    for e in edges:
        nodes[e[0]].addEdge(nodes[e[1]]) #TODO Check that adam is sending nodes in both directions.
    
    R = set([])
    P = set(nodes)
    X = set([])

    BronKerbosch(R, P, X)
