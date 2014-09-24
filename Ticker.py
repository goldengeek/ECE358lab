'''
Created on Sep 22, 2014

@author: edmondkwan
'''
from threading import Thread
from PacketService import PacketService

class Ticker(Thread):
    
    def __init__(self, event, Generator, PacketService, packetQueue, totalTicks,secondPerTick, rounds):
        Thread.__init__(self)
        self.stopped = event
        self.generator = Generator
        self.packetService = PacketService
        self.packetQueue = packetQueue
        self.totalTicks = totalTicks
        self.secondPerTick = secondPerTick
        self.rounds = rounds
        
    def collectData(self):
        totalGeneratedPackets, totalGenTicks = self.generator.getData()
        totalDroppedPackets, aveQueueLength, aveQueueFullness = self.packetQueue.getData()
        serverIdlePercent, aveSojournTime = self.packetService.getData()    
        
        print '-'*60
        print "Total number of packet Generated in {0} ticks are: {1}".format(totalGenTicks,totalGeneratedPackets)
        print "Total Packets Dropped: {0}".format(totalDroppedPackets)
        print "Percent of Dropped packet: {0} %".format(float(totalDroppedPackets)*100/totalGeneratedPackets)
        print "Average Queue Length: {0}".format(aveQueueLength)
        print "Average Queue Fullness: {0} %".format(aveQueueFullness*100)
        print "Average Idle percent: {0} %".format(serverIdlePercent*100)
        print "Average Sojourn Time per packet in ticks: {0}".format(aveSojournTime)
    
    
    def run(self):
        for i in range(0, self.rounds):
            tickCount =0
            while not self.stopped.wait(self.secondPerTick):
                self.generator.updateTick()
                self.packetService.updateTick()
                self.packetQueue.updateTick()
                tickCount +=1
                if tickCount >= self.totalTicks:
                    break
                #print tickCount
            self.collectData()
            self.resetService()
        return 
            # call a function
    
    def resetService(self):
        self.generator.totalGenPacket = 0
        self.generator.tickCounter = 0
        self.packetQueue.droppedPacket = 0
        self.packetQueue.tickerCount = 0
        self.packetQueue.queue=[]
        self.packetService.packetBeingServiced = None
        self.packetService.tickerCount = 0
        self.packetService.idleCount = 0
        
