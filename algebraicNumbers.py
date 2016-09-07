from BaseMatrix import *
from myFractions import fraction
from copy import deepcopy

class algebraicError(Exception):
    pass

class algebraic:
    def __init__(self, *coefficients):
        if len(coefficients) <= 1:
            raise NotImplemented("Must have at least 2 coefficients")
        temp = [fraction(-i, coefficients[0]) for i in coefficients[1:]]
        self._matrix = BaseMatrix(len(temp), len(temp), temp)
        self._degree = len(coefficients)-1
        for i in range(len(temp)-1):
            self._matrix[i+1, i] = 1

##    def estimateLargestMag(self, n):
##        poweredMatrix = deepcopy(self._matrix)
##        for i in range(n):
##            poweredMatrix = poweredMatrix*poweredMatrix
##        retVec = poweredMatrix.getCol(0)
##        retVec = [i*i for i in retVec]
##        ret = fraction(0, 1)
##        for i in retVec:
##            ret = ret + i
##        ret = float(ret.estimate(20))**.5
##        for i in range(n):
##            ret = ret**.5
##        return ret
        
            
##    def __pow__(self, power):
##    """returns (self**power)"""
##    k = bin(power)
##    ret = algebraic(*([0]*(self._degree+1)))
##    ptr = 1
##    ret = 1
##    while(k[-ptr] != 'b'):
##    	if(k[-ptr] == '1'):
##    		ret = (ret*self)
##    	n = (self*self)
##    	ptr = ptr + 1
##    return ret 			#exit
