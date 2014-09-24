'''
Created on Sep 22, 2014

@author: edmondkwan
sojourn Time, how to do dropped packets? make it zero, do i count?
'''

from Generator import Generator 
from Packet import Packet
from PacketQueue import PacketQueue
from PacketService import PacketService
from Ticker import Ticker
import time
from threading import Timer, Event
import sys , re
import argparse

def isNum (str):
    if re.match("[0-9]+", str):
        return True
    else:
        return False

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--TICKS', type=int, help="total number of ticks per cycle")
    parser.add_argument('--rounds', '-M', type=int, help="total number of rounds")
    parser.add_argument('--lamb','-la', type=int, help='average number of packets per second ')
    parser.add_argument('--length','-L', type=int, help='length of packet in bis')
    parser.add_argument('--serviceSpeed', '-C', type=int, help ='the service time recieved by packet. Value is a tranmission rate in bits/second')
    parser.add_argument('--sizeOfQueue','-K', type=int, help='the size of Queue, if this option is left out the queue is of infintie size')
    parser.add_argument('--secondsPerTick', '-st', type=float, help='seconds per each tick')
    args = parser.parse_args()
    
    secPerTick = 0.000001
    if args.secondsPerTick:
        secPerTick = args.secondsPerTick
    rounds = 1
    if args.rounds and args.rounds >1:
        rounds = args.rounds
    if not args.TICKS:
        print "missing TICKS argument"
        sys.exit()
    if not args.lamb:
        print "missing lamb argument"
        sys.exit()
    packetsPerSec = args.lamb
    if not args.length:
        print "missing length argument"
        sys.exit()
    lengthOfPacketInBits = args.length
    if not args.serviceSpeed:
        print "missing C argument"
        sys.exit()
    serviceSpeed = args.serviceSpeed
    if args.sizeOfQueue:
        sizeOfQueue = args.sizeOfQueue
    else:
        sizeOfQueue = 0
        
    packetServiceTime = (float(lengthOfPacketInBits)/(serviceSpeed))*(1.0/secPerTick)
    print "length of packet in bit", lengthOfPacketInBits
    print "service speed", serviceSpeed
    print "seconds per tic", secPerTick
    print 'service time in tick', packetServiceTime
    if packetServiceTime ==0:
        packetService =10
    
    packetQueue = PacketQueue(sizeOfQueue) 
    packetService = PacketService(packetQueue)
    generator = Generator(packetQueue, packetsPerSec, packetServiceTime)
    
    stopFlag = Event()
    thread = Ticker(stopFlag, generator, packetService, packetQueue,args.TICKS,secPerTick, rounds)
    thread.start()
    
        
    
    