'''
Created on Sep 22, 2014

@author: edmondkwan
'''

class Generator(object):
    def __init__(self, params):
        self.tickCounter = 0
        
    
    def updateTick(self):
        self.tickcounter += 1
    
    def computNextTick(self):
        return 5