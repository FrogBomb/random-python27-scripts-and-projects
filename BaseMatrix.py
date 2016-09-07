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
    
    def __mul__(self, other):
        """Multiplies two matricies"""
        if self._numCols != other._numRows:
            raise IndexError(
                "in m*n, the number of rows of n must match the number of columns of m")
        new_matrix = BaseMatrix(self._numRows, other._numCols)
        for i in range(new_matrix._numRows):
            for j in range(new_matrix._numCols):
                new_matrix[i, j] = sum(self[i, k]*other[k, j] for k in range(self._numCols))
        return new_matrix

    def __add__(self, other):
        if not isinstance(other, BaseMatrix):
            raise NotImplemented
        if (self._numRows != other._numRows)|(self._numCols != other._numCols):
            raise StandardError("must be the same size of matrix")
        return matrix(rows=self._numRows, cols=self._numCols, data=[self[i]+other[i] for i in range(len(self))])

    def __sub__(self, other):
        if not isinstance(other, BaseMatrix):
            raise NotImplemented
        if (self._numRows != other._numRows)|(self._numCols != other._numCols):
            raise StandardError("must be the same size of matrix")
        return matrix(rows=self._numRows, cols=self._numCols, data=[self[i]-other[i] for i in range(len(self))])

    def transpose(self):
        """Transposes the matrix."""
        newRows = self._numCols
        newCols = self._numRows
        new_data = [self[j, i] for i in range(newRows) for j in range(newCols)]
        self._numRows = newRows
        self._numCols = newCols
        self._data = new_data

    t = transpose ##alias
        
    def dims(self):
        return self._numRows, self._numCols
    
    def getRow(self, rowNum):
        return [self[rowNum, i] for i in range(self._numCols)]
    
    def getCol(self, colNum):
        return [self[i, colNum] for i in range(self._numRows)]
