'''
Created on Sep 22, 2014

@author: edmondkwan
'''

class Packet(object):

    def __init__(self, generatedAt):
        self.generatedAt = generatedAt
        
    def genAt(self, tickGenerated):
        self.generatedAt = tickGenerated
    