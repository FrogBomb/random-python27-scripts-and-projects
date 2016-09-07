###############################
##~~Written by Tom Blanchet~~##
#~~~~~Written  2012-2016~~~~~~#
###############################
import itertools
import Tkinter
import math
import sys
import random
import time
from functools import wraps
import anydbm
import copy
from TomMatrix import *

ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890"
LOOKANDSAYELEDICT = {\
'H':	(['H'],	22),\
'He':	(['Hf', 'Pa', 'H', 'Ca', 'Li'],	13112221133211322112211213322112),\
'Li':	(['He'],	312211322212221121123222112),\
'Be':	(['Ge', 'Ca', 'Li'],	111312211312113221133211322112211213322112),\
'B':	(['Be'],	1321132122211322212221121123222112),\
'C':	(['B'],	3113112211322112211213322112),\
'N':	(['C'],	111312212221121123222112),\
'O':	(['N'],	132112211213322112),\
'F':	(['O'],	31121123222112),\
'Ne':	(['F'],	111213322112),\
'Na':	(['Ne'],	123222112),\
'Mg':	(['Pm', 'Na'],	3113322112),\
'Al':	(['Mg'],	1113222112),\
'Si':	(['Al'],	1322112),\
'P':	(['Ho', 'Si'],	311311222112),\
'S':	(['P'],	1113122112),\
'Cl':	(['S'],	132112),\
'Ar':	(['Cl'],	3112),\
'K':	(['Ar'],	1112),\
'Ca':	(['K'],	12),\
'Sc':	(['Ho', 'Pa', 'H', 'Ca', 'Co'],	3113112221133112),\
'Ti':	(['Sc'],	11131221131112),\
'V':	(['Ti'],	13211312),\
'Cr':	(['V'],	31132),\
'Mn':	(['Cr', 'Si'],	111311222112),\
'Fe':	(['Mn'],	13122112),\
'Co':	(['Fe'],	32112),\
'Ni':	(['Zn', 'Co'],	11133112),\
'Cu':	(['Ni'],	131112),\
'Zn':	(['Cu'],	312),\
'Ga':	(['Eu', 'Ca', 'Ac', 'H', 'Ca', 'Zn'],	13221133122211332),\
'Ge':	(['Ho', 'Ga'],	31131122211311122113222),\
'As':	(['Ge', 'Na'],	11131221131211322113322112),\
'Se':	(['As'],	13211321222113222112),\
'Br':	(['Se'],	3113112211322112),\
'Kr':	(['Br'],	11131221222112),\
'Rb':	(['Kr'],	1321122112),\
'Sr':	(['Rb'],	3112112),\
'Y':	(['Sr', 'U'],	1112133),\
'Zr':	(['Y', 'H', 'Ca', 'Tc'],	12322211331222113112211),\
'Nb':	(['Er', 'Zr'],	1113122113322113111221131221),\
'Mo':	(['Nb'],	13211322211312113211),\
'Tc':	(['Mo'],	311322113212221),\
'Ru':	(['Eu', 'Ca', 'Tc'],	132211331222113112211),\
'Rh':	(['Ho', 'Ru'],	311311222113111221131221),\
'Pd':	(['Rh'],	111312211312113211),\
'Ag':	(['Pd'],	132113212221),\
'Cd':	(['Ag'],	3113112211),\
'In':	(['Cd'],	11131221),\
'Sn':	(['In'],	13211),\
'Sb':	(['Pm', 'Sn'],	3112221),\
'Te':	(['Eu', 'Ca', 'Sb'],	1322113312211),\
'I':	(['Ho', 'Te'],	311311222113111221),\
'Xe':	(['I'],	11131221131211),\
'Cs':	(['Xe'],	13211321),\
'Ba':	(['Cs'],	311311),\
'La':	(['Ba'],	11131),\
'Ce':	(['La', 'H', 'Ca', 'Co'],	1321133112),\
'Pr':	(['Ce'],	31131112),\
'Nd':	(['Pr'],	111312),\
'Pm':	(['Nd'],	132),\
'Sm':	(['Pm', 'Ca', 'Zn'],	311332),\
'Eu':	(['Sm'],	1113222),\
'Gd':	(['Eu', 'Ca', 'Co'],	13221133112),\
'Tb':	(['Ho', 'Gd'],	3113112221131112),\
'Dy':	(['Tb'],	111312211312),\
'Ho':	(['Dy'],	1321132),\
'Er':	(['Ho', 'Pm'],	311311222),\
'Tm':	(['Er', 'Ca', 'Co'],	11131221133112),\
'Yb':	(['Tm'],	1321131112),\
'Lu':	(['Yb'],	311312),\
'Hf':	(['Lu'],	11132),\
'Ta':	(['Hf', 'Pa', 'H', 'Ca', 'W'],	13112221133211322112211213322113),\
'W':	(['Ta'],	312211322212221121123222113),\
'Re':	(['Ge', 'Ca', 'W'],	111312211312113221133211322112211213322113),\
'Os':	(['Re'],	1321132122211322212221121123222113),\
'Ir':	(['Os'],	3113112211322112211213322113),\
'Pt':	(['Ir'],	111312212221121123222113),\
'Au':	(['Pt'],	132112211213322113),\
'Hg':	(['Au'],	31121123222113),\
'Tl':	(['Hg'],	111213322113),\
'Pb':	(['Tl'],	123222113),\
'Bi':	(['Pm', 'Pb'],	3113322113),\
'Po':	(['Bi'],	1113222113),\
'At':	(['Po'],	1322113),\
'Rn':	(['Ho', 'At'],	311311222113),\
'Fr':	(['Rn'],	1113122113),\
'Ra':	(['Fr'],	132113),\
'Ac':	(['Ra'],	3113),\
'Th':	(['Ac'],	1113),\
'Pa':	(['Th'],	13),\
'U':	(['Pa'],	3)}

