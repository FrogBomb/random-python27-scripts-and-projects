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

def putListIntoInt(inList, base = 2):
    """takes a list of values and converts it into an int"""
    string = "".join(str(i) for i in inList)
    return int(string, base)

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

def checkHammingCodeTrans(trans, HammingDecodingMatrix = None):
    """Checks errors in a transmitted code.
        This function returns
        Default is the (7, 4) code."""
    
    if HammingDecodingMatrix == None:
        rowValues = [85, 102, 120]
        data = []
        for i in rowValues:
            data += putBitsIntoList_2(i, 7)
        HammingDecodingMatrix = BaseMatrix(3, 7, data)
        
    HDM = HammingDecodingMatrix
    HDMdims = HDM.dims()
    bitMatrix = BaseMatrix(1+(len(trans)-1)/HDMdims[1], HDMdims[1], trans)
    bitMatrix.transpose()
    retMatrix = multiplyMatriciesMod2(HDM, bitMatrix)
    for i in range(retMatrix.dims()[1]):
        if sum(retMatrix.getCol(i)) != 0:
            print "Error in sector " + str(i) + "||errorCode =:",
            print retMatrix.getCol(i)
    return retMatrix
    

    
