#Daniel Hakim
def compute(A, B, maxDist):
    w = len(A)
    h = len(B)

    if abs(w - h) >= maxDist + 1:
        return maxDist + 1

    #Initial row of the array
    row = []
    for x in range(w):
        row.append(x+1)
    for y in range(h):
        newRow = [0] * w
        minVal = maxDist + 1
        for x in range(w):
            indicator = (A[x] == B[y])
            if indicator:
                indicator = 0
            else:
                indicator = 1
        
            if x == 0:
                val = min((y+1) + 1, y + indicator, row[x] + 1)
            else:
                val = min(newRow[x-1] + 1, row[x-1] + indicator, row[x] + 1)
            newRow[x] = val
            minVal = min(minVal, val)

        if minVal > maxDist:
            return maxDist + 1
        row = newRow
    return row[-1]
