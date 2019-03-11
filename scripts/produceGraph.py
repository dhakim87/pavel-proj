#input HF.txt, SF.txt
#output something.graph

import levenshtein
import networkx as nx
from collections import defaultdict
import bkTree

MIN_MATCH_LEN = 10

# finds the edit distance between two strings
def editDistLevenshtein(v, w, maxDist):
    #Heuristic: We assume the vast majority of the time, edit distance will be greater than max dist,
    #So for larger strings, we attempt to fail out early.
#    if len(v) > 4 * maxDist and len(w) > 4 * maxDist:
#        prefixDist = levenshtein.compute(v[:3 * maxDist], w[:3 * maxDist], maxDist)
#        if prefixDist > maxDist:
##            print("Early Breakout")
#            return prefixDist

    dist = levenshtein.compute(v,w,maxDist)
#    if dist == maxDist + 1:
#        print("Couldn't early break out :(")
    return dist

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
def addEdgesToGraph(seqGraph, sequences, K):

    # go through all sequences and find the pairwise distance.
    numSequences = len(sequences);
    numEdges = 0
    i = 0
    for seq in sequences:
        i += 1
        numEdges = 0
        for pair in sequences:
            # skip itself
            if seq >= pair:
                continue
            # otherwise determine if it's pairwise distance is less than K
            else:
                dist = editDistLevenshtein(seq, pair, K)
                if dist <= K:
                    seqGraph.add_edge(seq, pair, weight=dist)
                    seqGraph.add_edge(pair, seq, weight=dist)
                    numEdges += 1
                else:
                    continue
        print(str(i) + " / " + str(numSequences) + " Neighbors: " + str(numEdges))

    return seqGraph

def getKmers(seq, kmerLen):
    kmers = []
    for j in range(kmerLen, len(seq) + 1):
        i = j - kmerLen
        kmers.append(seq[i:j])
    return kmers

def addEdgesToGraphWithHashing(seqGraph, seqList, prefixLen, K):
    #TODO FIXME HACK:  Can probably hash in a more biologically relevant way...  Maybe take first and second letters of codons and ignore third or something.

    #First, make a dictionary from kmer to list of sequence by writing the kmers of length 10 in the prefix of length X of each sequence to a dictionary.  We can tweak this by changing k, it should come out to prefix len divided by k + 1 is our kmer length.  We want a kmer length that is larger to prevent matching everyting all the time.

    matchmap = defaultdict(list)
    kmerLen = prefixLen // (K + 1)
    
    if kmerLen < MIN_MATCH_LEN:
        print("WARNING:genes too short to guarantee matches of length " +str(MIN_MATCH_LEN) +", we may lose real matches (but come on... are these really biologically relevant?)")
        kmerLen = MIN_MATCH_LEN;
    
    shortSeqs = []
    midLenSeqs = []
    longSeqs =  []
    
    for seq in seqList:
        if len(seq) < prefixLen - K:
            shortSeqs.append(seq)
        elif len(seq) < prefixLen:
            midLenSeqs.append(seq)
        else:
            longSeqs.append(seq)

    #Short seqs should be compared with other short seqs and with midLenSeqs
    #midLenSeqs should be compared with everything
    #longSeqs should be compared with other long seqs and with midLenSeqs.

    seqL = longSeqs
    
#    print("Making Match Map");
    for seqIndex in range(len(seqL)):
        seq = seqL[seqIndex]
        prefixSeq = seq[:min(prefixLen, len(seq))]
        for kmer in getKmers(prefixSeq, kmerLen):
            matchmap[kmer].append(seqIndex)
#    print("Match Map Created");

    for seqIndex in range(len(seqL)):
#        print(str(seqIndex));
        toCheck = set([])
        prefixSeq = seqL[seqIndex][:prefixLen]
        for kmer in getKmers(prefixSeq, kmerLen):
            for match in matchmap[kmer]:
                if match != toCheck:
                    toCheck.add(match)

#        print("Matches: " + str(len(toCheck)))
        # skip itself
        seq = seqL[seqIndex]
        for matchIndex in toCheck:
            pair = seqL[matchIndex]
            if seqIndex >= matchIndex:
                continue

            # otherwise determine if it's pairwise distance is less than K
            dist = editDistLevenshtein(seq, pair, K)
            if dist <= K:
                seqGraph.add_edge(seq, pair, weight=dist)
                seqGraph.add_edge(pair, seq, weight=dist)
            else:
                continue

#def createGraphWithBKTree(sequences, K):
#    seqGraph = nx.Graph();
#    seqGraph.add_nodes_from(sequences.keys())
#    
#    tree = bkTree.BKTree()
#    for seq in sequences:
#        tree.add(seq)
#    
#    for seq in sequences:
#        foundSequences = tree.search(seq, K)
#        for nearbySeq in foundSequences:
#            if nearbySeq == seq:
#                continue
#            seqGraph.add_edge(seq, nearbySeq, weight=1)
#            seqGraph.add_edge(nearbySeq, seq, weight=1)
#
#    return seqGraph

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

def main(inputFile, outputFile, k):
    sequences = readData(inputFile)
    
    seqGraph = nx.Graph()
    seqGraph.add_nodes_from(sequences.keys())
    
    seqList = list(sequences.keys());
    seqList.sort(key = len)
    
    if len(seqList) == 0:
        print("No Sequences, Failing out")
        return

    buckets = defaultdict(list) #0-k, k-2*k, 2*k-3*k ...
    for s in seqList:
        buckets[len(s) // k].append(s)

    for bucketIndex in sorted(buckets.keys()):
        bucketSeqs = buckets[bucketIndex] + buckets[bucketIndex+1]
        minLength = len(bucketSeqs[0])
        maxLength = len(bucketSeqs[-1])
        print("Processing " + str(minLength) + " to " + str(maxLength) + ", " + str(len(bucketSeqs)) + " Sequences ...")
        addEdgesToGraphWithHashing(seqGraph, bucketSeqs, minLength, K=k)
    printGraph(sequences, seqGraph, outputFile)

#main("../data/output_tagged.txt", "../data/sim_data.graph", 20)