def timer(func, *args, **keywords):
    start = time.clock()
    retVal = func(*args, **keywords)
    stop = time.clock()
    return retVal, stop-start

def decTimer(func):
    def inTimer(*args, **keywords):
        start = time.clock()
        retVal = func(*args, **keywords)
        stop = time.clock()
        return retVal, stop-start
    return inTimer

def mod_exp(n, p, mod):
    """returns (n**p)%mod efficiently"""
    k = bin(p)
    n = n%mod
    if(n == 0):
    	return 0 		#exit
    ptr = 1
    ret = 1
    while(k[-ptr] != 'b'):
    	if(n == 1):
    		return ret 	#exit
    	if(k[-ptr] == '1'):
    		ret = (ret*n)%mod
    	n = (n**2)%mod
    	ptr = ptr + 1
    return ret 			#exit


def CRT(NList, ModList):
    """Solves the Chinese Remainder Theorem problem

    nList contains the values associated with the mods in modList.
    Returns the minimal solution [0] and then the solution modulus [1]."""

    nList= [i for i in NList]
    modList = [i for i in ModList]
    if len(nList) != len(modList):
        raise ValueError("Lists must be the same length")
    for i in modList:
        if i<2:
            raise ValueError("modList must only contain elements >= 2")
    if not isPWRPrime(*modList):
        NewN, NewMod = CRTforPair(nList[0], modList[0], nList[1], modList[1])
        return CRT([NewN] + nList[2:], [NewMod] + modList[2:])
    
    accModLProd = product(*modList) #product of everything in modList
    toSumList = (((nList[i])*(extended_euclid(
        accModLProd/modList[i], modList[i])[1])*(accModLProd/modList[i])) for i in range(len(modList)))
    #Will generate the mod inverses of accMLProd*n for each mod
    return sum(toSumList)%lcm(*modList), lcm(*modList)

def CRTforPair(N_1, Mod_1, N_2, Mod_2):
    if (N_1-N_2)%gcd(Mod_1, Mod_2)!=0:
        raise ValueError("There is no Solution!")
    if N_1%N_2==0:
        return N_1, Mod_1
    if N_2%N_1==0:
        return N_2, Mod_2
    TheLCM = lcm(Mod_1, Mod_2)
    TheGCD = gcd(Mod_1, Mod_2)
    k = N_1%TheGCD
    N_1 = (N_1-k)/TheGCD
    N_2 = (N_2-k)/TheGCD
    invMod1 = extended_euclid(Mod_1, Mod_2)[1]
    invMod2 = extended_euclid(Mod_2, Mod_1)[1]
    return (k+N_2*Mod_1*invMod1 + N_1*Mod_2*invMod2)%TheLCM, TheLCM

def product(*numList):
    """Returns the product of all the arguements."""
    if len(numList)==0:
        return 1
    ret = [n for n in numList]
    while(len(ret) != 1):
        iterList = (2*i for i in range((len(ret))/2))
        if len(ret)%2 == 0:
            ret = [ret[i]*ret[i+1] for i in iterList]
        else:
            temp = ret[-1]
            ret = [ret[i]*ret[i+1] for i in iterList]
            ret.append(temp)
    return ret[0]
    
def gcd_2(n, m):
    """finds the gcd of n and m"""
    if(n < m):##swaps n and m
        n ^= m
        m ^= n
        n ^= m
    while(m!=0):
        k = n%m
        n = m
        m = k
    return n

def innerProduct(listA, listB):
	return sum(vector(listA)*vector(listB))

def extended_euclid(n, m):
    """Finds the gcd [index 0] of n and m and (n**-1)mod m [index 1](if it exists).
        If no inverse, will find solution for a number which multiplies to the gcd'"""
    q_list = []
    n%=m
    ##value setup##
    if(n < m):##swaps n and m
        n ^= m
        m ^= n
        n ^= m
    ##value setup##
    while(m!=0):
        k = n%m
        q_list.append(n/m)
        n = m
        m = k
    invCommaMod = [0, 1]
    for q in q_list:
        invCommaMod = [invCommaMod[1], invCommaMod[0]+invCommaMod[1]*q]
    if(len(q_list)%2 == 1):
        return n, invCommaMod[0]
    return n, ((-invCommaMod[0])%invCommaMod[1])


