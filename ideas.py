##A decorator!
##Use:
#just before a function, type
#@print_timing

import time

def print_timing(func):
  def wrapper(*arg):
    t1 = time.clock()
    res = func(*arg)
    t2 = time.clock()
    print '%s took %0.3fms' % (func.func_name, (t2-t1)*1000.0)
    return res
  return wrapper


##using yield
def solitareDeal(deck):
    """Deals the deck out in an solitare fashion."""
    curDeal = [[]] ##will be a list of lists
    curPlace = 0
    for i in deck:
        yield curDeal[:-1]##cuts off the open spot at the end
        curDeal[curPlace].append(i)
        curPlace += 1
        if len(curDeal)==curPlace:
            curPlace = 0
            curDeal.append([])
    yield curDeal[:-1]##for the last card!

def solitareDealDemo():
    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    print "This is our deck!"
    print deck
    temp = raw_input("\nPress Enter\n")
    for i in solitareDeal(deck):
        print i
        temp = raw_input("\nPress Enter\n")
    print "And that's it!"

from random import randint

def skipAround(yourList):
    """Skips around your list!"""
    while(True):
        curIndex = randint(0, len(yourList)-1)
        yield yourList[curIndex]


##Some string functions

def cat(*strings):
    """Concatinates strings"""
    return "".join(strings)

def initials(string, sep = ".", sepAtEnd = True):
    """Returns the initials of a string"""
    splitString = string.split(" ")
    theInitialList = [i[:1].capitalize() for i in splitString]
    return sep.join(theInitialList)+sep*sepAtEnd

##Using Dictionaries

def addKey(myDict, newKey):
    """Adds a key "newKey" if the key does not already exist."""
    if not myDict.has_key(newKey):
        myDict[newKey] = None

def sortKeys(myDict):
    """Takes a dictionary and returns a sorted list of the keys."""
    ret = myDict.keys()
    return ret.sort()

def reverseDict(myDict):
    """Makes a new dictionary, but swaps keys with values"""
    keys = myDict.keys()
    values = myDict.values()
    retDict = dict()
    for k in keys:
        retDict[myDict[k]] = k
    return retDict

##Some interesting tidbits

class ThisIsMyError(Exception):
    """This is My Error, and this is why they are easy to make!"""
    pass


def floatsSuck():
    a =(10000000000000000000000/3.0 + .7)*10
    b = 100000000000000000000000/3.0
    c = b + 7
    print "a =(10000000000000000000000/3.0 + .7)*10 = " +str(a)
    print "b = 100000000000000000000000/3.0 = " + str(b)
    print "c = b + 7 = " + str(c)
    print "a - b = " + str(a - b) + "(should be 7...)"
    print "c - b = " + str(c - b) + "(should be 7...)"
    print "a - c = " + str(a - c) + "(should be 0...)"

def floatsSuckLess():
    a =(100/3.0 + .7)*10
    b = 1000/3.0
    c = b + 7
    print "a =(100/3.0 + .7)*10 = " +str(a)
    print "b = 1000/3.0 = " + str(b)
    print "c = b + 7 = " + str(c)
    print "a - b = " + str(a - b) + "(should be 7...)"
    print "c - b = " + str(c - b) + "(should be 7...)"
    print "a - c = " + str(a - c) + "(should be 0...)"

