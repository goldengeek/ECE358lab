'''
Created on Sep 22, 2014

@author: edmondkwan
'''

class Packet(object):

    def __init__(self, generatedAt,length, nodePosition):
        self.generatedAt = generatedAt
        self.length = length
        
    def genAt(self, tickGenerated):
        self.generatedAt = tickGenerated
    