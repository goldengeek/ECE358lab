'''
Created on Oct 26, 2014

@author: edmondkwan
'''

import random
import math
from math import log
from Packet import Packet
from Medium import Medium


class NetworkNode(object):
    def __init__(self,medium, sendingProb, packetsPerSec, secPerTick, position):
        self.sendingProb = sendingProb
        self.packetsPerSec = packetsPerSec
        self.failCount = 0
        self.state = 0 # 0 = default, 1 = check medium , 2 = medium not busy for 92 bit time, 3 secondary 96 bit time wait, 4 secondary not busy, 5 check collision,6 Jamming Signal
        self.tickCount = 0
        self.secPerTick = secPerTick
        self.position = position
        self.genNextPacketAt = self.computeNextPacketTick()
        self.packetQueue = []
        self.medium = medium
        self.prevTR = 0
        
        self.waitState = False
        self.waitLength = 0
        self.sendingPacket = None
        self.mediumIdleCount = 0
        self.bitTime1 = (1.0/self.medium.speedOfLan)/float(self.secPerTick) #in ticks
        self.bitTime92 = 92*self.bitTime1
        
        self.dropdPacket = 0
        self.packetGenerated = 0
        self.sentPackets = 0
        pass
    
    def updateTick(self):
        self.tickCount+=1
            
        if self.tickCount >= self.genNextPacketAt:
            self.packetGenerated += 1
            self.genPacket()
            self.genNextPacketAt = self.computeNextPacketTick()
        
        if self.waitState and self.waitLength>0:
            self.waitLength -= 1
            return
        if self.waitState and self.waitLength <=0:
            self.waitState = False
            self.waitLength = 0
          
        if self.state == 0 and len(self.packetQueue)>0:
            self.failCount = 0
            self.recieveDataFromUpperLayer()  
        elif (self.state == 1 or self.state == 3) and self.mediumIdleCount<=self.bitTime92:
            self.mediumIdleCount+=1
            if not self.isMediumIdle():
                #chceck state, its not going in to BEB
                self.mediumIdleCount = 0
                if self.sendingProb == 0:
                    self.waitState = True
                    self.state = 1
                    self.waitLength = self.prevTR
                if self.state == 3:
                    self.state = 1 
                    self.BEB()
        elif (self.state == 1 or self.state == 3) and self.mediumIdleCount >self.bitTime92:
            self.mediumIdleCount = 0
            if self.state == 1:
                self.state = 2
            if self.state == 3:
                self.state = 4
            self.recieveDataFromUpperLayer()
        elif self.state == 5 and self.waitLength >0:
            self.waitLength -=1
            #if self.medium.collision:
            if self.medium.didCollide():
                #print "NODE COLLIDE"
                self.state = 6
                self.waitLength = 0
                self.SendJamingSignal()
        elif self.state == 5 and self.waitLength <=0:
            #YAY no collision
            self.failCount = 0
            self.sendingPacket = None
            self.state = 0
            self.sentPackets += 1
            pass
        elif self.state == 6 and self.waitState == False:
            self.state =1
            self.BEB()
 
    def computeNextPacketTick(self):
        randNum = random.uniform(0,1)
        deltaTime = (-1.0/float(self.packetsPerSec))*log(1-randNum)
        nextGenTick = int(deltaTime*(1/self.secPerTick)) + self.tickCount
        if int(deltaTime*(1/self.secPerTick)) == 0:
            nextGenTick = self.tickCount
        return nextGenTick
    
           
    def genPacket(self):
        packet = Packet(self.tickCount, 1500*8, self.position)
        self.packetQueue.append(packet)
        #if (self.state == 0) and len(self.packetQueue) >0:
            #self.sendingPacket = self.packetQueue[0]
            #self.packetQueue = self.packetQueue[1:]
            #self.recieveDataFromUpperLayer()
        
    def recieveDataFromUpperLayer(self):
        #print 'In Recieved Data From Upper Layer. Current State is {0}'.format(self.state)
        #self.failCount = 0
        #self.state = 0
        #while(True):
            if self.state == 0:
                self.state = 1
                #break
            #if self.isMediumIdle():
            if self.state == 2 or self.state == 4:
                randNum = random.uniform(0,1)
                #CHECK THIS, should be oppsoite
                if randNum < self.sendingProb or self.sendingProb == 1 or self.sendingProb == 0:
                    self.transmitData()
                    #break
                else:
                    if self.state == 2:
                        self.waitOneSlot()
                        self.state = 3
                    if self.state == 4:
                        self.state = 1
                        self.BEB()
                    #break
                
    def transmitData(self):
        #print 'Transmitting packet on to medium. Current State is {0}'.format(self.state)
        if self.sendingPacket == None:
            self.sendingPacket = self.packetQueue[0]
            self.packetQueue = self.packetQueue[1:]
        self.medium.transmit(self.position, self.sendingPacket)
        self.state = 5 #check for collision
        #self.waitLength = (float(self.sendingPacket.length)/float(self.medium.speedOfLan))*(1.0/self.secPerTick)
        self.waitLength = (float(1500*8)/float(self.medium.speedOfLan))*(1.0/self.secPerTick)
        
        #Fifure  out if we are sending to position 0, 1 or whatever..
    
    def BEB(self):
        self.failCount += 1
        if self.failCount > 10:
            #drop packet
            self.sendingPacket = None
            self.waitState = False
            self.state = 0
            self.failCount = 0
            self.dropdPacket += 1
            return
        self.waitState = True
        randNum = random.uniform(0, math.pow(2, self.failCount-1))
        self.waitLength = randNum*self.bitTime1*512
        #print self.waitLength
        self.prevTR = self.waitLength
        #print self.waitLength
    
    def SendJamingSignal(self):
        self.waitState = True
        self.waitLength = 48*self.bitTime1
    
    def waitOneSlot(self):
        self.waitState = True
        self.waitLength = self.bitTime1
        return
    
    def isMediumIdle(self):
        #wait 96 bit time
        return self.medium.isMediumIdle(self.position)
    
    def getData(self):
        return (self.packetGenerated, self.dropdPacket, self.sentPackets)
    

    