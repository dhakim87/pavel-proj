import os
import sys
import networkx as nx
import random
import re
from collections import defaultdict

import NucSimul
import produceGraph
import bronKerbosch
import MotifSearch

HAPPYORSAD = "HAPPY"
CLIQUES_FILE = "../data/sim_data_" + HAPPYORSAD + "_CLIQUES.cliques"

### NucSimul:
    # input: input.txt (parameters for nuc sim)
    # output: output_happy.txt, output_sad.txt
### formatInputs:
    # input: output_happy.txt, output_sad.txt
    # output: output_tagged.txt
### produceGraph:
    # input: output_tagged.txt
    # output: sim_data.Graph
### bronKerbosch:
    # input: sim_data.Graph
    # output: sim_data.cliques (3x)
### MotifSearch:
    # input: sim_data.cliques (3x)
    # output: list of motifs per clique

def runNucSimul():
    file = "../data/input.txt";
    NucSimul.Main(file)

### formats the inputs for the produceGraph.py script
def runFormatInputs():
    # adds the tags for the happy file
    file = open("output_happy.txt", 'r')
    genes = list()
    
    # takes each line and adds a happy tag
    for line in file:
        genes.append(line[:-1] + ", H")

    # adds the tags for the sad file.
    file = open("output_sad.txt", 'r')

    # takes each line and adds a sad tag
    for line in file:
        genes.append(line[:-1] + ", S")

    # outputs to a new file with newlines
    file2 = open("../data/output_tagged.txt", 'w')

    for line in genes:
        file2.write(line + "\n")

### produceGraph
def runProduceGraph():
    sequences = produceGraph.readData("../data/output_tagged.txt")
    graph = produceGraph.createGraph(sequences, K=20)
    input_for_bK = produceGraph.printGraph(sequences, graph, "../data/sim_data.graph")
    return input_for_bK

### produce cliques -- need to fix bronKerbosch code!!!
def runBronKerbosch():
    inputFile = "../data/sim_data.graph"
    outputFile = CLIQUES_FILE
    target = HAPPYORSAD
    F = .5
    bronKerbosch.main(inputFile, outputFile, target, F)

### produce motifs per clique, over all cliques
def runMotifSearch():
    MotifSearch.main(CLIQUES_FILE)

def main():
    runNucSimul();
    runFormatInputs();
    runProduceGraph();
    runBronKerbosch();
    runMotifSearch();
    pass;

main()
