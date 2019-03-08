#input HF.txt, SF.txt
#output something.graph

import networkx as nx

def hammingDistance(p, q):
    dist = 0
    # loop through each char and see if they match
    for i in range(len(p)):
        if(p[i] != q[i]):
            dist += 1
            
    return dist

# finds the edit distance between two strings
def editDist(v, w):
    distance = 0
    backtrack, s = editAlign(v, w)
    newV, newW = outputEdit(backtrack, v, w)
    distance = hammingDistance(newV, newW)
    
    
    
    return distance


# global alignment for edit distance
def editAlign(v, w):
    
    # find the dimensions of the graph
    n = len(v)
    m = len(w)
    
    sigma = 1
    
    # initialize the backtrack matrix to be the correct size
    backtrack = list()
    s = list()
    # set up the grid for n+1 x m+1
    for i in range(0,n+1):
        backtrack.append(list())
        s.append(list())
        for j in range(0,m+1):
            backtrack[i].append(0)
            s[i].append(0)
    
    # set the first column to zeros.
    s[0][0] = 0
    for i in range(1,len(v)+1):
        s[i][0] = s[i-1][0]-sigma
        backtrack[i][0] = "|"
    
    # set the first row to zeros
    for j in range(1,len(w)+1):
        s[0][j] = s[0][j-1]-sigma
        backtrack[0][j] = "-"
        
    # go through each other element and determine the weight value (0 for an insertion or deletion, 1 for a match)
    for i in range(1,len(v)+1):
        for j in range(1,len(w)+1):
            
            if v[i-1] == w[j-1]:
                # the tile is the max of the predecessors plus the respective edges
                s[i][j] = max([s[i-1][j]-sigma, s[i][j-1]-sigma, s[i-1][j-1]])
            else:
                s[i][j] = max([s[i-1][j]-sigma, s[i][j-1]-sigma, s[i-1][j-1]-1])
            
            # figure out which path was taken and make backtrack have the correct symbols.
            if s[i][j]+sigma == s[i-1][j]:
                backtrack[i][j] = "|"
            elif s[i][j]+sigma == s[i][j-1]:
                backtrack[i][j] = "-"
            elif (s[i][j] == s[i-1][j-1] or s[i][j] == s[i-1][j-1]-1):
                backtrack[i][j] = "*"
                
    return backtrack, s[i][j]


def outputEdit(backtrack, v, w):
    
    i = len(v)
    j = len(w)
    alignedV = ""
    alignedW = ""
    
    # go through the matrix and navigate to the souce via longest path
    for idx in range(len(v)+len(w),0, -1):
        
        if backtrack[i][j] == "|":
            i = i-1
            alignedV += v[i]
            alignedW += "-"
        elif backtrack[i][j] == "-":
            j = j-1
            alignedV += "-"
            alignedW += w[j]
        elif backtrack[i][j] == "*":
            i = i-1
            j = j-1
            alignedV += v[i]
            alignedW += w[j]
        if (i == 0 and j == 0):
            break
            
    return alignedV[::-1], alignedW[::-1]

# parses the data into a list.
def readData(filename):

    sequences = {}
    file = open(filename, 'r')

    # append all lines without the newline to the sequences list.
    for line in file:

        seq, tag = line[:-1].split(", ")
        sequences[seq] = tag

    return sequences


# takes the data and creates a graph
def createGraph(sequences, K):

    seqGraph = nx.Graph()
    seqGraph.add_nodes_from(sequences.keys())

    # go through all sequences and find the pairwise distance.
    for seq in sequences:
        
        for pair in sequences:

            # skip itself
            if seq == pair:
                continue

            # otherwise determine if it's pairwise distance is less than K
            else:
                dist = editDist(seq, pair)
                if dist < K:
                    seqGraph.add_edge(seq, pair, weight=dist)
                else:
                    continue

    return seqGraph

# takes a graph and prints out a text file of the .graph format
# nodes first followed by their tag then the edges in start, end, weight format.
def printGraph(sequences, seqGraph, filename):

    f = open(filename, 'w')

    for node in seqGraph.nodes():
        delim = ", " + sequences[node]
        f.write(node + delim + "\n")
    f.write("---"+ "\n")
    for e in seqGraph.edges():
        f.write(e[0] + ", " + e[1]+ "\n")

    return

def main(inputFile, outputFile, k):
    sequences = readData(inputFile)
    graph = createGraph(sequences, K=k)
    printGraph(sequences, graph, outputFile)

#main("../data/output_tagged.txt", "../data/sim_data.graph", 20)
