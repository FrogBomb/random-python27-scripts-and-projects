# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 13:46:57 2014

@author: Tom
"""
def nxnSpiral(n, i, j):
    if i>=n or j>=n:
        raise IndexError(n, i, j)
    if j == 0:
        return n**2-1-i
    elif i == n-1:
        return n**2-n-j
    else:
        return nxnSpiral(n-1, n-2-i, n-1-j)

def isPrime(n):
    if n<=1:
        return False
    for i in range(2, int(n**.5) + 2):
        if n%i == 0:
            return False
    return True
    
def nxnUlamSpiral(n, i, j):
    curNum = nxnSpiral(n, i, j)
    if curNum == 0:
        return "*"
    if isPrime(curNum):
        return "+"
    else:
        return " "
        
if __name__=="__main__":
    for j in range(50):
        for i in range(50):
            print nxnUlamSpiral(50, j, i),
        print ""