def max_mod(n, inlist):
    """Returns k in inlist with the maximum value for n%k"""
    currMax = 0
    ret = inlist[0] #defaults to some item in inlist.
    for item in inlist:
        if currMax < n%item:
            currMax = n%item
            ret = item
    return ret

def gcd(*numList):
    """finds the gcd of a list of numbers"""
    currGcd = numList[0]
    i = 1
    while(i<len(numList)):
        currGcd = gcd_2(currGcd, numList[i])
        i += 1
    return currGcd

def isPWRPrime(*numList):
    """Are all the integers Pair Wise Reletively Prime?"""
    numPairs = itertools.combinations(numList, 2)
    return all(gcd_2(*pair) == 1 for pair in numPairs)

def lcm(*numList):
    """finds the lcm of a list of numbers"""
    currLcm = numList[0]
    i = 1
    while(i<len(numList)):
        currLcm = (currLcm*numList[i])/gcd_2(currLcm, numList[i])
        i += 1
    return currLcm

def BestCalls_huggy_bear(n, inlist):
    
    """www.contestcen.com/tough.htm
Provides the best calls (until reaching the min of inlist > 1) for
n people using the numbers to call in inlist. Call numbers are prioritized by
their order in inlist."""

    ret = []
    pops = [n]
    org_n = n
    checklist = inlist[:]
    inlist = inlist[:]
    while inlist.count(1)>0:
        inlist.remove(1)
    if lcm(*inlist)<=n:
        n %= lcm(*inlist)
        print "The game will not get past" , org_n-n, "people!"
        print "Solving instead for the fastest way to get to", org_n-n, "people."
    while(n > min(inlist)):
        for item in checklist:
            if (item >= n)&(item != min(checklist)):
                try:
                    inlist.remove(item)
                except ValueError:
                        pass
        mod = max_mod(n, inlist)
        ret.append(mod)
        n -= n%mod
        pops.append(n)
    return dict(bestCalls=ret, populations = pops, n=org_n, inlist=checklist)

def complexLog(value, base = math.e):
    """Computes the log of a complex number."""
    mag = (value*value.conjugate()).real**.5
    tan_theta = value.imag/value.real
    theta = math.atan(tan_theta)/math.log(base, math.e)
    return complex(math.log(mag, base), theta)


def solvePolynomial(coeffs, confidence=0.1**5):
    """Solves a polynomial from a list of coefficients (least significant to most)."""
    coeffs.reverse()
    topRow = [-coeffs[i]/float(coeffs[0]) for i in range(1, len(coeffs))]
    solMatrix = matrix(1, len(coeffs)-2, len(coeffs)-1)
    solMatrix.addRow(0, topRow)
    eigen = solMatrix.Eigen(20, confidence=confidence)
    return eigen[0], [len(i) for i in eigen[1]]


def walshMatrix(n):
    """Generates an nth degree Walsh Matrix"""
    if n<0:
        raise ValueError("n must be >=0")
    if n == 0:
        return matrix(1, 1, 1)
    else:
        return walshMatrix(n-1).KroneckerProd(matrix([1, 1, 1, -1]))

def memo(func):
    """The memorize decorator function."""
    cache = {}
    @ wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap

def listOfPrimePowers(n):
    """Returns 2 lists, (prime powers up to n, their bases)"""
    try:
        ##These are all saved variables in the function
        ##for faster calculation later. 
        sieveList = listOfPrimePowers.biggestList
        #sieveList has 0 for non-powers, 2 for primes, 1 for powers
        primeBases = listOfPrimePowers.pBases
        #primeBases has the prime base for every prime power.
        #arbitrary if not a prime power. 
    except AttributeError:
        ##initializes the variables if they haven't been defined yet.
        listOfPrimePowers.biggestList = [0, 0, 2, 2, 1, 2]
        listOfPrimePowers.pBases = [0, 1, 2, 3, 2, 5]
        sieveList = listOfPrimePowers.biggestList
        primeBases = listOfPrimePowers.pBases
    if len(sieveList)>n:
        sieveList = sieveList[:n+1]
        primeBases = primeBases[:n+1]
    else:
        ##Here's where the algorithm starts
        ##This is similar to a sieve of eratosthenes
        ##But it keeps track of when a number is
        ##eliminated twice. Those will be the non-squares.
        prevN = len(sieveList)-1
        sieveList   = sieveList + [2]*(n-prevN)
        primeBases  += [i for i in xrange(prevN+1, n+1)]
        for i in xrange(2, n/2+1):
            if sieveList[i] == 2:
                j = i*(prevN/i)+i
                if j == i:
                    j+=i
                while(j<=n):
                    if sieveList[j]==2:
                        sieveList[j]-=1
                        primeBases[j]=i
                    elif sieveList[j]==1:
                        sieveList[j]-=1
                    j+=i
        listOfPrimePowers.biggestList = sieveList
        listOfPrimePowers.pBases = primeBases
    ##Now, time to extract all the prime powers and their bases!
    retList = []
    retPrimeBases = []
    for i in xrange(n+1):
        if sieveList[i]!=0:
            retList.append(i)
            retPrimeBases.append(primeBases[i])
    return retList, retPrimeBases

