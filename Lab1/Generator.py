'''
Created on Sep 22, 2014

@author: edmondkwan
'''
import random
from Packet import Packet
from PacketQueue import PacketQueue 
from math import log as ln
import time

class Generator(object):
    def __init__(self, packetQueue, packetsPerSec, packetServiceTime, secPerTick):
        self.packetQueue = packetQueue
        self.tickCounter = 0
        self.packetPerSec = packetsPerSec
        self.totalGenPacket = 0
        self.packetServiceTime = packetServiceTime
        self.secPerTick = secPerTick
        
        self.genPacket()
        self.genPacketAt = self.computeNextPacketTick()
        
        self.debugCount = 0
        self.debugTime = time.time()
    
    def updateTick(self):
        self.tickCounter += 1
        if self.tickCounter >= self.genPacketAt:
            self.genPacket()
            self.genPacketAt = self.computeNextPacketTick()
        if self.tickCounter % 1000000 == 0:
            self.debugCount +=1
            print "{0} Million Ticks recieved in {1} seconds".format(self.debugCount, (time.time()-self.debugTime))
        #print "tick count {0}".format(self.tickCounter)
            
    def computeNextPacketTick(self):
        randNum = random.uniform(0,1)
        deltaTime = (-1.0/float(self.packetPerSec))*ln(1-randNum)
        nextGenTick = int(deltaTime*(1/self.secPerTick)) + self.tickCounter
        if int(deltaTime*(1/self.secPerTick)) == 0:
            nextGenTick = self.tickCounter
        
        #print "next packet generating at {0}".format(nextGenTick)
        return nextGenTick
    
    def genPacket(self):
        packet = Packet(self.tickCounter, self.packetServiceTime) 
        self.totalGenPacket += 1
        self.sendPacket(packet)
        #print "generatring new Packet"
        
    def sendPacket(self, packet):
        self.packetQueue.send(packet)
        #print "sending packet to Queue"
        
    def getData (self):
        return (self.totalGenPacket, self.tickCounter)