# -*- coding: utf-8 -*-
"""
Created on Tue Nov 25 16:09:45 2014

@author: Tom
"""

def numOfFoursInBase(n, base):
    ret = 0
    while(n!=0):
        m = n//base
        if n-(m*base) == 4:
            ret += 1
        n = m
    return ret
    
def fouriestTransform(n):
    best = 2
    i = 2
    mostFours = 0
    while(i<n):
        newTest = numOfFoursInBase(n, i)
        if mostFours < newTest:
            best = i
            mostFours = newTest
        i+=1
    return dict(base = best, numberOfFoursInBase = mostFours)