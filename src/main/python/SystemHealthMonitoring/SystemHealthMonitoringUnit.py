# Copyright (C) 2015 Siavoosh Payandeh Azad

import networkx
import hashlib
import copy
import re
from Mapper import Mapping_Functions
import SHMU_Functions
from ConfigAndPackages import Config
import random


class SystemHealthMonitoringUnit:
    def __init__(self):
        self.SHM = networkx.DiGraph()   # System Health Map
        self.SnapShot = None
        self.MPM = {}                     # Most Probable Mapping Lib

    def setup_noc_shm(self, ag, turns_health):
        print ("===========================================")
        print ("PREPARING SYSTEM HEALTH MAP...")
        if not Config.SetRoutingFromFile:
            for node in ag.nodes():
                self.SHM.add_node(node, TurnsHealth=copy.deepcopy(turns_health), NodeHealth=True, NodeSpeed=100,
                                  RouterTemp=10, NodeTemp=random.randint(0, Config.MaxTemp))
        else:
            try:
                RoutingFile = open(Config.RoutingFilePath, 'r')
            except IOError:
                print ('CAN NOT OPEN', Config.RoutingFilePath)

            while True:
                line = RoutingFile.readline()
                if "Ports" in line:
                    ports = RoutingFile.readline()
                    port_list = ports.split()
                    print ("port_list:", port_list)
                if "Node" in line:
                    NodeID = int(re.search(r'\d+', line).group())
                    node_turns_health = copy.deepcopy(turns_health)
                    line = RoutingFile.readline()
                    turns_list = line.split()
                    for turn in node_turns_health.keys():
                        if turn not in turns_list:
                            node_turns_health[turn] = False
                    self.SHM.add_node(NodeID, TurnsHealth=copy.deepcopy(node_turns_health), NodeHealth=True,
                                      NodeSpeed=100, RouterTemp=0, NodeTemp=0)
                if line == '':
                    break
            for node in ag.nodes():
                if node not in self.SHM.nodes():
                    self.SHM.add_node(node, TurnsHealth=copy.deepcopy(turns_health), NodeHealth=True,
                                      NodeSpeed=100, RouterTemp=0, NodeTemp=0)
        for link in ag.edges():
            self.SHM.add_edge(link[0], link[1], LinkHealth=True)
        print ("SYSTEM HEALTH MAP CREATED...")

    ##################################################
    def break_link(self, link, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m BREAKING LINK: "+str(link))
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = False

    def restore_broken_link(self, link, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m LINK: "+str(link)+" RESTORED...")
        self.SHM.edge[link[0]][link[1]]['LinkHealth'] = True

    ##################################################
    def break_turn(self, node, turn, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m BREAKING TURN: "+str(turn)+" IN NODE "+str(node))
        self.SHM.node[node]['TurnsHealth'][turn] = False

    def restore_broken_turn(self, node, turn, report):
        if report:
            print ("===========================================")
            print ("\033[33mSHM::\033[0m TURN:"+str(turn)+" IN NODE"+str(node)+" RESTORED")
        self.SHM.node[node]['TurnsHealth'][turn] = True

    ##################################################
    def introduce_aging(self, node, speed_down, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeSpeed'] *= 1-speed_down
        if report:
            print ("\033[33mSHM::\033[0m AGEING NODE:"+str(node)+" ... SPEED DROPPED TO: " +
                   str(self.SHM.node[node]['NodeSpeed'])+" %")
        if self.SHM.node[node]['NodeSpeed'] == 0:
            self.break_node(node, True)

    ##################################################
    def break_node(self, node, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeHealth'] = False
        if report:
            print ("\033[33mSHM::\033[0m NODE "+str(node)+" IS BROKEN...")

    def restore_broken_node(self, node, report):
        if report:
            print ("===========================================")
        self.SHM.node[node]['NodeHealth'] = True
        if report:
            print ("\033[33mSHM::\033[0m NODE "+str(node)+" IS RESTORED...")

    ##################################################
    def TakeSnapShotOfSystemHealth(self):
        self.SnapShot = copy.deepcopy(self.SHM)
        print ("A SNAPSHOT OF SYSTEM HEALTH HAS BEEN STORED...")
        return None

    ##################################################
    def RestoreToPreviousSnapShot(self):
        self.SHM = copy.deepcopy(self.SnapShot)
        print ("SYSTEM HEALTH MAP HAS BEEN RESTORED TO PREVIOUS SNAPSHOT...")
        self.SnapShot = None
        return None

    ##################################################
    def AddCurrentMappingToMPM(self, tg):
        """
        Adds a mapping (Extracted from TG) under a fault configuration to MPM.
        The dictionary key would be the hash of fault config
        :param tg: Task Graph
        :return: None
        """
        MappingString = Mapping_Functions.mapping_into_string(tg)
        self.MPM[hashlib.md5(SHMU_Functions.GenerateFaultConfig(self)).hexdigest()] = MappingString
        return None

    ##################################################
    def CleanMPM(self):
        self.MPM = {}
        return None

    def UpdateNodeTemp(self, node, temp):
        """
        Will update a Node's temperature.
        :param node: Node ID Number
        :param temp: Temperature in centigrade
        :return: True if Node is healthy and temp update is successful and False if Not!
        """
        if self.SHM.node[node]['NodeHealth']:
            self.SHM.node[node]['NodeTemp'] = temp
            return True
        else:
            return False

    def UpdateRouterTemp(self, node, temp):
        """
        Will update a Router's temperature.
        :param node: Node ID Number
        :param temp: Temperature in centigrade
        :return: None
        """
        self.SHM.node[node]['RouterTemp'] = temp
        return None

    ##################################################
    # ToDO: To implement the classification algorithm