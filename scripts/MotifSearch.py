### INPUT: LIST OF CLIQUES FROM BRON-KERBOSCH ALGORITHM
### OUTPUT: LIST OF MOTIFS FOR EACH CLIQUE


import re

#from BA1I import Neighbors, HammingDistance, FirstSymbol, Suffix, PatternToNumber, Quotient, Remainder, NumberToPattern
#from BA1H import *

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
    for i in range(1, len(clique)):
        sub = clique[i]
        for text in range(len(sub) - k + 1):
            pattern = sub[text:text+k]
            neighborhood = Neighbors(pattern, d)
            for j in range(len(neighborhood)):
                if neighborhood[j] not in patternprime_lst:
                    patternprime_lst.append(neighborhood[j])

    for i in range(len(patternprime_lst)):
        sub = patternprime_lst[i]
        subinAll = True
        for j in range(1, len(clique)):
            if ApproxPatternCount(clique[j], sub, d) == 0:
                subinAll = False
                break
        if subinAll == True:
            temp_lst.append(sub)

    motifs = []
    for i in range(len(temp_lst)):
        if temp_lst[i] not in motifs:
            motifs.append(temp_lst[i])
    return motifs


def main():

    with open('Sample.cliques') as f:

    #f = open('cliques.txt','r')
        all = f.readlines()

        all = [x.strip('\n') for x in all]

    k = 6
    d = 2
    for i in range(len(all)):
        line = all[i]
        clique = re.split(',', line)
        print ('Clique {}: {}'.format(i+1, MotifEnumeration(clique, k, d)))


main()