def listOfPrimes(n):
    """returns a list of primes up to n"""
    try:
        ##These are all saved variables in the function
        ##for faster calculation later. 
        sieveList = listOfPrimePowers.biggestList
    except AttributeError:
        ##initializes the variables if they haven't been defined yet.
        listOfPrimePowers.biggestList = [0, 0, 1, 1, 0, 1]
        sieveList = listOfPrimePowers.biggestList
    if len(sieveList)>n:
        pass
    else:
        ##Here's where the algorithm starts
        ##This the sieve of eratosthenes
        prevN = len(sieveList)-1
        sieveList   = sieveList + [1]*(n-prevN)
        i = 2
        while i<= int(n**.5):
            if sieveList[i] == 1:
                j = i*(prevN/i)+i
                if j == i:
                    j+=i
                while(j<=n):
                    if sieveList[j]==1:
                        sieveList[j]=0
                    j+=i
            i+=1
        listOfPrimePowers.biggestList = sieveList
    ##Now, time to extract all the primes!
    retList = []
    i = 0
    while i<= n:
        if sieveList[i]!=0:
            retList.append(i)
        i+= 1
    return retList
    
@memo ##sexy decorator            
def choose(a, b):
    """Calculates the binomial coefficient of a over b."""
    if a<b or b<0:
        return 0
    if b>a-b:
        return choose(a, a-b)
    primePowList, primeBaseList = listOfPrimePowers(a)
    ##e.g.:
    ##primePowList = [2, 3, 4, 5, 7, 8, 9,...]
    ##primeBaseList = [2, 3, 2, 5, 7, 2, 3,...]
    expDict = dict.fromkeys(primeBaseList, 0)
    for j in range(len(primePowList)):
        expDict[primeBaseList[j]] -= b/primePowList[j]
        expDict[primeBaseList[j]] += a/primePowList[j] - (a-b)/primePowList[j]
    return product(*[k**expDict[k] for k in expDict.iterkeys()])

def factorial(n):
    """Calculates n!"""
    primePowList, primeBaseList = listOfPrimePowers(n)
    expDict = dict.fromkeys(primeBaseList, 0)
    for j in range(len(primePowList)):
        expDict[primeBaseList[j]] += n/primePowList[j]
    return product(*[k**expDict[k] for k in expDict.iterkeys()])

def makeSum_Of_kth_Powers_to_N(k, retCoeffs=False):
    """Returns a function for calculating sum(i**k for i in range(n+1))"""
    ##Note, this does not use Benoulli numbers... ha ha ha
    OurLcm = lcm(*range(1,k+2))
    coeffsList = [0]*(k+1) + [OurLcm/(k+1)]
    j = k
    while(j>0):
        coeffsList[j] = sum(((-1)**(i-j+1))*choose(i, j-1)*coeffsList[i]\
                            for i in range(j+1, k+2))/j
        j -= 1
    OurGcd = abs(gcd(*(coeffsList+[OurLcm])))
    coeffsList = [i/OurGcd for i in coeffsList]
    OurLcm = OurLcm/OurGcd
    if retCoeffs:
        return lambda n: sum(coeffsList[i]*n**i for i in range(k+2))/OurLcm,\
               (coeffsList, OurLcm)
    else:
        return lambda n: sum(coeffsList[i]*n**i for i in range(k+2))/OurLcm

def factorInt(n, primeList=None):
    """Factors an Integer n. Returns a list of 2-tuples: (prime, power)"""
    ##This is not a fast implementation for large n.
    ##However, this will be fine for small purposes.
    
    sqrtOfN = int(n**.5)
    if primeList != None:
        LoP = primeList
    else:
        LoP = listOfPrimes(sqrtOfN)
    retList = []
    for p in LoP:
        if p>sqrtOfN:
            break
        k = 0
        while(n%p == 0):
            n = n/p
            k+=1
        if k != 0:
            retList.append((p, k))
    if n<sqrtOfN:
        return retList
    else:
        return retList + [(n, 1)]

def findPrimePowerModMultiplicativeOrder(x, p, k, primeList=None):
    """Finds the multiplicative order of x modulo p**k for a prime p.
        (This will function incorrectly if p is not a prime or
        if x is not reletively prime to p)"""
    ##This is slow for large n, but will be fine for small purposes.
    ret = (p-1)*(p**(k-1))
    if k!= 1:
        factorizedRet = factorInt(p-1, primeList)+[(p, k-1)]
    else:
        factorizedRet = factorInt(p-1, primeList)
    for prime, power in factorizedRet:
        while power>0:
            ret = ret/prime
            power -= 1
            if mod_exp(x, ret, p**k) != 1:
                ret = ret*prime
                break
    return ret

