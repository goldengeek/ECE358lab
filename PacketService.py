'''
Created on Sep 22, 2014

@author: edmondkwan
'''

class PacketService(object):

    def __init__(self, packetQueue):
        self.tickerCount = 0
        self.idleCount = 0
        self.packetQueue = packetQueue
        self.packetBeingServiced = None
        self.sojournTimeSum = 0
        self.packetServed =0
        
    def updateTick(self):
        self.tickerCount+=1
        self.servicePacket()
        
    def servicePacket(self):
        if self.packetBeingServiced == None:
            #attempt to get a new packet
            self.packetBeingServiced = self.packetQueue.getPacket()

            #no new packet to get, up the count
            if self.packetBeingServiced == None:
                self.idleCount +=1
                #print "service is Idle"
            else:
                self.performServices()
        else:
            self.performServices()

    def performServices(self):
        if self.packetBeingServiced.serviceTime > 0:
            self.packetBeingServiced.serviceTime -= 1
            #print "packet being serviced"
        else:
            #print "packet has finished servicing"
            self.packetBeingServiced.exitedSystemAt = self.tickerCount
            self.sojournTimeSum += self.tickerCount - self.packetBeingServiced.generatedAt
            self.packetServed += 1
            self.packetBeingServiced = None
            
    def getData(self):
        serverIdlePercent = float(self.idleCount)/float(self.tickerCount)
        if self.packetServed != 0:
            aveSojournTime = float(self.sojournTimeSum)/self.packetServed
        aveSojournTime = 0        
        return (serverIdlePercent, aveSojournTime)