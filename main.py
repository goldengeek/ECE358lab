'''
Created on Sep 22, 2014

@author: edmondkwan
'''

from Generator import Generator 
from Packet import Packet
from PacketQueue import PacketQueue
from PacketService import PacketService
from Ticker import Ticker
import time
from threading import Timer, Event


if __name__ == '__main__':
    packetsPerSec = 100
    packetQueue = PacketQueue(100) 
    packetService = PacketService(packetQueue)
    generator = Generator(packetQueue, packetsPerSec)
    stopFlag = Event()
    thread = Ticker(stopFlag, generator, packetService)
    thread.start()
    