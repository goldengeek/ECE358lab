'''
Created on Sep 22, 2014

@author: edmondkwan
'''

class Packet(object):

    def __init__(self, generatedAt, serviceTime):
        self.generatedAt = generatedAt
        self.exitedSystemAt = 0
        self.serviceTime = serviceTime
        
        
    def genAt(self, tickGenerated):
        self.generatedAt = tickGenerated
    