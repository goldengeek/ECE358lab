'''
Created on Sep 22, 2014

@author: edmondkwan
'''
from threading import Thread
from PacketService import PacketService

class Ticker(Thread):
    
    def __init__(self, event, Generator, PacketService):
        Thread.__init__(self)
        self.stopped = event
        self.generator = Generator
        self.packetService = PacketService

    def run(self):
        while not self.stopped.wait(1):
            self.generator.updateTick()
            self.packetService.updateTick()
            
            # call a function
    
        