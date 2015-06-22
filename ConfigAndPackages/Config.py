# Copyright (C) 2015 Siavoosh Payandeh Azad
import PackageFile
################################################
#          Debug  Config
################################################
DebugInfo = True
DebugDetails = False
LoGDirectory = "LOGS"
################################################
#          TG  Config
################################################
# TG_Type can be: 'RandomDependent','RandomIndependent','Manual'
TG_Type = 'Manual'
# For Random TG_Type:
NumberOfTasks = 10
NumberOfEdges = 15
WCET_Range = 30
EdgeWeightRange = 7
Release_Range = 5      # task release time range
# The following is only for Manual TG_Type:
# Note::    if you have High-critical tasks in your TG, make sure that you have checked partitioning options for the
#           network.
Task_List = [0, 1, 2, 3, 4, 5, 6, 7]
Task_WCET_List = [30, 30, 20, 40, 10, 5, 15, 20]
Task_Criticality_List = ['H', 'L', 'H', 'L', 'L', 'H', 'L', 'L']
TG_Edge_List = [(1, 2), (1, 3), (2, 5), (0, 5), (4, 7), (4, 3), (1, 6), (0, 6)]
TG_Edge_Weight = [5, 9, 4, 7, 5, 3, 5, 1]
################################################
#          AG  Config
################################################
# AG_Type can be : 'Generic','Manual'
AG_Type = 'Generic'
# Todo: virtual channel
VirtualChannelNum = 0
# in case of Generic AG_type
# available topologies: 2DTorus, 2DMesh, 2DLine, 2DRing
NetworkTopology = '2DMesh'
Network_X_Size = 6
Network_Y_Size = 6
Network_Z_Size = 1

# Only for Manual AG_Type:
PE_List = [0, 1, 2, 3]
AG_Edge_List = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 2), (3, 1)]
# AG_Edge_Port_List shows which port of each router is connected to which port of the other on every link
AG_Edge_Port_List = [('E', 'W'), ('S', 'N'), ('W', 'E'), ('S', 'N'), ('N', 'S'), ('E', 'W'), ('W', 'E'), ('N', 'S')]
################################################
#          Routing  Config
################################################
# Todo: introduce more turn models
# Available Turn Models : 'FULL_TurnModel', 'XY_TurnModel', 'WestFirst_TurnModel', 'NorthLast_TurnModel'
UsedTurnModel = PackageFile.WestFirst_TurnModel
RoutingFilePath = "User_Inputs/RoutingFile.txt"
################################################
#          SHM  Config
################################################
# Do not change if you have conventional 2D NoC
TurnsHealth = PackageFile.TurnsHealth_2DNetwork

# Number of Unreachable-Rectangles
NumberOfRects = 5

# Here you can break things as initial defects...
# For 2X2 network:
# ListOfBrokenLinks = [(0, 1), (0, 2)]

# For 4X4 network:
# ListOfBrokenLinks = [(0, 1), (0, 4)]

# List of broken PE
ListOfBrokenPEs = [1]
# I know its a dictionary
ListOfBrokenTurns = {}
# ListOfBrokenTurns = {1: 'W2S', 2: 'W2S'}

# For aging, we need to give the tool a dictionary of nodes and their speed down...
# so {1: 0.3} means that node 1's speed has decreased by 30% from its current state.
# I know its a dictionary too
ListOfAgedPEs = {1: 0.3, 2: 0.1}
################################################
#          Clustering Function  Config
################################################
ClusteringIteration = 1000

################################################
#          Mapping Function  Config
################################################
# Mapping_Function can be : 'MinMin','MaxMin','MinExecutionTime','MinimumCompletionTime'
#                           'LocalSearch','IterativeLocalSearch',
Mapping_Function = 'LocalSearch'
LocalSearchIteration = 20
IterativeLocalSearchIterations = 20

################################################
#          Scheduling  Config
################################################
SlackCount = 2      # this is used for number of repetitions of the critical tasks
################################################
#           Network Partitioning
################################################
EnablePartitioning = True

if EnablePartitioning:
    # Critical Region Nodes:
    # for 6X6 network example no 2 of ReCoSoc Paper
    CriticalRegionNodes = [16, 17, 21, 22, 23, 28, 29]
    GateToNonCritical = [15, 27]
    GateToCritical = [20]
    # For 6X6 network: (This is the Example scenario no. 2 in ReCoSoC paper)
    ListOfBrokenLinks = [(35, 29), (29, 35), (34, 28), (28, 34), (33, 27), (11, 17), (17, 11), (10, 16), (16, 10),
                         (9, 15), (14, 15), (20, 26), (20, 19), (20, 14), (26, 27)]
    # The virtual broken links for Non critical is not quite right in the ReCoSoC paper for the case of gateways
    # To automatic generation of rectangles for the gateways can be fixed with the following workaround
    # we have to break the links between Gateways and the nodes on the region that gateway should not send
    # data to.
    VirtualBrokenLinksForNonCritical = [(20, 21), (27, 28), (27, 21), (15, 21), (15, 16)]
    VirtualBrokenLinksForCritical = [(27, 33), (27, 26), (15, 14), (15, 9)]
else:
    # No regions:
    CriticalRegionNodes = []
    GateToNonCritical = []
    GateToCritical = []
    # For those who don't need broken links
    ListOfBrokenLinks = []
    VirtualBrokenLinksForNonCritical = []
    VirtualBrokenLinksForCritical = []