##Other ideas
class BaseMatrix:
    """A basic matrix object class!"""

    def __init__(self, rows, cols, data = None):
        self._numRows = rows
        self._numCols = cols
        if data == None:
            self._data = [0]*rows*cols
        elif len(data)>rows*cols:
            raise BufferError("data must be able to fit in the matrix")
        else:
            self._data = data + [0]*(rows*cols-len(data))
            
    def __getitem__(self, key):
        if type(key) == int:
            return self._data[key]
        if type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)&(key[0]>=0)&(key[1]>=0):
                    return self._data[self._numCols*key[0] + key[1]]
                else:
                    raise IndexError("list index out of range")
        raise TypeError("must be an int or two ints separated by a comma")
    
    def __setitem__(self, key, value):
        if type(key) == int:
            self._data[key] = value
            return
        if type(key) == tuple:
            if len(key) == 2:
                if (key[0]<self._numRows)&(key[1]<self._numCols)&(key[0]>=0)&(key[1]>=0):
                    self._data[self._numCols*key[0] + key[1]] = value
                    return
                else:
                    raise IndexError("list index out of range")
        raise TypeError("must be an int or two ints separated by a comma")
    
    def __str__(self):
        ret = ""
        return ret.join(str(self.getRow(i))+"\n" for i in range(self._numRows))[:-1]
    
    def dims(self):
        return self._numRows, self._numCols
    
    def getRow(self, rowNum):
        return [self[rowNum, i] for i in range(self._numCols)]
    
    def getCol(self, colNum):
        return [self[i, colNum] for i in range(self._numRows)]

    def transpose(self):
        """Transposes the matrix."""
        newRows = self._numCols
        newCols = self._numRows
        new_data = [self[j, i] for i in range(newRows) for j in range(newCols)]
        self._numRows = newRows
        self._numCols = newCols
        self._data = new_data

##Implementation 1 (String and List manipulation heavy)
def putBitsIntoList_1(n, L):
    """Takes an integer and puts L of it's least sig bits into a list"""
    binstr = bin(n)[2:]
    ret = [0]*L
    for i in range(L):
        try:
            ret[i] = int(binstr[-i-1])
        except IndexError:
            pass
    return ret

##Implementation 2 (This one is more fun!)
def putBitsIntoList_2(n, L):
    """Takes an integer and puts L of it's least sig bits into a list"""
    ret = []
    for i in range(L):
        ret.append(n%2)
        n = n/2
    return ret

def multiplyMatriciesMod2(self, other):
    """Multiplies two matricies mod 2"""
    ###Note, this is NOT CLEANED. I had this as an
    ###overloaded __mul__ in one of my other programs.(I was thinking we could
    ###talk about inheritence for a "MathMatrix" or something of the sort)
    if self._numCols != other._numRows:
        raise IndexError(
            "in m*n, the number of rows of n must match the number of columns of m")
    new_matrix = BaseMatrix(self._numRows, other._numCols)
    for i in range(new_matrix._numRows):
        for j in range(new_matrix._numCols):
            new_matrix[i, j] = sum(self[i, k]*other[k, j] for k in range(self._numCols))%2
    return new_matrix
    
def getHammingBits(bitList, HammingEncodingMatrix = None):
    """Returns an altered bitList of specified hamming code.
        Default is the (7, 4) code."""
    
    if HammingEncodingMatrix == None: ##Default Hamming Matrix
        rowValues = [11, 13, 1, 14, 2, 4, 8]
        data = []
        for i in rowValues:
            data += putBitsIntoList_2(i, 4)
        HammingEncodingMatrix = BaseMatrix(7, 4, data)
        
    if not isinstance(HammingEncodingMatrix, BaseMatrix):
        raise TypeError("HammingEncodingMatrix must be a matrix!")
    HEM = HammingEncodingMatrix
    HEMdims = HEM.dims()
    bitMatrix = BaseMatrix(1+(len(bitList)-1)/HEMdims[1], HEMdims[1], bitList)
    bitMatrix.transpose()
    retMatrix = multiplyMatriciesMod2(HEM, bitMatrix)
    retList = []
    for i in range(retMatrix.dims()[1]):
        retList+=retMatrix.getCol(i)
    return retList

def checkHammingCode(hamCode, HammingDecodingMatrix = None):
    """Checks errors in a transmitted code.
        This function says what blocks had errors, if they are correctable, etc.
        Default is the (7, 4) code."""
    ##Need to implement
    
        
