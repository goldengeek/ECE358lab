'''
Created on Oct 26, 2014

@author: edmondkwan
'''

import random
import math
from math import log
from ECE358.Lab2.Packet import Packet

class NetworkNode(object):
    def __init__(self,medium, sendingProb, packetsPerSec, secPerTick, position):
        self.sendingProb = sendingProb
        self.packetsPerSec = packetsPerSec
        self.failCount = 0
        self.state = 0 # 0 = default, 1 = in waiting loop to send, 2 = sensing medium, 3 = idle, 4 = busy
        self.tickCount = 0
        self.secPerTick = secPerTick
        self.position = position
        self.genNextPacketAt = self.computeNextPacketTick()
        self.packetQueue = []
        self.medium = medium
        
        self.sendingPacket = None
        self.mediumIdleCount = 0
        self.bitTime1 = (1.0/self.medium.speedOfLan)/float(self.secPerTick) #in ticks
        self.bitTime92 = 92*self.bitTime1
        pass
    
    def updateTick(self):
        self.tickCount+=1
        if self.tickCount >= self.genNextPacketAt:
            self.genPacket()
            self.genPacketAt = self.computeNextPacketTick()
        if self.state == 2 and self.mediumIdleCount<=self.bitTime92:
            self.mediumIdleCount+=1
            idleness = self.isMediumIdle()
            if idleness == False:
                state = 3
        
            
    def genPacket(self):
        packet = Packet(self.tickCount)
        self.packetQueue.append(packet)
        if (self.state == 0 or self.state == 1) and len(self.packetQueue) >0:
            self.sendingPacket = self.packetQueue[0]
            self.packetQueue = self.packetQueue[1:]
        
    def recieveDataFromUpperLayer(self):
        self.failCount = 0
        #self.state = 0
        while(True):
            if self.state == 1 or self.state == 0:
                self.state = 2
                break
            #if self.isMediumIdle():
                randNum = random.uniform(0,1)
                if randNum > self.sendingProb:
                    self.transmitData()
                    break
                else:
                    self.waitOneSlot()
                    self.state = 1
            elif self.state == 1:
                self.BEB()
                
    def transmitData(self):
        pass
    
    def BEB(self):
        randNum = random.uniform(0, math.pow(2, self.failCount-1))
        for i in range(0, randNum*512):
            self.waitOneSlot()
    
    def waitOneSlot(self):
        #wait one slot
        return
    
    def isMediumIdle(self):
        #wait 96 bit time
        pLeft = self.medium.pleft
        pRight = self.medium.pright
        
        if self.position >= pLeft and self.position<= pRight:
            return False
        else:
            return True
    
    def computeNextPacketTick(self):
        randNum = random.uniform(0,1)
        deltaTime = (-1.0/float(self.packetPerSec))*log(1-randNum)
        nextGenTick = int(deltaTime*(1/self.secPerTick)) + self.tickCounter
        if int(deltaTime*(1/self.secPerTick)) == 0:
            nextGenTick = self.tickCounter
        return nextGenTick
    

        