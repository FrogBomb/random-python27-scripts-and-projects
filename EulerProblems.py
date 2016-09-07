import Useful_Algorithms
import copy
MaskDict = dict()
MaskDict[3] = { 1:(int('001', 2),),\
                    2:(int('001', 2),),\
                    3:(int('001', 2),)}
    
MaskDict[2] = {  1:(int('011', 2),int('010', 2)),\
                     2:(int('011', 2),int('010', 2)),\
                     3:(int('011', 2),)}

MaskDict[1] = {1:(int('111', 2), int('110', 2),\
                         int('101', 2), int('100', 2)),\
                   2:(int('111', 2), int('110', 2),\
                         int('101', 2)),\
                   3:(int('111', 2), int('101', 2))}

def unorderedSumCombo(n, degree):
    if degree == 1:
        yield (n,)
    elif degree == 2:
        if n == 0:
            yield (0, 0)
        else:
            for i in range(n+1):
                yield (i, n-i)
    else:
        for i in range(n+1):
            gen = unorderedSumCombo(i, degree - 1)
            for j in gen:
                yield j+ (n-i,)
                

@Useful_Algorithms.memo
def _euler416MaskHelper(fromTriple, toTriple):
    """Returns a dictionary with keys that are the product mask (OR) of
    possible mask combos, and with corresponding values that are the
    number of mask combos that go from fromTriple to toTriple that AND to
    the key."""
    if sum(i for i in fromTriple)!= sum(j for j in toTriple):
        raise ValueError("fromTriple and toTriple Must add to the same number")
    if all(i==0 for i in fromTriple):
        return {0:1}
    retDict = dict.fromkeys(range(8), 0)
    for i in range(3):
        for j in range(3):
            if fromTriple[i]!=0:
                if toTriple[j]!=0:
                    prevFromTriple = tuple(fromTriple[k]-(i==k) for k in range(3))
                    prevToTriple = tuple(toTriple[k]-(j==k) for k in range(3))
                    previousResult = _euler416MaskHelper(prevFromTriple,\
                                                        prevToTriple)
                    for mask in MaskDict[i+1][j+1]:
                        for prevPMask in previousResult:
                            retDict[mask|prevPMask] += previousResult[prevPMask]
    return retDict
    
        
    
def euler416(m, n, mod = 10**9):
    """A row of n squares contains a frog in the leftmost square.
By successive jumps the frog goes to the rightmost
square and then back to the leftmost square. On the outward trip
he jumps one, two or three squares to the right, and on the homeward
trip he jumps to the left in a similar manner. He cannot jump
outside the squares. He repeats the round-trip travel m times.

Let F(m, n) be the number of the ways the frog can travel
so that at most one square remains unvisited.
For example, F(1, 3) = 4, F(1, 4) = 15, F(1, 5) = 46,
F(2, 3) = 16 and F(2, 100) mod 109 = 429619151."""
    if n == 2:
        return 1
    if m == 1 and n == 3:
        return 4
    if n<2:
        raise ValueError("n must be greater than 2")
    ##Since the frog effectively could have traveled the same direction 2*m times
    ##instead of back and forth m times, we will just assume that.
    m = 2*m

    ##We will look at blocks of 6 at a time, shifting by 3 at each iteration:
    ##[1 |2 |3 |1`|2`|3`]
    ##We'll assume all the number of paths up to 1, 2, and 3 have been calculated.
    ##Then, we'll calculate the number of paths from each of these to 1`, 2`, and 3`
    ##(We say a path ends at one of these as soon as the frog would touch it)
    ##We can simultaniously calculate all trips by the use of "masks."
    ##on the first 3 tiles, representing what tiles the frog has been on.
    ##MaskDict[a][b] are the masks of paths from a to b`.

    ##We then make a transition matrix, counting the number of ways a fromTriple
    ##goes to a toTriple, and if one was missed before and after the transition.
    ##If one was missed before and through the transition, then we have 0 in the
    ##matrix at that location.
    sumTotalsFrom = unorderedSumCombo(m, 3)
    transMatrix = dict()
    ElementList = []
    CompoundElementList = []
    for fromTriple in sumTotalsFrom:
        sumTotalsTo = unorderedSumCombo(m, 3)
        for toTriple in sumTotalsTo:
            maskCounts = _euler416MaskHelper(fromTriple, toTriple)
            missOneCounts = sum(maskCounts[i] for i in [6, 5, 3])%mod
            getAllCounts = maskCounts[7]%mod
            transMatrix[((False,)+fromTriple, (False,)+toTriple)] = getAllCounts
            transMatrix[((True,)+fromTriple, (True,)+toTriple)] = getAllCounts
            transMatrix[((False,)+fromTriple, (True,)+toTriple)] = missOneCounts
        ElementList.append((True,)+fromTriple)
        ElementList.append((False,)+fromTriple)

    power = (n-2)/3 + 1
    startIndex = 2-((n+1)%3)
    powerBin = bin(power)
    SquaredTransDict = copy.deepcopy(transMatrix) ##I will square this repeatedly
    ptr = 1
    PowTransDict = dict()
    for key in ElementList:
        PowTransDict[(key, key)] = 1
    while(powerBin[-ptr] != 'b'):
        if(powerBin[-ptr] == '1'):
            newPowDict = dict()
            for keyA in ElementList:
                for keyB in ElementList:
                    accu = 0
                    for k in ElementList:
                        if SquaredTransDict.has_key((keyA, k)) and PowTransDict.has_key((k, keyB)):
                            accu += SquaredTransDict[keyA,k]*PowTransDict[k,keyB]
                    accu %= mod
                    if accu!=0:
                        newPowDict[keyA,keyB] = accu
            PowTransDict = newPowDict
        newSquaredDict = dict()
        for keyA in ElementList:
            for keyB in ElementList:
                accu = 0
                for k in ElementList:
                    if SquaredTransDict.has_key((keyA, k)) and SquaredTransDict.has_key((k, keyB)):
                        accu += SquaredTransDict[keyA,k]*SquaredTransDict[k,keyB]
                accu %= mod
                if accu != 0:
                    newSquaredDict[keyA,keyB] = accu
        SquaredTransDict = newSquaredDict
        ptr = ptr + 1

    fromStart = [0, 0, 0]
    fromStart[startIndex] = m
    fromStart = (False, ) + tuple(fromStart)
    toEnd1 = (True, m, 0, 0)
    toEnd2 = (False, m, 0, 0)
    return PowTransDict
