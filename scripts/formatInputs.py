# formats the inputs for the produceGraph.py script

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