def sumOfDigitCyclesOfUnitFractions(n):
    """Let L(n) be the length of the the cycle of the digits of 1/n.
    This function solves for sum(L(i) for i in xrange(1, n+1))"""
    LastCheck = time.clock()
    L = [1]*n
    maxI = int(math.log(n, 2))
    maxJ = int(math.log(n, 5))
    for i in xrange(maxI+1):
        for j in xrange(maxJ+1):
            m = (2**i)*(5**j)
            if m<=n:
                L[m-1] = 0
    LoP = listOfPrimes(n)
    ret = 0
    offSet = 0
    for p in LoP:
        if p != 2 and p != 5:
            k = 1
            powerOfP = p
            while k<=math.log(n, p):
                mO = findPrimePowerModMultiplicativeOrder(10, p, k, LoP)
                multipleOfPPower = powerOfP
                while multipleOfPPower <= n:
                    L[multipleOfPPower-1-offSet] = lcm(mO, L[multipleOfPPower-1-offSet])
                    multipleOfPPower += powerOfP
                    if multipleOfPPower%(powerOfP*p) == 0:
                        multipleOfPPower += powerOfP
                k+=1
                powerOfP *= p
            if time.clock()-LastCheck >20:
                print str(p) + " is the prime at "+ str(time.clock())
                LastCheck = time.clock()
                L.reverse()
                for i in xrange(p - offSet):
                    ret += L.pop()
                L.reverse()
                offSet = p
    return ret+sum(L)

def listOfDigitCyclesOfUnitFractions(n):
    """Let L(n) be the length of the the cycle of the digits of 1/n.
    This function gives a dictionary with key-value pairs i:L(i)
    for i up to (and including) n"""
    LastCheck = time.clock()
    L = [1]*n
    maxI = int(math.log(n, 2))
    maxJ = int(math.log(n, 5))
    for i in xrange(maxI+1):
        for j in xrange(maxJ+1):
            m = (2**i)*(5**j)
            if m<=n:
                L[m-1] = 0
    LoP = listOfPrimes(n)
    offSet = 0
    for p in LoP:
        if p != 2 and p != 5:
            k = 1
            powerOfP = p
            while k<=math.log(n, p):
                mO = findPrimePowerModMultiplicativeOrder(10, p, k, LoP)
                multipleOfPPower = powerOfP
                while multipleOfPPower <= n:
                    L[multipleOfPPower-1-offSet] = lcm(mO, L[multipleOfPPower-1-offSet])
                    multipleOfPPower += powerOfP
                    if multipleOfPPower%(powerOfP*p) == 0:
                        multipleOfPPower += powerOfP
                k+=1
                powerOfP *= p
            if time.clock()-LastCheck >20:
                print str(p) + " is the prime at "+ str(time.clock())
                LastCheck = time.clock()
                L.reverse()
#                for i in xrange(p - offSet):
#                    ret += L.pop()
                L.reverse()
                offSet = p
    retDict = dict.fromkeys(range(1, n+1))
    for key in retDict.iterkeys():
        retDict[key] = L[key-1]
    return retDict

def repeatSequenceGenerator(sequence):
    """Makes a generator that repeats the sequence indefinately. """
    while(True):
        for i in sequence:
            yield i

def substringsGenerator(string):
    for curStringSize in range(1, len(string)+1):
        for i in range(1+len(string)-curStringSize):
            yield string[i:i+curStringSize]

def NumberOfOneChildNumbersWithNDigits(N):
    """The number of one-child numbers with N digits

We say that a d-digit positive number (no leading zeros)
is a one-child number if exactly one of its sub-strings is divisible by d.

For example, 5671 is a 4-digit one-child number.
Among all its sub-strings 5, 6, 7, 1, 56, 67, 71,
567, 671 and 5671, only 56 is divisible by 4.
Similarly, 104 is a 3-digit one-child number because
only 0 is divisible by 3.
1132451 is a 7-digit one-child number because only 245 is divisible by 7.
"""
    if N<1:
        raise ValueError("N must be 1 or larger")
    if N%10 == 0:
        ##There will be no solutions
        return 0
    
    aN = N #just N

    ##use "left to right sweep dict" method
    ##Keys: (curCount, aList, aTracker)
    preDict =    {(1*(2%N==0), (0,), 2): 1, (1*(3%N==0), (0,), 3): 1,\
                  (1*(6%N==0), (0,), 6): 1, (1*(1%N==0), (0,), 1): 1,\
                  (1*(7%N==0), (0,), 7): 1, (1*(8%N==0), (0,), 8): 1,\
                  (1*(4%N==0), (0,), 4): 1, (1*(9%N==0), (0,), 9): 1,\
                  (1*(5%N==0), (0,), 5): 1}
##    masterDict = anydbm.open("C:/Python27/poopers0.dat", 'n')
##    writeToDict = anydbm.open("C:/Python27/poopers1.dat", 'n')
    masterDict = dict()
    writeToDict = dict()
    for key in preDict.iterkeys():
##        masterDict[str(key)] = str(preDict[key])
        masterDict[key] = preDict[key]
    for i in range(N-1):
        print "cycle", i, time.clock(), len(masterDict)
        for key in masterDict.iterkeys():
            for d in range(10):
##                key = eval(prekey)
                aTracker = (key[2]*10+d)%aN
                aList = [(10*j)%aN for j in key[1]]+[(10*key[2])%aN]
                for v in [v for v in aList]:
                    if 2<aList.count(v):
                        aList.remove(v)
                aList.sort()
                curCount = key[0]
                try:
                    curCount+=aList.count(aTracker)
                except ValueError:
                    pass
                if curCount<2:
                    newKey = (curCount, tuple(aList), aTracker)
                    if writeToDict.has_key(newKey):
                        writeToDict[newKey] += masterDict[key]
