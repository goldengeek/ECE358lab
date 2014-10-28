'''
Created on Oct 26, 2014

@author: edmondkwan
'''
import argparse
from ECE358.Lab2.NetworkNode import NetworkNode
from ECE358.Lab2.Medium import Medium


if '__name__' == '__main__':
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
    
    numberOfNodes = args.NumOfNodes
    packetsPerSecond = args.DataPacetPerSecond
    speedOfLan = args.SpeedOfLan
    packetLength = args.packetLength
    sendingProb = args.PersistenceParam
    ticks = args.Ticks
    secPerTick = args.secPerTick
    
    medium = Medium(secPerTick, speedOfLan)
    
    nodes = []
    for i in range(numberOfNodes):
        node = NetworkNode(medium, sendingProb, secPerTick, i*10)
        nodes.append(node)
    
    for i in range(ticks):
        
    