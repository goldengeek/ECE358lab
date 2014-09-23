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
                print "service is Idle"
            else:
                self.performServices()
        else:
            self.performServices()

    def performServices(self):
        if self.packetBeingServiced.serviceTime > 0:
            self.packetBeingServiced.serviceTime -= 1
            print "packet being serviced"
        else:
            print "packet has finished servicing"
            self.packetBeingServiced = None