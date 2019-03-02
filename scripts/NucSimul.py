# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import random

def GenerateSequences(alphabet, probabilities, size, count):
    out = []    
    for i in range(count):
        out.append("".join(random.choices(population = alphabet, weights = probabilities, k = size))   )
    return out

def SeqAnalysis (seq_str):
    out = ""   
    out += "A:" + str(seq_str.count("A")) + ", "
    out += "C:" + str(seq_str.count("C")) + ", "
    out += "G:" + str(seq_str.count("G")) + ", "
    out += "T:" + str(seq_str.count("T"))
    return out


#open input file and read content into array
input_file = open("input.txt", "r")
lines = input_file.readlines()
prA = float((lines[0]))
prC = float((lines[1]))
prG = float((lines[2]))
prT = float((lines[3]))
length_hap = int((lines[4]))
count_hap = int((lines[5]))

prAs = float((lines[6]))
prCs = float((lines[7]))
prGs = float((lines[8]))
prTs = float((lines[9]))
length_sad = int((lines[10]))
count_sad = int((lines[11]))
 
try:
    motifs_hap = (lines[12][:-1]).split(",")
    motifs_hap_prob = [float(x) for x in (lines[13]).split(",")]
    motifs_sad = (lines[14][:-1]).split(",")
    motifs_sad_prob = [float(x) for x in (lines[15]).split(",")]
    alphabet_hap = ["A", "C", "G", "T"] + motifs_hap
    prop_hap = [prA, prC, prG, prT] + motifs_hap_prob
    output_happy = GenerateSequences(alphabet_hap, prop_hap, length_hap, count_hap)
    alphabet_sad = ["A", "C", "G", "T"] + motifs_sad
    prob_sad = [prA, prC, prG, prT] + motifs_sad_prob
    output_sad = GenerateSequences(alphabet_sad, prob_sad, length_sad, count_sad)    

except:
    alphabet = ["A", "C", "G", "T"]
    prop_hap = [prA, prC, prG, prT]
    output_happy = GenerateSequences(alphabet, prop_hap, length_hap, count_hap)
    prob_sad = [prAs, prCs, prGs, prTs]
    output_sad = GenerateSequences(alphabet, prob_sad, length_sad, count_sad)

str_hap = ""
for seq in output_happy:
    str_hap +=seq + "\n"

str_sad = ""
for seq in output_sad:
    str_sad +=seq + "\n"

#sequence char analysis
out_analytics ="happy sequences" + "\n"

for h1 in output_happy:
    out_analytics += h1 + " {" + SeqAnalysis(h1) + "} " + "\n"

out_analytics +="sad sequences" + "\n"
for h2 in output_sad:
    out_analytics += h2 + " {" + SeqAnalysis(h2) + "} " + "\n"

#write output to file
output_file_hap = open("output_happy.txt", "w")
output_file_hap.write(str_hap)
output_file_sad = open("output_sad.txt", "w")
output_file_sad.write(str_sad)
output_file_analytics = open("output_analytics.txt", "w")
output_file_analytics.write(out_analytics)

#close input and output files when done
input_file.close()
output_file_hap.close()
output_file_sad.close()
output_file_analytics.close()
