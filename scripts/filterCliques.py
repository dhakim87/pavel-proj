def filterByCount(inputFile, outputFile, minCount):
    with open(inputFile) as f:
        all = f.readlines()

    with open(outputFile, "w") as f:
        for line in all:
            if len(line.split(",")) >= minCount:
                f.write(line);
                f.write("\n")

