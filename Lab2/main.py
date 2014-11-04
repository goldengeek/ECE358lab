'''
Created on Oct 26, 2014

@author: edmondkwan
'''
import argparse
from NetworkNode import NetworkNode
from Medium import Medium
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--NumOfNodes', '-N', type=int, help="")
    parser.add_argument('--DataPacketPerSecond', '-A', type=int, help="")
    parser.add_argument('--SpeedOfLan', '-W', type=int, help="")
    parser.add_argument('--packetLength', '-L', type=int, help="")
    parser.add_argument('--PersistenceParam', '-P', type=float, help="")  #prob of sending if idle
    parser.add_argument('--Ticks', '-T', type=float, help="")  #prob of sending if idle
    parser.add_argument('--secPerTick', '-S', type=float, help="")  #prob of sending if idle
    args = parser.parse_args()
    
    secPerTick = 0.000001

    if args.NumOfNodes:
        numberOfNodes = args.NumOfNodes
    else:
        print 'Missing -N arg'
        sys.exit()
    if args.DataPacketPerSecond:
        packetsPerSecond = args.DataPacketPerSecond
    else:
        print "missing -A arg"
        sys.exit()
    if args.SpeedOfLan:
        speedOfLan = args.SpeedOfLan
    else:
        print "Missing -W arg"
        sys.exit()
    if args.packetLength:
        packetLength = args.packetLength
    else:
        print "missing -L arg"
        sys.exit()
    if args.PersistenceParam:
        sendingProb = args.PersistenceParam
    else:
        print "Missing -P arg"
        sys.exit()
    if args.Ticks:
        ticks = args.Ticks
    else:
        print "Missing -T arg"
        sys.exit()
    if args.secPerTick:
        secPerTick = args.secPerTick
    else:
        print "Missing -S arg"
        sys.exit()
    
    medium = Medium(secPerTick, speedOfLan,numberOfNodes)
    
    nodes = []
    for i in range(numberOfNodes):
        node = NetworkNode(medium, sendingProb, packetsPerSecond, secPerTick, (i+1)*10)
        nodes.append(node)
    
    count = 0
    for i in range(int(ticks)):
        for node in nodes:
            node.updateTick()
        medium.updateTick()
        if i % 1000000 == 0:
            print "{0} Million Ticks Are done".format(count)
            count +=1
    
    medium.printData()
    
    Total_sum = 0
    Total_dropped = 0
    Total_sent = 0
    for node in nodes:
        totalGen, dropped, sent = node.getData()
        Total_sum += totalGen
        Total_dropped += dropped
        Total_sent += sent
        
    print "total number of packets Generated: {0}".format(Total_sum)
    print "total number of packets Sent: {0}".format(Total_sent)
    print "total number of packets dropped: {0}".format(Total_dropped)
            
    