__author__ = 'siavoosh'
import networkx
import random
def GenerateTG(Task_List,TG_Edge_List,Task_Criticality_List,Task_WCET_List,TG_Edge_Weight):
    print("PREPARING TASK GRAPH (TG)...")
    TG=networkx.DiGraph()
    Edge_Criticality_List=[]
    # IF both sender and receiver are critical then that transaction is critical
    print "\tCALCULATING THE CRITICALITY OF LINKS..."
    for edge in TG_Edge_List:
        if Task_Criticality_List[Task_List.index(edge[0])]=='H' and Task_Criticality_List[Task_List.index(edge[1])]=='H' :
            Edge_Criticality_List.append('H')
        else:
            Edge_Criticality_List.append('L')
    print "\tLINKS CRITICALITY CALCULATED!"
    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i],WCET=Task_WCET_List[i],Criticality=Task_Criticality_List[i],Cluster=None,Node=None,Priority=None)

    for i in range(0,len(TG_Edge_List)):
        TG.add_edge(TG_Edge_List[i][0],TG_Edge_List[i][1],Criticality=Edge_Criticality_List[i],Link=[],ComWeight=TG_Edge_Weight[i])  # Communication weight
    AssignPriorities(TG)
    print("TASK GRAPH (TG) IS READY...")
    return TG

def GenerateRandomTG(NumberOfTasks,NumberOfEdges,WCET_Range,EdgeWeightRange):
    TG=networkx.DiGraph()
    print("PREPARING RANDOM TASK GRAPH (TG)...")

    Task_List=[]
    Task_Criticality_List=[]
    Task_WCET_List=[]
    TG_Edge_List=[]
    Edge_Criticality_List=[]
    TG_Edge_Weight=[]

    for i in range(0,NumberOfTasks):
        Task_List.append(i)
        Task_Criticality_List.append(random.choice(['H','L']))
        Task_WCET_List.append(random.randrange(1,WCET_Range))

    for j in range(0,NumberOfEdges):
        SourceTask = random.choice(Task_List)
        DestTask = random.choice(Task_List)
        while SourceTask==DestTask:
            DestTask = random.choice(Task_List)

        if (SourceTask,DestTask) not in TG_Edge_List:
            TG_Edge_List.append((SourceTask,DestTask))
            TG_Edge_Weight.append(random.randrange(1,EdgeWeightRange))

    print "\tCALCULATING THE CRITICALITY OF LINKS..."
    for edge in TG_Edge_List:
        if Task_Criticality_List[Task_List.index(edge[0])]=='H' and Task_Criticality_List[Task_List.index(edge[1])]=='H' :
            Edge_Criticality_List.append('H')
        else:
            Edge_Criticality_List.append('L')
    print "\tLINKS CRITICALITY CALCULATED!"
    #Todo: writing randomly generated TG
    for i in range(0,len(Task_List)):
        TG.add_node(Task_List[i],WCET=Task_WCET_List[i],Criticality=Task_Criticality_List[i],Cluster=None,Node=None,Priority=None)

    for i in range(0,len(TG_Edge_List)):
        # making sure that the graph is still acyclic
        if not networkx.has_path(TG,TG_Edge_List[i][1],TG_Edge_List[i][0]):
            TG.add_edge(TG_Edge_List[i][0],TG_Edge_List[i][1],Criticality=Edge_Criticality_List[i],Link=[],ComWeight=TG_Edge_Weight[i])  # Communication weight
    AssignPriorities(TG)
    print("TASK GRAPH (TG) IS READY...")
    return TG


def FindSourceNodes(TG):
    SourceNode=[]
    for Task in TG.nodes():
        if len(TG.predecessors(Task))==0:
            SourceNode.append(Task)
    return SourceNode


def AssignPriorities(TG):
    print("ASSIGNING PRIORITIES TO TASK GRAPH (TG)...")
    SourceNodes=FindSourceNodes(TG)
    for Task in SourceNodes:
        TG.node[Task]['Priority']=0

    for Task in TG.nodes():
        distance=[]
        if Task not in SourceNodes:
            for Source in SourceNodes:
                if networkx.has_path(TG,Source,Task):
                    ShortestPaths=networkx.shortest_path(TG,Source,Task)
                    distance.append(len(ShortestPaths)-1)
            TG.node[Task]['Priority']=min(distance)