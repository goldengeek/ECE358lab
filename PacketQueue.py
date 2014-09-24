'''
Created on Sep 22, 2014

@author: edmondkwan
'''
from Packet import Packet

class PacketQueue(object):

    def __init__(self, size):
        self.size = size
        self.droppedPacket = 0
        self.tickCounter = 0
        self.sumOfSizeOfQueuePerTick = 0
        self.queue = []
    
    def updateTick(self):
        self.tickCounter +=1
        self.sumOfSizeOfQueuePerTick += len(self.queue)
    
    def send (self, packet):
        if self.size != 0:
            if len(self.queue) < self.size:
                self.queue.append(packet)
                #print "packet Queue being added to"
            else:
                #print "packet being dropped"
                self.droppedPacket +=1
        else:
            self.queue.append(packet)
            #print "packet Queue being added to"
        #print "size of queue: {0}".format(len(self.queue))
    
    def getPacket(self):
        if len (self.queue) >0:
            packet = self.queue[0]
            self.queue = self.queue[1:]
        else:
            return None
            #print "packet queue empty"
        #print "returning packet"
        #print "size of queue: {0}".format(len(self.queue))
        return packet
    
    def getData(self):
        aveQueueLength = float(self.sumOfSizeOfQueuePerTick)/float(self.tickCounter)
        if self.size == 0:
            aveQueueFullness = 0
        else:
            aveQueueFullness = aveQueueLength/self.size
        return (self.droppedPacket, aveQueueLength, aveQueueFullness)
        