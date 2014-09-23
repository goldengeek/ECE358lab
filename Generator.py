'''
Created on Sep 22, 2014

@author: edmondkwan
'''
import random
from Packet import Packet
from PacketQueue import PacketQueue 
from math import log as ln

class Generator(object):
    def __init__(self, packetQueue, packetsPerSec):
        self.packetQueue = packetQueue
        self.tickCounter = 0
        self.packetPerSec = packetsPerSec
        
        self.genPacket()
        self.genPacketAt = self.computeNextPacketTick()
    
    def updateTick(self):
        self.tickCounter += 1
        if self.tickCounter == self.genPacketAt:
            self.genPacket()
            self.genPacketAt = self.computeNextPacketTick()
        print "tick count {0}".format(self.tickCounter)
            
    def computeNextPacketTick(self):
        randNum = random.uniform(0,1)
        print randNum
        deltaTime = (-1.0/float(self.packetPerSec))*ln(1-randNum)
        nextGenTick = int(deltaTime*10000) + self.tickCounter
        print "next packet generating at {0}".format(nextGenTick)
        return nextGenTick
    
    def genPacket(self):
        packet = Packet(self.tickCounter, 10) 
        self.sendPacket(packet)
        print "generatring new Packet"
        
    def sendPacket(self, packet):
        self.packetQueue.send(packet)
        print "sending packet to Queue"