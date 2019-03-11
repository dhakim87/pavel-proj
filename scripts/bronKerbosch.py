from collections import defaultdict
import sys
#input .graph
#output .cliques

class Node:
    def __init__(self, id, sequence, happysad):
        self.id = id
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

def getConnectedComponents(allNodes):
    visited = set([])
    
    connectedSets = []
    toVisit = []
    for n in allNodes:
        if n.id in visited:
            continue
        connectedSet = set([])
        toVisit.append(n)
        while len(toVisit) > 0:
            curNode = toVisit.pop()
            if curNode.id in visited:
                continue
            visited.add(curNode.id)
            connectedSet.add(curNode)
            for e in curNode.edges:
                toVisit.append(e)
        connectedSets.append(connectedSet)
    return connectedSets

def main(inputFile, outputFile, target, F):
    cliqueSizes = []
    with open(inputFile) as f:
        data = f.read().splitlines()
        print("Num Genes: " + str(len(data)))
        delimeter = data.index("---")
        
        nodeGen = 0
        nodes = []
        for x in data[:delimeter]:
            ab = x.split(", ")
            nodes.append(Node(nodeGen, ab[0], ab[1]))
            nodeGen += 1
        
        nodeMap = {}
        for n in nodes:
            nodeMap[n.sequence] = n
        
        edges = [(x.split(", ")[0], x.split(", ")[1]) for x in data[delimeter+1:]]
        
        for e in edges:
            n1 = nodeMap[e[0]]
            n2 = nodeMap[e[1]]
            #TODO Check that adam is sending nodes in both directions.
            n1.addEdge(n2)
            n2.addEdge(n1)
            if abs(len(n1.sequence) - len(n2.sequence)) > 20:
                print("WTF");
    
        connectedComponents = getConnectedComponents(nodes)
        componentSizeCounts = defaultdict(int)
        for comp in connectedComponents:
            componentSizeCounts[len(comp)] += 1
    
        print("Number Of Connected Components: " + str(len(connectedComponents)))
        print("Connected Component Size Distribution: ")
        for size in sorted(list(componentSizeCounts)):
            print("\tSize: " + str(size) + " Count: " + str(componentSizeCounts[size]))


        results = []
        for component in connectedComponents:
            R = set([])
            P = component
            X = set([])
            BronKerbosch(R, P, X, results)

    with open(outputFile, "w") as outF:
        for r in results:
            numHappy = 0
            numSad = 0
            for n in r:
                if n.happysad == "H":
                    numHappy += 1
                if n.happysad == "S":
                    numSad += 1
            if numHappy + numSad >= 4:
                print("Clique Size: " + str(numHappy + numSad) + " Happy: " + str(numHappy) + " Sad: " + str(numSad));
                print("Representative Sequences:")
                for n in r:
                    print(n.sequence[30:60])
            if target == "HAPPY":
                if numHappy / (numHappy + numSad) >= F:
                    outF.write(",".join(x.sequence for x in r))
                    cliqueSizes.append(len(r))
            if target == "SAD":
                if numSad / (numHappy + numSad) >= F:
                    outF.write(",".join(x.sequence for x in r))
                    cliqueSizes.append(len(r))
            if target == "ALL":
                outF.write(",".join(x.sequence for x in r))
                cliqueSizes.append(len(r))

    print("Num Cliques: " + str(len(cliqueSizes)));
    cliqueSizes.sort()
    median = cliqueSizes[len(cliqueSizes)//2];
    print("Median Clique Size: " + str(median));
    print("Mean clique size: " + str(sum(cliqueSizes)/len(cliqueSizes)));
    print("Max clique size: " + str(max(cliqueSizes)))

#----------------------------------------------------------------
#if (len(sys.argv) == 1):
#    print("Usage: ")
#    print("python " + sys.argv[0] + " <pathToInput.graph> <target> <F Ratio>")
#    print("Ex: python " + sys.argv[0] + " ../data/test.graph HAPPY .8")
#    print("Ex: python " + sys.argv[0] + " ../data/test.graph SAD .8")
#    print("Ex: python " + sys.argv[0] + " ../data/test.graph ALL")
#else:
#    inputFile = sys.argv[1]
#    target = sys.argv[2]
#    F = None
#    if target != "ALL":
#        F = float(sys.argv[3])
#
#    main(inputFile, target, F)
