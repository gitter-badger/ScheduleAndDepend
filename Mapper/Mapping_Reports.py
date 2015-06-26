# Copyright (C) 2015 Siavoosh Payandeh Azad
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from ConfigAndPackages import Config
from ArchGraphUtilities import AG_Functions
import random, networkx

def ReportMapping(AG, logging):
    logging.info("===========================================")
    logging.info("      REPORTING MAPPING RESULT")
    logging.info("===========================================")
    for Node in AG.nodes():
        logging.info("NODE:"+str(Node)+"CONTAINS:"+str(AG.node[Node]['MappedTasks']))
    for link in AG.edges():
         logging.info("LINK:"+str(link)+"CONTAINS:"+str(AG.edge[link[0]][link[1]]['MappedTasks']))
    return None

def DrawMappingDistribution(AG, SHM):
    fig_Num = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    fig_Util = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    MaxNumberOfTasks = 0
    MaxUtilization = 0
    for node in AG.nodes():
        MaxNumberOfTasks = max(len(AG.node[node]['MappedTasks']), MaxNumberOfTasks)
        MaxUtilization = max(AG.node[node]['Utilization'], MaxUtilization)

    for node in AG.nodes():
        Location = AG_Functions.ReturnNodeLocation(node)
        XSize= float(Config.Network_X_Size)
        YSize= float(Config.Network_Y_Size)
        Num = 255*len(AG.node[node]['MappedTasks'])/float(MaxNumberOfTasks)
        Util = 255*AG.node[node]['Utilization']/float(MaxUtilization)
        if SHM.SHM.node[node]['NodeHealth']:
            color = '#%02X%02X%02X' % (255, 255-Num, 255-Num)
        else:   # node is broken
            color = '#7B747B'
        fig_Num.gca().add_patch(patches.Rectangle((Location[0]/XSize, Location[1]/YSize),
                                               width=0.15, height=0.15, facecolor=color,
                                               edgecolor="black", linewidth=3))
        if SHM.SHM.node[node]['NodeHealth']:
            color = '#%02X%02X%02X' % (255, 255-Util, 255-Util)
        else:   # node is broken
            color = '#7B747B'
        fig_Util.gca().add_patch(patches.Rectangle((Location[0]/XSize, Location[1]/YSize),
                                               width=0.15, height=0.15, facecolor=color,
                                               edgecolor="black", linewidth=3))

    fig_Num.text(0.25, 0.03, 'Distribution of number of the tasks on the network', fontsize=35)
    fig_Util.text(0.25, 0.03, 'Distribution of utilization of network nodes', fontsize=35)
    fig_Num.savefig("GraphDrawings/Mapping_Num.png")
    fig_Util.savefig("GraphDrawings/Mapping_Util.png")
    fig_Num.clf()
    fig_Util.clf()
    return None


def DrawMapping(TG, AG, SHM):
    """
    This function draws the tasks on tiles of network. this would be very useful to check how our
    mapping optimization is acting...
    :param TG: Task Graph
    :param AG: Architecture Graph
    :param SHM: System Health Management
    :return: None
    """
    fig = plt.figure(figsize=(4*Config.Network_X_Size, 4*Config.Network_Y_Size))
    ColorList = []
    POS = {}
    for node in AG.nodes():
        Location = AG_Functions.ReturnNodeLocation(node)
        XSize = float(Config.Network_X_Size)
        YSize = float(Config.Network_Y_Size)
        if SHM.SHM.node[node]['NodeHealth']:
            if Config.EnablePartitioning:
                if node in Config.CriticalRegionNodes:
                    color = '#FF878B'
                elif node in Config.GateToNonCritical:
                    color = '#928AFF'
                elif node in Config.GateToCritical:
                    color = '#FFC29C'
                else:
                    color = 'white'
            else:
                color = 'white'
        else:   # node is broken
            color = '#7B747B'
        fig.gca().add_patch(patches.Rectangle((Location[0]/XSize, Location[1]/YSize),
                                               width=0.15, height=0.15, facecolor=color,
                                               edgecolor="black", linewidth=3, alpha= 0.5))
        OffsetX = 0
        OffsetY = 0.02
        TaskCount = 0
        for task in AG.node[node]['MappedTasks']:
            TaskCount += 1
            OffsetX += 0.03
            if TaskCount == 5:
                TaskCount = 0
                OffsetX = 0.03
                OffsetY += 0.03
            random.seed(task)
            r = random.randrange(0,255)
            g = random.randrange(0,255)
            b = random.randrange(0,255)
            color = '#%02X%02X%02X' % (r,g,b)
            ColorList.append(color)
            POS[task]=(Location[0]/XSize+OffsetX, Location[1]/YSize+OffsetY)

    networkx.draw(TG, POS, with_labels=True, node_size=700, node_color=ColorList, width=0, alpha = 0.5)
    fig.text(0.25, 0.02, 'Mapping visualization for network nodes', fontsize=35)
    fig.savefig("GraphDrawings/Mapping.png")
    fig.clf()
    return None