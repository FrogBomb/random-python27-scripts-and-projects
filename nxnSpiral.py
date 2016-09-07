# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 13:20:08 2014

@author: Tom
"""

def nxnSpiral(n, i, j):
    if i>=n or j>=n:
        raise IndexError(n, i, j)
    if j == 0:
        return str(n**2-1-i)
    elif i == n-1:
        return str(n**2-n-j)
    else:
        return nxnSpiral(n-1, n-2-i, n-1-j)
        
if __name__ == "__main__":
    for j in range(10):
        for i in range(10):
            print nxnSpiral(10, i, j), "\t",
        print ""