### INPUT: LIST OF CLIQUES FROM BRON-KERBOSCH ALGORITHM
### OUTPUT: LIST OF MOTIFS FOR EACH CLIQUE

import re
import time
import random
#from BA1I import Neighbors, HammingDistance, FirstSymbol, Suffix, PatternToNumber, Quotient, Remainder, NumberToPattern
#from BA1H import *
#EMBEDDED_MOTIFS = ['AGG', 'ACC', 'ACCCCA','ATTT','ATTTA', 'AGTTTA']

def Suffix(Pattern):

    return Pattern[1:]
def FirstSymbol(Pattern):
    return Pattern[0]
def Neighbors(Pattern, d):

    shortest_neighbors = ['A', 'C', 'G', 'T']

    if d == 0:
        return [Pattern]

    if len(Pattern) == 1:
        return shortest_neighbors

    Neighborhood = []
    for neighbor in Neighbors(Suffix(Pattern), d):
        if HammingDistance(Suffix(Pattern), neighbor) < d:
            for x in shortest_neighbors:
                concat = x + neighbor
                Neighborhood.append(concat)
        else:
            concat_FirstSymbol = FirstSymbol(Pattern)+neighbor
            Neighborhood.append(concat_FirstSymbol)
    return Neighborhood
def PatternToNumber(Pattern):

    SymbolToNumber = {'A':0, 'C':1, 'G':2, 'T':3} #make dict mapping nucleotides to numbers

    if Pattern == '':
        return 0
    else:

        symbol = Pattern[-1] #final nucleotide of Pattern
        Prefix = Pattern[:-1]

    return 4 * PatternToNumber(Prefix) + SymbolToNumber[symbol]
def Quotient(index, k):
    return index//k
def Remainder(index, k):
    return index%k
def NumberToPattern(index, k):

    NumberToSymbol = {0:'A', 1:'C', 2:'G', 3:'T'} #make dict mapping numbers to nucleotides

    if k == 1:
        return NumberToSymbol[index]
    prefixIndex = Quotient(index, 4)
    r = Remainder(index, 4)
    symbol = NumberToSymbol[r]
    PrefixPattern = NumberToPattern(prefixIndex, k-1)
    PrefixPattern = NumberToPattern(prefixIndex, k-1)
    return PrefixPattern + symbol
def HammingDistance(Pattern, Text):

    count = 0

    for i in range(len(Pattern)):
        if Pattern[i] != Text[i]:
            count += 1
    return count
def ApproximateOccurrences(Pattern, Text, d):

    approxoccur = []

    for i in range(len(Text) - len(Pattern) + 1):
        if HammingDistance(Pattern, Text[i:i+len(Pattern)]) <= d:
            Text[i:i+len(Pattern)] == Pattern
            approxoccur.append(str(i))
    return approxoccur
def ApproxPatternCount(Text, Pattern, d):
    count = 0
    for i in range(len(Text) - len(Pattern) + 1):
        if HammingDistance(Pattern, Text[i:i+len(Pattern)]) <= d:
            count += 1
    return count

def MotifEnumeration(clique, k, d):

    temp_lst = []
    patternprime_lst = []
    for i in range(0, len(clique)-k+1):
        #sub = clique[i]
        sub = clique[i:i+k]
        # for text in range(len(sub) - k + 1):
        #     pattern = sub[text:text+k]
        #neighborhood = Neighbors(pattern, d)
        neighborhood = Neighbors(sub, d)
        for j in range(len(neighborhood)):
            if neighborhood[j] not in patternprime_lst:
                patternprime_lst.append(neighborhood[j])

    for j in range(0, len(clique)):
        if clique[j:j+k] in patternprime_lst:
            temp_lst.append(clique[j:j+k])

    return list(set(temp_lst))

def main(filename, outputFile, k):
    with open(CLIQUES_FILE) as f:
        all = f.readlines()
        all = [x.strip('\n') for x in all]

    #k = random.randint(3,10)

    #k = 3
    d = 0
    clique = ''.join(all)
    lst_motifs = MotifEnumeration(clique, k, d)
    lst_motifs
    # enumerate common motifs across all cliques
    # for i in range(len(all)):
    #     line = all[i]
    #     #clique = re.split(',', line)
    #     lst_motifs = MotifEnumeration(clique, k, d)

    # calculate AT:GC ratio of lst_motifs
    count_A = 0
    count_T = 0
    count_G = 0
    count_C = 0
    ratio = 0
    sum_ratio = 0
    if lst_motifs != []:
        for motif in lst_motifs:
            for nuc in motif:
                if nuc == 'A':
                    count_A +=1
                elif nuc == 'T':
                    count_T +=1
                elif nuc == 'G':
                    count_G +=1
                elif nuc == 'C':
                    count_C +=1
            count_CG = count_C + count_G
            count_CG
            count_AT = count_A + count_T
            count_AT
            if count_CG != 0:
                ratio = (count_AT)/(count_CG)
            # if count_AT != 0:
            #      ratio = (count_CG)/(count_AT)

            if count_CG == 0 and count_AT >= 1:
                ratio = 1
            # if count_AT == 0 and count_CG >= 1:
            #     ratio = 1
            sum_ratio += ratio
        if len(lst_motifs) >= 1:
            avg_ratio = sum_ratio/len(lst_motifs)
            print ("AT:GC ratio of k-mer length "+str(k)+" is "+str(round(ratio,2)))

    # remove empty lists in lst_motifs
    # with open(outputFile, "w") as outF:
    #     if lst_motifs != []:
    #         outF.write(",".join(x for x in lst_motifs))
    # with open(outputFile, "r") as outF:
    #     motifs = outF.readlines()

HAPPYORSAD = "ALL"
CLIQUES_FILE = "../data/sim_data_" + HAPPYORSAD + "_CLIQUES2.cliques"
OUTPUT_FILE = "../data/output_motifs.lstmotifs"
for k in range(3,8):
    main(CLIQUES_FILE, OUTPUT_FILE, k)
