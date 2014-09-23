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
            self.packetBeingServiced = self.packetQueue.getPacket()
            self.idleCount +=1
            print "service is Idle"
        else:
            self.packetBeingServiced.serviceTime -= 1
            print "packet being serviced"
            
        