'''
Created on Oct 26, 2014

@author: edmondkwan
'''



class Medium(object):
    def __init__(self, secPerTick, speedOfLan):
        self.active = False
        self.tickCount = 0
        self.nodeTransmitPos = 0
        self.pleft = 0
        self.pright = 0
        self.propSpeed = 200000000
        self.propTime =(10.0/self.propSpeed)*(1.0/secPerTick)
        self.propCount = 0
        self.secPerTick = secPerTick
        self.speedOfLan = speedOfLan
    
    def updateTick(self):
        self.tickCount +=1
        self.propCount +=1
        if self.propCount >= self.propTime:
            self.pright +=1
            self.pleft -=1
            self.propCount = 0
    def isMediumIdle(self):
        return not self.active
    
    def transmit(self,position):
        self.active = True
        self.nodeTransmitPos = position
        self.pleft = position
        self.pright = position