##                        writeToDict[str(newKey)] = str(int(writeToDict[str(newKey)])\
##                                                  + int(masterDict[prekey]))
                    else:
                        try:
                            writeToDict[newKey] = masterDict[key]
##                            writeToDict[str(newKey)] = str(masterDict[prekey])
                        except MemoryError:
                            print len(masterDict)
                            raise MemoryError
        del masterDict
        masterDict = writeToDict
        writeToDict = dict()
##        writeToDict = anydbm.open("C:/Python27/poopers"+str(i+2)+".dat", 'n')
    retTotal = 0
    for key in masterDict.iterkeys():
        if key[0] == 1:
            retTotal+= masterDict[key]
##    masterDict.close()
    return retTotal
####This is my previous algorithm. It is slow. 
##        KDict = dict()
##        for i in range(10):
##            KDict[str(i)] = 1*(i%N==0)
##        curLenOfKeys = 1
##        while curLenOfKeys<N:
##            KDictIterKeysI = [i for i in KDict.iterkeys()]
##            KDictIterKeysJ = [j for j in KDict.iterkeys()]
##            for i in KDictIterKeysI:
##                for j in KDictIterKeysJ:
##    ##                if time.clock()-LastCheck>20:
##    ##                    LastCheck = time.clock()
##    ##                    print "at " + str(LastCheck)+ " in depth " + str(N)+\
##    ##                          " keyLength " + str(curLenOfKeys)
##                    if len(i) == curLenOfKeys and len(j) == curLenOfKeys:
##                        if i[1:] == j[:-1]:
##                            newKey = i[0]+j
##                            if i[1:] != '':
##                                newVal = KDict[i]+KDict[j]\
##                                    -KDict[i[1:]]+1*(int(newKey)%N==0)
##                            else:
##                                newVal = KDict[i]+KDict[j]+1*(int(newKey)%N==0)
##                            if newVal <= 1:
##                                KDict[newKey] = newVal
##            keys = [k for k in KDict.iterkeys()]
##            for key in keys:
##                if len(key)< curLenOfKeys-1:
##                    KDict.pop(key)
##            curLenOfKeys += 1
##        for key in [k for k in KDict.iterkeys()]:
##                if key[0] == "0":
##                    del KDict[key]
##                elif len(key)< curLenOfKeys:
##                    del KDict[key]
##        return sum(v for v in KDict.itervalues())

def iterateMultidementionalArray(dimSizes):
    """Makes a generator that iterates through multidementional indecies."""
    if len(dimSizes) == 1:
        for i in range(dimSizes[0]):
            yield tuple([i])
    else:
        iMA = iterateMultidementionalArray(dimSizes[1:])
        while(True):
            try:
                nextTail = iMA.next()
            except StopIteration:
                break
            for i in range(dimSizes[0]):
                yield tuple([i]) + nextTail
                
def factorisationTriples(PowDict):
    K = [key for key in PowDict.iterkeys()]
    K.sort()
    K.reverse()
    logK = [math.log(key, 2) for key in K]
    curLowSums = [0]*len(PowDict)
    curMidSums = [0]*len(PowDict)
    curHighSums = [PowDict[key] for key in K]
    oldLowSums = curLowSums
    oldMidSums = curMidSums
    oldHighSums = curHighSums
    curLow = 0
    curMid = 0
    curHigh = sum(PowDict[key]*math.log(key, 2) for key in K)
    curDif = curHigh-curLow
    change = True
    while(change):
        print time.clock(), curDif
        change = False
        oldLowSums = curLowSums
        oldMidSums = curMidSums
        oldHighSums = curHighSums
#        oldLow = curLow
#        oldMid = curMid
#        oldHigh = curHigh
        testDifferences = iterateMultidementionalArray([v+1 for v in [oldLowSums[i]+oldHighSums[i] for i in \
                                                                      range(len(oldHighSums))]])
        for t in testDifferences:
            listT = [i for i in t]
            curLowSums = listT
            curHighSums = [oldLowSums[i]+oldHighSums[i]-listT[i] for i in range(len(listT))]
            curLow = sum(curLowSums[i]*logK[i] for i in range(len(curLowSums)))
            curHigh = sum(curHighSums[i]*logK[i] for i in range(len(curHighSums)))
            if max(abs(curMid-curLow),\
                    abs(curMid-curHigh),\
                    abs(curLow-curHigh))\
                    <curDif:
                change = True
                temp = [(curLow, curLowSums),\
                        (curHigh, curHighSums)\
                        , (curMid, curMidSums)]
                temp.sort()
                curLow, curLowSums = temp[0]
                curMid, curMidSums = temp[1]
                curHigh, curHighSums = temp[2]
                curDif = curHigh - curLow
                break
    high = 0
    mid = 0
    low = 0
    total = 0
