# -*- coding: utf-8 -*-
"""
Created on Mon Aug 11 19:31:04 2014

@author: Tom
"""

class ThreeTree:
    def __init__(self, coordinates, data):
        self.coords = coordinates
        self.data = data
        self.nodes = []
        
    def split(self, data1, data2, data3):
        if len(self.nodes) == 0:
            newCoords = (self.coords[0]/2.0, self.coords[1]/2.0)
        else:
            newCoords = ((self.coords[0]+self.nodes[-1][0].coords[0])/2.0,\
                        (self.coords[1]+self.coords[-1][0].coords[1])/2.0)
                        
        self.nodes.append[[ThreeTree(newCoords, data1),\
                            ThreeTree(newCoords, data2),\
                            ThreeTree(newCoords, data3)]]
       