# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 22:22:24 2016

@author: Tom
"""

HAS_NUMBER_IN_RESPONSE = True

def getDocsFromTextFile(filename): 
    f = open(filename, 'r')
    ret = f.readlines()
    f.close()
    return [d for d in ret if (not d.isspace())]
    
def cleanWord(raw_w):
    return raw_w.lower().strip(",").replace("'s", "")

def makeMatFromDocuments(docs):
    
    """
    docs: A list of survey responses.
    """
    
    retMat = dict()
    
    for i in xrange(len(docs)):
        d = docs[i]
        if HAS_NUMBER_IN_RESPONSE:
            sentences = d.split(".")[1:]
        else:
            sentences = d.split(".")
        for s in sentences:
            words = s.split(" ")
            for raw_w in words:
                w = cleanWord(raw_w)
                try:
                    retMat[w][i] += 1
                except KeyError:
                    retMat[w] = [0]*len(docs)
                    retMat[w][i] = 1
                    
    return retMat
    
if __name__ == "__main__":
    myMat = makeMatFromDocuments(getDocsFromTextFile("artSurveyData.txt"))
    
    