##    logK = [mpmath.log(key, 2) for key in K]
    for i in range(len(K)):
        low+= logK[i]*oldLowSums[i]
        mid+= logK[i]*oldMidSums[i]
        high+= logK[i]*oldHighSums[i]
        total+= logK[i]*PowDict[K[i]]
    curDif = high-low
    change = True
    testDifferences = iterateMultidementionalArray([PowDict[key]+1 for key in K])
    while(change):
        print time.clock(), curDif
        change = False
#        oldHigh = high
#        oldMid = mid
#        oldLow = low
        bestNewHigh = 0
        bestNewLow = total+1
        breakflag = False
        test2 = 0
        for t in testDifferences:
            test = 0
            for i in range(len(K)):
                test += logK[i]*t[i]
            if (test>total/5 and test<total/3) and curDif>(total-test)/2 - test: ##A good heuristic for most cases.
                print time.clock(), bestNewLow, bestNewHigh
                bestNewLow = test
                curLowSums = t
                testDiffs2 = iterateMultidementionalArray([PowDict[K[i]]+1-t[i] for i in range(len(K))])
                bestNewHigh = 0
                curHighSums = oldHighSums
                for t2 in testDiffs2:
                    test2 = 0
                    for i in range(len(K)):
                        test2 += logK[i]*t2[i]
                    bestNewHigh = test2
                    curHighSums = t2
                    if bestNewHigh>bestNewLow:
                        if curDif>max(abs(bestNewHigh-bestNewLow),\
                                      abs(total-bestNewHigh-(2*bestNewLow)),\
                                      abs(total-(2*bestNewHigh)-bestNewLow)):
                            breakflag = True
                            break
            if breakflag:
                break 
        if breakflag:
            low = bestNewLow
            oldLowSums = curLowSums
            high = bestNewHigh
            oldHighSums = curHighSums
        mid = total - high - low
        oldMidSums = tuple([PowDict[K[i]]-oldHighSums[i]-oldLowSums[i] for i in range(len(K))])
        temp = [(low, oldLowSums),\
                (high, oldHighSums)\
                , (mid, oldMidSums)]
        temp.sort()
        low, oldLowSums = temp[0]
        mid, oldMidSums = temp[1]
        high, oldHighSums = temp[2]
        print low, mid, high
        if(curDif>high-low):
            change = True
            curDif = high-low
    return K, oldLowSums, oldMidSums, oldHighSums

def pivotFlip(string, pivot):
    """Reverses a string past a pivot index."""
    flip = list(string[pivot:])
    flip.reverse()
    return string[:pivot]+''.join(flip)

def findMaximixArrangements(N):
    """Generates a list of Maximix arrangements (Project Euler, #336)"""
    ##This algorithm searches for possibilities by starting with as few cars as possible, and then
    ##adding cars to the front and then applying the farthest movement to the front car. 
    if N == 1:
        return ['a']
    if N == 2:
        return ['ba']
    if N>36:
        raise ValueError("N is too large")
    previousSolution = findMaximixArrangements(N-1)
    for i in range(len(previousSolution)): ##Moves cars up one letter and adds 'a' in front
        previousSolution[i] = 'a' + ''.join(ALPHABET[ALPHABET.index(a)+1] for a in previousSolution[i])
    ##The following dictionaries will have keys that are car arrangements, and values
    ##that are the "maximix" distances from the N-1 solution.
    ##To each of these, we apply 2 pivotFlips, one from 0 and then one from any point to the left
    ##Of the end.
    newSolutions = []
    for pS in previousSolution:
        nS = pivotFlip(pS, 0)
        for i in range(1, N-1):
            newSolutions.append(pivotFlip(nS, i))
    return newSolutions
def lookAndSaySequence(start = '1'):
    yield start
    curString = start
    newString = ''
    while(True):
        curCount = 0
        curChar = curString[0]
        for char in curString:
            if char == curChar:
                curCount += 1
            else:
                newString += str(curCount) + curChar
                curChar = char
                curCount = 1
        newString += str(curCount) + curChar
        curChar = char
        yield newString
        curString = newString
        newString = ''
def lookAndSayIsMadeOfElements(string):
    if string == '':
        return True
    string
#    tests = []
    ElementDict = LOOKANDSAYELEDICT
    ElementList = [str(el[1]) for el in ElementDict.itervalues()]
    for el in ElementList:
        if string.startswith(el):
            newString = string[len(el):]
            temp = lookAndSayIsMadeOfElements(newString)
            if temp:
                return True
    return False
def lookAndSayCounts(N, mod=2**30):
    """Gives the counts for 1's, 2's, and 3's for the N'th number in the look and say sequence.
(with a modulus)"""
    if N <= 1:
        return 0, 0, 0
    if N == 1:
        return 1%mod, 0, 0
    if N == 2:
        return 2%mod, 0, 0
    if N == 3:
        return 1%mod, 1%mod, 0
    if N == 4:
        return 3%mod, 1%mod, 0
    if N == 5:
        return 4%mod, 2%mod, 0
    if N == 6:
        return 3%mod, 2%mod, 1%mod
    if N == 7:
        return 4%mod, 3%mod, 1%mod
