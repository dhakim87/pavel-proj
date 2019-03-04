from collections import defaultdict
import sys
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

def BronKerbosch(R, P, X, results):
    if len(P) == 0 and len(X) == 0:
        results.append(R)
    for v in list(P):
        BronKerbosch(union(R, setof(v)), intersect(P, neighbors(v)), intersect(X, neighbors(v)), results)
        P = difference(P, setof(v))
        X = union(X, setof(v))

def neighbors(n):
    neigh = set([])
    for nn in n.edges:
        neigh.add(nn)
    return neigh;

def main(inputFile, target, F):
    with open(inputFile) as f:
        data = f.read().splitlines()
        delimeter = data.index("---")
        
        nodes = [Node(x.split(", ")[0], x.split(", ")[1]) for x in data[:delimeter]]
        nodeMap = {}
        for n in nodes:
            nodeMap[n.sequence] = n
        
        edges = [(x.split(", ")[0], x.split(", ")[1]) for x in data[delimeter+1:]]
        
        for e in edges:
            nodeMap[e[0]].addEdge(nodeMap[e[1]]) #TODO Check that adam is sending nodes in both directions.
        
        R = set([])
        P = set(nodes)
        X = set([])

        results = []
        BronKerbosch(R, P, X, results)

        for r in results:
            numHappy = 0
            numSad = 0
            for n in r:
                if n.happysad == "H":
                    numHappy += 1
                if n.happysad == "S":
                    numSad += 1
            if target == "HAPPY":
                if numHappy / (numHappy + numSad) >= F:
                    print(",".join(x.sequence for x in r))
            if target == "SAD":
                if numSad / (numHappy + numSad) >= F:
                    print(",".join(x.sequence for x in r))
            if target == "ALL":
                print(",".join(x.sequence for x in r))

#----------------------------------------------------------------
if (len(sys.argv) == 1):
    print("Usage: ")
    print("python " + sys.argv[0] + " <pathToInput.graph> <target> <F Ratio>")
    print("Ex: python " + sys.argv[0] + " ../data/test.graph HAPPY .8")
    print("Ex: python " + sys.argv[0] + " ../data/test.graph SAD .8")
    print("Ex: python " + sys.argv[0] + " ../data/test.graph ALL")
else:
    inputFile = sys.argv[1]
    target = sys.argv[2]
    F = None
    if target != "ALL":
        F = float(sys.argv[3])

    main(inputFile, target, F)
