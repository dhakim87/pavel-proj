import levenshtein

class Node:
    def __init__(self, word):
        self.word = word
        self.children = {}

    def add(self, newWord):
        if self.word == newWord:
            print("Don't add the same word twice")
            return;
        editDist = levenshtein.compute(self.word, newWord)
        if editDist in self.children:
            self.children[editDist].add(newWord)
        else:
            self.children[editDist] = Node(newWord)

    def search(self, word, maxEditDist, outputList):
        #Use triangle inequality to restrict search
        editDist = levenshtein.compute(self.word, word)
        if editDist <= maxEditDist:
            outputList.append(self.word)

        minBound = editDist - maxEditDist
        maxBound = editDist + maxEditDist

        for child in self.children:
            if child >= minBound and child <= maxBound:
                self.children[child].search(word, maxEditDist, outputList)

class BKTree:
    def __init__(self):
        self.root = None;

    def add(self, word):
        if self.root is None:
            self.root = Node(word)
        else:
            self.root.add(word)

    def search(self, word, maxEditDist):
        outputList = []
        if self.root is None:
            return outputList
        self.root.search(word, maxEditDist, outputList)
        return outputList