##    if N == 8:
##        return 6%mod, 2%mod, 2%mod

    power = N-8
    ##ElementTransDict will be a dictionary on a weighted graph structure
    ##with keys as nodes. I will treat it like a matrix, and take the N-8th power of it.
    ElementTransDict = copy.deepcopy(LOOKANDSAYELEDICT)
    for key in ElementTransDict.iterkeys():
        keyCount = dict()
        for k in ElementTransDict[key][0]:
            keyCount[k] = ElementTransDict[key][0].count(k)
        ElementTransDict[key] = keyCount
        
    ElementList= [el for el in ElementTransDict.iterkeys()]
    curElements = dict.fromkeys(ElementList, 0)
    curElements['Hf'] = 1%mod
    curElements['Sn'] = 1%mod
    ##Time for some math...
    powerBin = bin(power)
    SquaredTransDict = copy.deepcopy(ElementTransDict) ##I will square this repeatedly
    ptr = 1
    PowTransDict = dict()
    for key in ElementList:
        PowTransDict[key] = {key:1}
    while(powerBin[-ptr] != 'b'):
        if(powerBin[-ptr] == '1'):
            newPowDict = dict.fromkeys(ElementList)
            for key in newPowDict:
                newPowDict[key] = dict()
            for keyA in ElementList:
                for keyB in ElementList:
                    accu = 0
                    for k in ElementList:
                        if SquaredTransDict[keyA].has_key(k) and PowTransDict[k].has_key(keyB):
                            accu += SquaredTransDict[keyA][k]*PowTransDict[k][keyB]
                            accu %= mod
                    if accu!=0:
                        newPowDict[keyA][keyB] = accu
            PowTransDict = newPowDict
        newSquaredDict = dict.fromkeys(ElementList)
        for key in newSquaredDict:
            newSquaredDict[key] = dict()
        for keyA in ElementList:
            for keyB in ElementList:
                accu = 0
                for k in ElementList:
                    if SquaredTransDict[keyA].has_key(k) and SquaredTransDict[k].has_key(keyB):
                        accu += SquaredTransDict[keyA][k]*SquaredTransDict[k][keyB]
                        accu %= mod
                if accu != 0:
                    newSquaredDict[keyA][keyB] = accu
        SquaredTransDict = newSquaredDict
        ptr = ptr + 1
    newCurElements = dict()
    for keyA in PowTransDict:
        accu = 0
        for k in curElements:
            if PowTransDict[k].has_key(keyA):
                accu += PowTransDict[k][keyA]*curElements[k]%mod
        if accu != 0:
            newCurElements[keyA] = accu
    ElementStrDict = copy.deepcopy(LOOKANDSAYELEDICT)
    for key in ElementStrDict.iterkeys():
        ElementStrDict[key] = str(ElementStrDict[key][1])
    return  sum(ElementStrDict[el].count('1')*newCurElements[el] for el in newCurElements)%mod,\
            sum(ElementStrDict[el].count('2')*newCurElements[el] for el in newCurElements)%mod,\
            sum(ElementStrDict[el].count('3')*newCurElements[el] for el in newCurElements)%mod

def intToBalancedTernary(n):
    if not any(type(n)==i for i in (int, long)):
        raise TypeError("n must be an int or long")
    if n == 0:
        return "0"
    retList = []
    while n!= 0:
        div = n//3
        rem = n-3*div
        if rem == 0:
            retList += ["0"]
            n = div
        if rem == 1:
            retList += ["1"]
            n = div
        if rem == 2:
            retList += ["T"]
            n = div+1
    retList.reverse()
    return "".join(retList)

def intFromBalancedTernary(string):
    ret = 0
    for tet in string:
        ret *= 3
        if tet == "1":
            ret += 1
        elif tet == "T":
            ret -= 1
        elif tet == "0":
            continue
        else:
            raise TypeError("String is not a valid balanced ternary form.")
    return ret
                
def de_bruijn(k, n):
    """Calculates a k-ary De Bruijn sequence of order n"""
    LyndonWords = []
    curWord = [0]
    while curWord!=[]:
        if n%len(curWord) == 0:
            LyndonWords.append(curWord)
        curWord = (curWord*(1+(n/len(curWord))))[:n]
        while curWord[-1] == k-1:
            curWord.pop()
            if len(curWord) == 0:
                break
        if len(curWord)!=0:
            curWord[-1]+=1

            
    ret = [letter for word in LyndonWords for letter in word]
    return ret

def findLargestAlphebetizedSubstr(inStr):
    """Finds the largest substring of inStr that is in alphebetical order."""
    if(len(inStr) == 0):
        return ""
    curSubstr = inStr[0]
    curLargestSubstr = ""
    for i in inStr:
        if i.lower() >= curSubstr[-1].lower():
            #Still alphabetical...
            curSubstr += i
            
        else:                            
            #No longer alphabetical...
            if len(curSubstr) > len(curLargestSubstr): 
                #Test to see if this substring is longer than the last one.
                curLargestSubstr = curSubstr
            curSubstr = i
            
    #End looping through string
    if len(curSubstr) > len(curLargestSubstr): 
        #Test to see if this final substring is longer than the biggest so far.
        return curSubstr
        
    return curLargestSubstr