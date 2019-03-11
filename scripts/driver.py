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
import levenshtein
import filterCliques

HAPPYORSAD = "ALL"
CLIQUES_FILE = "../data/real_data_" + HAPPYORSAD + "_CLIQUES.cliques"
CLIQUES_FILE_FILTERED = "../data/" + HAPPYORSAD + "_filtered.txt"
FORMAT_INPUT_H =["../Real_Data/Fixed/Happy/Anaerotruncus_colihominis_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Dialister_invisus_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Escherichia_coli_FIXED.txt",
                 "../Real_Data/Fixed/Happy/FaeHaemophilus_parainfluenzae_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Faecalibacterium_prausnitzii_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Pasteurellaceae_bacterium_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Peptostreptococcaceae_bacterium_FIXED.txt",
                 "../Real_Data/Fixed/Happy/Ruminococcus_albus_FIXED.txt",
                 "../Real_Data/Fixed/Happy/uminococcus_bicirculans_FIXED.txt"]

FORMAT_INPUT_S = ["../Real_Data/Fixed/Sad/Alistipes_inops_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Clostridium_sporogenes_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Erysipelotrichaceae_bacterium_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Flavonifractor_plautii_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Hafnia_alvei_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Klebsiella_pneumoniae_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Mucinivorans_hirudinis_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Parabacteroides_distasonis_FIXED.txt",
                  "../Real_Data/Fixed/Sad/Porphyromonadaceae_bacterium_FIXED.txt"]

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
    genes = list()
    
    fileIndex = 0  #TODO FIXME HACK:  Pass metadata with each gene through the system.
    for filename in FORMAT_INPUT_H:
        file = open(filename, 'r')
        # takes each line and adds a happy tag
        for line in file:
            genes.append(line[:-1] + ", H")

    for filename in FORMAT_INPUT_S:
        # adds the tags for the sad file.
        file = open(filename, 'r')
        # takes each line and adds a sad tag
        for line in file:
            genes.append(line[:-1] + ", S")

    # outputs to a new file with newlines
    file2 = open("../data/output_tagged.txt", 'w')

    for line in genes:
        file2.write(line + "\n")

### produceGraph
def runProduceGraph():
    produceGraph.main("../data/output_tagged.txt", "../data/sim_data.graph", 20)

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

def runFilterCliques():
    filterCliques.filterByCount(CLIQUES_FILE, CLIQUES_FILE_FILTERED, 12)

def main():
    print("Simulator");
    runNucSimul();
    print("Format inputs");
    runFormatInputs();
    print("making Graph");
    runProduceGraph();
    print("Bron Kerbosching");
    runBronKerbosch();
    print("Searching for motifs");
    runMotifSearch();
    print("Filtering cliques by size");
    runFilterCliques();
    pass;

main()
