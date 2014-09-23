'''
Created on Sep 22, 2014

@author: edmondkwan
'''
from Packet import Packet

class PacketQueue(object):

    def __init__(self, size):
        self.size = size
        self.queue = []
        
    def send (self, packet):
        if self.size != 0:
            if len(self.queue) < self.size:
                self.queue.append(packet)
                print "packet Queue being added to"
        else:
            self.queue.append(packet)
            print "packet Queue being added to"
    
    def getPacket(self):
        if len (self.queue) >0:
            packet = self.queue[0]
            self.queue = self.queue[1:]
        else:
            return None
            print "packet queue empty"
        print "returning packet"
        return packet
        