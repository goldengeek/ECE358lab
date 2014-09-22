'''
Created on Sep 22, 2014

@author: edmondkwan
'''

from Generator import Generator 
from Packet import Packet
from PacketQueue import PacketQueue
from PacketService import PacketService
import time
from threading import Timer

generator = Generator()

def print_time():
    print time.time()

def ticker():
    while True:
        print time.time()
        Timer(5,generator.updateTick,()).start()


if __name__ == '__main__':
    ticker()
    pass
