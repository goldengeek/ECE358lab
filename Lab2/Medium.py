'''
Created on Oct 26, 2014

@author: edmondkwan
'''
import math



class Medium(object):
    def __init__(self, secPerTick, speedOfLan, lengthOfWireInNodes):
        self.active = False
        self.JamState = False
        self.collision = False
        self.tickCount = 0
        self.lengthOfWireInNodes = lengthOfWireInNodes
        self.nodeTransmitPos = 0
        self.propSpeed = 200000000
        #self.propSpeed = 100
        self.propTime =(10.0/self.propSpeed)*(1.0/secPerTick)
        self.secPerTick = secPerTick
        self.speedOfLan = speedOfLan
        
        self.waitLenght = 0
        self.bitTime1 = (1.0/self.speedOfLan)/float(self.secPerTick)
        
        
        self.position = []
        self.pLeft = []
        self.pRight = []
        self.propCount = []
        self.packetsInLan = []
        self.packetFinishTime = []
        
        self.packetDelayTime = []
        self.collisionCount = 0
        
    
    def updateTick(self):
        self.tickCount +=1
        if self.JamState and self.waitLenght <= self.bitTime1 *48:
            self.waitLenght += 1
            return
        if self.JamState and self.waitLenght > self.bitTime1 * 48:
            self.waitLenght = 0
            self.JamState = False
            self.active = False
        if self.active == True:
            for b in range(len(self.packetsInLan)):
                self.propCount[b]+=1
                if self.propCount[b] < self.propTime:
                    self.pLeft[b] -= int(self.propCount[b]/self.propTime)
                    self.pRight[b] += int(self.propCount[b]/self.propTime)
                    self.propCount[b] = 0
            
                 
            i = 0
            while i <len(self.packetsInLan):
            #for i in range(len(self.packetsInLan)):
                
                #if self.packetFinishTime[i]>=self.tickCount:
                #print len(self.packetsInLan)
                while len(self.packetsInLan)>0 and i<len(self.packetsInLan) and self.packetFinishTime[i]<=self.tickCount:
                    #print len(self.packetFinishTime),len(self.packetsInLan), i
                    #print type(self.packetsInLan[i])
                    #print len(self.packetsInLan)
                    
                    #print i, len(self.packetsInLan)
                    #print self.packetFinishTime[i], self.tickCount
                    self.packetDelayTime.append(self.tickCount - self.packetsInLan[i].generatedAt)
                    del self.pLeft[i]
                    del self.pRight[i]
                    del self.propCount[i]
                    del self.packetsInLan[i]
                    del self.packetFinishTime[i]
                    
                    if len(self.packetsInLan) <=0:
                        #nothing is in lan. acive is now false
                        self.active = False
                i +=1
            #print len(self.packetsInLan)
            for i in range(len(self.packetsInLan)):
                for b in range (len(self.packetsInLan)):
                    if b == i:
                        pass
                    #print self.position[i], self.pLeft[b], self.pRight[b]
                    if self.position[i] >= self.pLeft[b] and self.position[i] <= self.pRight[b]:
                        self.collision = True
                        
            if self.collision:
                self.position = []
                self.pLeft = []
                self.pRight = []
                self.propCount = []
                self.packetsInLan = []
                self.active = True
                self.JamState = True
                self.collisionCount +=1
    def isMediumIdle(self, position):
        if self.JamState:
            return False
        for i in range(len(self.packetsInLan)):
            if position >= self.pLeft[i] and position <= self.pRight[i]:
                return False
        return True
    
    def transmit(self,position, packet):
        self.active = True
        #self.nodeTransmitPos 
        #self.pleft = position
        #self.pright = position
        self.pLeft.append(position)
        self.pRight.append(position)
        self.position.append(position)
        self.packetsInLan.append(packet)
        #packetEndTime = (float(position*10)/float(self.speedOfLan))+float(packet.length)/float(self.speedOfLan)*(1.0/self.secPerTick)
        #packetEndTime = (float(position*10)/float(self.speedOfLan))+float(1500)/float(self.speedOfLan)*(1.0/self.secPerTick)
        packetEndTime = (float(max(position*10, self.lengthOfWireInNodes*10-position*10))/float(self.propSpeed))+(float(1500)/float(self.speedOfLan))
        self.packetFinishTime.append(packetEndTime*(1.0/self.secPerTick)+self.tickCount)
        #print packetEndTime*(1.0/self.secPerTick)+self.tickCount, self.tickCount
        self.propCount.append(0)
        
    def printData(self):
        print "Number of Packets Sent in {1} seconds is {0}".format(len(self.packetDelayTime),self.tickCount*(self.secPerTick))
        print "Number of Collision are {0}".format(self.collisionCount)
        sum =0
        for delay in self.packetDelayTime:
            sum += delay
        print "Average Delay in ticks is {0}".format(sum/len(self.packetDelayTime))
        
    
        