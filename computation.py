from myFractions import *
import Tkinter, tkFileDialog
##def e_spigot():
##    
##    currentEst = fraction(1, 1) 
##    stop = -1
##    n = 6
##    while(True):
##        low = reduce(lambda a, b: 1+a*b, [fraction(2,1)]+[fraction(1,n-i) for i in range(n)]) 
##        high = reduce(lambda a, b: 1+a*b, [fraction(3,1)]+[fraction(1,n-i) for i in range(n)])
##        lowGen = low.estimate_generator()
##        highGen = high.estimate_generator()
##        nextLow = lowGen.next()
##        nextHigh = highGen.next()
##        i = 0
##        while(nextLow == nextHigh):
##            i+=1
##            if i > stop:
##                yield nextLow
##            nextLow = highGen.next()
##            nextHigh = lowGen.next()
##        stop = i
##        n+=6

def multiply2by2Matricies(A, B):
    """This performs matrix multiplication in only 7 multiplies."""
    ##Thank you the internet and Strassen...
    M_1 = (A[0][0]+A[1][1])*(B[0][0]+B[1][1])
    M_2 = (A[1][0]+A[1][1])*B[0][0]
    M_3 = A[0][0]*(B[0][1]-B[1][1])
    M_4 = A[1][1]*(B[1][0]-B[0][0])
    M_5 = (A[0][0]+A[0][1])*B[1][1]
    M_6 = (A[1][0]-A[0][0])*(B[0][0]+B[0][1])
    M_7 = (A[0][1]-A[1][1])*(B[1][0]+B[1][1])
    return [[M_1+M_4-M_5+M_7, M_3+M_5],
            [M_2+M_4        , M_1-M_2+M_3+M_6]]

def contFracConvergent(conFracGen, convergentIndex, starter = None):
        matrixArray = [[[conFracGen.next(), 1],
                        [1,                 0]] for j in range(convergentIndex+1)]
        if starter!=None:
            matrixArray= [starter]+matrixArray
        while(len(matrixArray)!=1):
            matrixArray = [multiply2by2Matricies(matrixArray[2*i], matrixArray[2*i+1]) for i in range(len(matrixArray)/2)]+[matrixArray[-1]]*(len(matrixArray)%2)
        return matrixArray[0], conFracGen

def ratAproxE(n):
    for j in range(n):
        matrixArray = [[[4*i+1, 2],
                        [2*i+1, 1]] for i in range(1, n+1)]
        while(len(matrixArray)!=1):
            matrixArray = [multiply2by2Matricies(matrixArray[2*i], matrixArray[2*i+1]) for i in range(len(matrixArray)/2)]+[matrixArray[-1]]*(len(matrixArray)%2)
        return matrixArray[0]

    return h, k
def contFracSpigot(conFracGen, blockSize = 1):
    """contFracSpigot(contFracGen) -> digit generator
This uses Wallis' Algorithm to estimate the value
from normalized continued fraction form. That is, at step n,
[a_n 1][h_n-1 k_n-1] = [h_n]
[1   0][h_n-2 k_n-2]   [k_n]
where h_n/k_n converges to the continued fraction value."""
    conGen = conFracGen
    h = [1, 0]
    k = [0, 1]
    i = 0##current decimal
    cycles = 200
    expandCycles = True
    pastDecimal = False
    for j in range(cycles):
        nextGen = conGen.next()
        h = [nextGen*h[0]+h[1], h[0]]
        k = [nextGen*k[0]+k[1], k[0]]
    while(True):
        try:
            test = range(cycles)
        except MemoryError:
            cycles-=blockSize+200
            expandCycles = False
        for j in range(cycles):
            nextGen = conGen.next()
            h = [nextGen*h[0]+h[1], h[0]]
            k = [nextGen*k[0]+k[1], k[0]]
        error = fraction(1, k[0]*k[1])
        ###est1 and est2 will always bound any further values.
        est1 = fraction(h[1], k[1])
        est2 = fraction(h[0], k[0])
        Gen1 = est1.estimate_generator(i, blockSize)
        Gen2 = est2.estimate_generator(i, blockSize)
        next1 = Gen1.next()
        next2 = Gen2.next()
        while(next1 == next2):
            if not pastDecimal:
                pastDecimal = True
                next1 = Gen1.next()
                next2 = Gen2.next()
                break
            yield next1
            next1 = Gen1.next()
            next2 = Gen2.next()
            if next1 == next2:
                i += blockSize
        if expandCycles:
            cycles+=200
        
def e_spigot(blockSize = 1):
    return contFracSpigot(e_continuedFrac(), blockSize)

def e_continuedFrac():
    ##e = [2:1,2,1,1,4,1,1,6,...]
    yield 2
    yield 1
    n = 2
    while(True):
        yield n
        yield 1
        yield 1
        n+=2

if __name__ == "__main__":
    howManyDigits = int(raw_input("How many digits (x1000)? : "))
    blockSize = 1000
    eSpigotGen = e_spigot(blockSize)
    root = Tkinter.Tk()
    try:
        outFile = tkFileDialog.asksaveasfile(title = "File To Print e To",\
                                             parent = root)
        if outFile != None:
            outFile.writelines(eSpigotGen.next()+"\n"\
                                for i in range(howManyDigits + 2))
    finally:
        if outFile != None:
            outFile.close()
        root.destroy()
        
