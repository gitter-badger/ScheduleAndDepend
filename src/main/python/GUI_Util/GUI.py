# Copyright (C) Siavoosh Payandeh Azad


import Tkinter
import ttk
import tkFileDialog
import tkMessageBox
from ConfigAndPackages import Config
from ConfigAndPackages import PackageFile

from PIL import ImageTk, Image


class ConfigApp(Tkinter.Tk):

    apply_button = False

    # Task clustering Config
    cl_opt_start_row = 2
    cl_opt_start_col = 3

    # Mapping Algorithm Config
    Mapping_OptStartRow = 6
    Mapping_OptStartCol = 3

    # Architecture Graph Config
    Topology_StartingRow = 2
    Topology_StartingCol = 0

    # Task Graph Config
    TG_StartingRow = 7
    TG_StartingCol = 0

    # Routing Config
    Routing_StartingRow = 15
    Routing_StartingCol = 0

    # Fault Handling
    Fault_StartingRow = 2
    Fault_StartingCol = 6

    # visualization
    Viz_StartingRow = 7
    Viz_StartingCol = 6

    # Animation Frame generation
    Anim_StartingRow = 12
    Anim_StartingCol = 6

    # vertical Link placement optimization
    VLPlacement_StartingRow = 2
    VLPlacement_StartingCol = 9

    # Dependability Config
    dependability_starting_row = 8
    dependability_starting_col = 9

    # PMC Config
    PMC_StartingRow = 12
    PMC_StartingCol = 9

    OptionMenuWidth = 15
    EntryWidth = 10

    RoutingDict = {'2D': ['XY', 'West First', 'North Last', 'Negative First', 'From File'],
                   '3D': ['XYZ', 'Negative First', 'From File']}

    MappingDict = {'Manual': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap', 'MinMin',
                              'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime'],
                   'RandomDependent': ['LocalSearch', 'IterativeLocalSearch', 'SimulatedAnnealing', 'NMap'],
                   'RandomIndependent': ['MinMin', 'MaxMin', 'MinExecutionTime', 'MinimumCompletionTime']}

    VLP_Alg_List = ['LocalSearch', 'IterativeLocalSearch']

    FlowControlList = ['Wormhole', 'StoreAndForward']

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent

        img = ImageTk.PhotoImage(Image.open("GUI_Util/Jelly.png"))

        # This work, "Jelly.png", is a derivative of "Sea Ghost" by Joey Gannon,
        # used under CC BY-SA.  The original version can be found here:
        # https://www.flickr.com/photos/brunkfordbraun/679827214
        # This work is under same license as the original
        
        self.label1 = Tkinter.Label(self, text="", image=img)
        self.label1.image = img
        # ---------------------------------------------
        #                   Topology
        # ---------------------------------------------
        self.TopologyLabel = Tkinter.Label(self, text="Topology:")
        available_topologies = ['2DTorus', '2DMesh', '2DLine', '2DRing', '3DMesh']
        self.Topology = Tkinter.StringVar()
        self.TopologyOption = Tkinter.OptionMenu(self, self.Topology, *available_topologies,
                                                 command=self.network_size_cont)
        self.TopologyOption.config(width=self.OptionMenuWidth)

        self.network_size_x = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.network_size_y = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.network_size_z = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)

        # ---------------------------------------------
        #                   TG
        # ---------------------------------------------
        self.TG_Label = Tkinter.Label(self, text="Task Graph Type:")
        self.AvailableTGs = ['RandomDependent', 'RandomIndependent', 'Manual', 'FromDOTFile']
        self.TGType = Tkinter.StringVar(self)
        self.TGType.set('RandomDependent')
        self.TGTypeOption = Tkinter.OptionMenu(self, self.TGType, *self.AvailableTGs, command=self._tg_type_cont)
        self.TGTypeOption.config(width=self.OptionMenuWidth)

        self.NumOfTasks_Label = Tkinter.Label(self, text="Number of Tasks:")
        self.NumOfTasks = Tkinter.Entry(self, width=self.EntryWidth)

        self.NumOfCritTasks_Label = Tkinter.Label(self, text="Number of Critical Tasks:")
        self.NumOfCritTasks = Tkinter.Entry(self, width=self.EntryWidth)

        self.NumOfEdge_Label = Tkinter.Label(self, text="Number TG Edges:")
        self.NumOfEdge = Tkinter.Entry(self, width=self.EntryWidth)

        self.WCET_Range_Label = Tkinter.Label(self, text="WCET Range:")
        self.WCET_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.EdgeWeight_Range_Label = Tkinter.Label(self, text="Edge Weight Range:")
        self.EdgeWeight_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.Release_Range_Label = Tkinter.Label(self, text="Task Release Range:")
        self.Release_Range = Tkinter.Entry(self, width=self.EntryWidth)

        self.TGBrowse = Tkinter.Entry(self, bg='gray')
        self.TGBrowse.insert(0, "TG File Path...")

        self.TGBrowseButton = Tkinter.Button(self, text="Browse", command=self._get_tg_file)

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        self.RoutingLabel = Tkinter.Label(self, text="Routing Algorithm:")
        available_routings = self.RoutingDict['2D']
        self.RoutingAlg = Tkinter.StringVar()
        self.RoutingAlg.set(self.RoutingDict['2D'][0])
        self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *available_routings,
                                                   command=self._routing_func)
        self.RoutingAlgOption.config(width=self.OptionMenuWidth)

        self.RoutingTypeLabel = Tkinter.Label(self, text="Routing type:")
        available_routings_types = ['MinimalPath', 'NonMinimalPath']
        self.RoutingType = Tkinter.StringVar()
        self.RoutingType.set('MinimalPath')
        self.RoutingTypeOption = Tkinter.OptionMenu(self, self.RoutingType, *available_routings_types)
        self.RoutingTypeOption.config(width=self.OptionMenuWidth)

        self.RoutingBrowse = Tkinter.Entry(self, bg='gray')
        self.RoutingBrowse.insert(0, "Routing File Path...")

        self.RoutingBrowseButton = Tkinter.Button(self, text="Browse", command=self._get_routing_file)

        self.flow_control_label = Tkinter.Label(self, text="Flow Control:")
        available_flow_controls = self.FlowControlList
        self.FlowControl = Tkinter.StringVar()
        self.FlowControl.set(self.FlowControlList[0])
        self.FlowControlOption = Tkinter.OptionMenu(self, self.FlowControl, *available_flow_controls,
                                                    command=self._routing_func)
        # ---------------------------------------------
        #                   Clustering
        # ---------------------------------------------
        self.ClusteringOptVar = Tkinter.BooleanVar(self)
        self.ClusteringOptEnable = Tkinter.Checkbutton(self, text="Clustering Optimization",
                                                       variable=self.ClusteringOptVar, command=self._clustering_cont)
        self.ClusteringIterLabel = Tkinter.Label(self, text="Clustering Iterations:")
        self.ClusteringIterations = Tkinter.Entry(self, width=self.EntryWidth)

        self.ClusteringCostLabel = Tkinter.Label(self, text="Cost Function Type:")
        available_costs = ['SD', 'SD+MAX', 'MAX', 'SUMCOM', 'AVGUTIL', 'MAXCOM']
        self.ClusterCost = Tkinter.StringVar(self)
        self.ClusterCost.set('SD+MAX')
        self.ClusterCostOpt = Tkinter.OptionMenu(self, self.ClusterCost, *available_costs)
        self.ClusterCostOpt.config(width=self.OptionMenuWidth)
        # ---------------------------------------------
        #                   Mapping
        # ---------------------------------------------
        self.Mapping_Label = Tkinter.Label(self, text="Mapping Algorithm:")
        self.Mapping = Tkinter.StringVar(self)
        self.Mapping.set('LocalSearch')
        self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomDependent'],
                                                command=self._mapping_alg_cont)
        self.MappingOption.config(width=self.OptionMenuWidth)

        self.MappingCostLabel = Tkinter.Label(self, text="Cost Function Type:")
        available_mapping_costs = ['SD', 'SD+MAX', 'MAX', 'CONSTANT']
        self.MappingCost = Tkinter.StringVar(self)
        self.MappingCost.set('SD+MAX')
        self.MappingCostOpt = Tkinter.OptionMenu(self, self.MappingCost, *available_mapping_costs)
        self.MappingCostOpt.config(width=self.OptionMenuWidth)
        # ---------------------------------------------
        #           Local Search
        # ---------------------------------------------
        self.LS_Iter_Label = Tkinter.Label(self, text="LS Iterations:")
        self.LS_Iter = Tkinter.Entry(self, width=self.EntryWidth)
        self.LS_Iter.insert(0, '100')

        self.ILS_Iter_Label = Tkinter.Label(self, text="ILS Iterations:")
        self.ILS_Iter = Tkinter.Entry(self, width=self.EntryWidth)
        self.ILS_Iter.insert(0, '10')

        # ---------------------------------------------
        #           Simulated Annealing
        # ---------------------------------------------

        self.SA_Label = Tkinter.Label(self, text="Annealing Schedule:")
        available_annealing = ['Linear', 'Exponential', 'Adaptive', 'Markov', 'Logarithmic', 'Aart', 'Huang']
        self.Annealing = Tkinter.StringVar()
        self.Annealing.set('Linear')
        self.AnnealingOption = Tkinter.OptionMenu(self, self.Annealing,
                                                  *available_annealing, command=self._annealing_termination)
        self.AnnealingOption.config(width=self.OptionMenuWidth)

        self.SA_Term_Label = Tkinter.Label(self, text="Termination Criteria:")
        available_termination = ['StopTemp', 'IterationNum']
        self.Termination = Tkinter.StringVar()
        self.Termination.set('StopTemp')
        self.TerminationOption = Tkinter.OptionMenu(self, self.Termination,
                                                    *available_termination, command=self._annealing_termination)
        self.TerminationOption.config(width=self.OptionMenuWidth)

        self.SA_IterLabel = Tkinter.Label(self, text="Number of Iterations:")
        self.SA_Iterations = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Iterations.insert(0, '100000')

        self.SA_InitTemp_Label = Tkinter.Label(self, text="Initial Temperature:")
        self.SA_InitTemp = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_InitTemp.insert(0, '100')

        self.SA_StopTemp_Label = Tkinter.Label(self, text="Stop Temperature:")
        self.SA_StopTemp = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_StopTemp.insert(0, '5')

        self.SA_Alpha_Label = Tkinter.Label(self, text="Cooling ratio:")
        self.SA_Alpha = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Alpha.insert(0, '0.999')

        self.SA_LoG_Const_Label = Tkinter.Label(self, text="Log cooling constant:")
        self.SA_LoG_Const = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_LoG_Const.insert(0, '1000')

        self.CostMonitor_Label = Tkinter.Label(self, text="Cost Monitor Queue Size:")
        self.CostMonitor = Tkinter.Entry(self, width=self.EntryWidth)
        self.CostMonitor.insert(0, '2000')

        self.CostMonitorSlope_Label = Tkinter.Label(self, text="Slope Range For Cooling:")
        self.CostMonitorSlope = Tkinter.Entry(self, width=self.EntryWidth)
        self.CostMonitorSlope.insert(0, '0.02')

        self.MaxSteadyState_Label = Tkinter.Label(self, text="Max steps/no improvement:")
        self.MaxSteadyState = Tkinter.Entry(self, width=self.EntryWidth)
        self.MaxSteadyState.insert(0, '30000')

        self.MarkovNum_Label = Tkinter.Label(self, text="Length of Markov Chain:")
        self.MarkovNum = Tkinter.Entry(self, width=self.EntryWidth)
        self.MarkovNum.insert(0, '2000')

        self.MarkovTempStep_Label = Tkinter.Label(self, text="Temperature step:")
        self.MarkovTempStep = Tkinter.Entry(self, width=self.EntryWidth)
        self.MarkovTempStep.insert(0, '1')

        self.SA_Delta_Label = Tkinter.Label(self, text="Delta:")
        self.SA_Delta = Tkinter.Entry(self, width=self.EntryWidth)
        self.SA_Delta.insert(0, '0.05')

        # ---------------------------------------------
        #               Fault Injection
        # ---------------------------------------------
        self.FaultInjection = Tkinter.BooleanVar(self)
        self.FaultInjectionEnable = Tkinter.Checkbutton(self, text="Event Driven Fault Injection",
                                                        variable=self.FaultInjection,
                                                        command=self._fault_injection)

        self.MTBF_Label = Tkinter.Label(self, text="MTBF (sec):")
        self.MTBF = Tkinter.Entry(self, width=self.EntryWidth)
        self.MTBF.insert(0, '2')

        self.SDMTBF_Label = Tkinter.Label(self, text="TBF's Standard Deviation:")
        self.SDMTBF = Tkinter.Entry(self, width=self.EntryWidth)
        self.SDMTBF.insert(0, '0.1')

        self.RunTime_Label = Tkinter.Label(self, text="Program RunTime:")
        self.RunTime = Tkinter.Entry(self, width=self.EntryWidth)
        self.RunTime.insert(0, '10')

        # ---------------------------------------------
        #               Viz
        # ---------------------------------------------
        self.AllViz = Tkinter.BooleanVar(self)
        self.AllViz.set('False')
        self.AllVizEnable = Tkinter.Checkbutton(self, text="Check/Un-check all reports",
                                                variable=self.AllViz, command=self._all_viz_func,
                                                wraplength=100)

        self.RG_Draw = Tkinter.BooleanVar(self)
        self.RG_Draw.set('False')
        self.RG_DrawEnable = Tkinter.Checkbutton(self, text="Routing Graph", variable=self.RG_Draw)

        self.SHM_Draw = Tkinter.BooleanVar(self)
        self.SHM_Draw.set('False')
        self.SHM_DrawEnable = Tkinter.Checkbutton(self, text="System Health Map", variable=self.SHM_Draw)

        self.Mapping_Draw = Tkinter.BooleanVar(self)
        self.Mapping_Draw.set('False')
        self.Mapping_DrawEnable = Tkinter.Checkbutton(self, text="Mapping Report", variable=self.Mapping_Draw)

        self.PMCG_Draw = Tkinter.BooleanVar(self)
        self.PMCG_Draw.set('False')
        self.PMCG_DrawEnable = Tkinter.Checkbutton(self, text="PMCG Report", variable=self.PMCG_Draw)

        self.TTG_Draw = Tkinter.BooleanVar(self)
        self.TTG_Draw.set('False')
        self.TTG_DrawEnable = Tkinter.Checkbutton(self, text="TTG Report", variable=self.TTG_Draw)

        # ---------------------------------------------
        #               Anim
        # ---------------------------------------------
        self.AnimEnable = Tkinter.BooleanVar(self)
        self.AnimEnable.set('False')
        self.AnimEnableBox = Tkinter.Checkbutton(self, text="Generate Animation Frames",
                                                 variable=self.AnimEnable, command=self._animation_config)

        self.FrameRezLabel = Tkinter.Label(self, text="Frame Resolution(dpi):")
        self.FrameRez = Tkinter.Entry(self, width=self.EntryWidth)
        self.FrameRez.insert(0, '20')

        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        self.VLPlacementEnable = Tkinter.BooleanVar(self)
        self.VLPlacementEnable.set('False')
        self.VLPlacementEnableBox = Tkinter.Checkbutton(self, text="Enable VL Placement Optimization",
                                                        variable=self.VLPlacementEnable,
                                                        command=self._vl_placement_func,
                                                        wraplength=200)

        self.VLP_Alg_Label = Tkinter.Label(self, text="Opt algorithm:")
        self.VLP_Alg = Tkinter.StringVar()
        self.VLP_Alg.set('LocalSearch')
        self.VLP_AlgOption = Tkinter.OptionMenu(self, self.VLP_Alg, *self.VLP_Alg_List, command=self._vlp_alg_func)
        self.VLP_AlgOption.config(width=self.OptionMenuWidth)

        self.NumOfVLs_Label = Tkinter.Label(self, text="Number of VLs:")
        self.NumOfVLs = Tkinter.Entry(self, width=self.EntryWidth)

        self.VLP_IterationsLS_Label = Tkinter.Label(self, text="LS Iterations:")
        self.VLP_IterationsLS = Tkinter.Entry(self, width=self.EntryWidth)

        self.VLP_IterationsILS_Label = Tkinter.Label(self, text="ILS Iterations:")
        self.VLP_IterationsILS = Tkinter.Entry(self, width=self.EntryWidth)
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        self.SlackNumber_Label = Tkinter.Label(self, text="Task Slack Count:")
        self.SlackNumber = Tkinter.Spinbox(self, from_=0, to=10, width=self.EntryWidth)

        self.ComSlackNumber_Label = Tkinter.Label(self, text="Com. Slack Count:")
        self.ComSlackNumber = Tkinter.Spinbox(self, from_=0, to=10, width=self.EntryWidth)

        self.NumberOfRects_Label = Tkinter.Label(self, text="NoCDepend Rectangle #:")
        self.NumberOfRects = Tkinter.Spinbox(self, from_=1, to=10, width=self.EntryWidth)
        self.NumberOfRects.delete(0, 'end')
        self.NumberOfRects.insert(0, 3)

        self.ErrorMessage = Tkinter.Label(self, text="", font="-weight bold", fg="red")

        # ----------------------------------------
        #           PMC config
        # ----------------------------------------
        self.PMCEnable = Tkinter.BooleanVar(self)
        self.PMCEnable.set('False')
        self.PMCEnableEnableBox = Tkinter.Checkbutton(self, text="Enable PMC config",
                                                      variable=self.PMCEnable, command=self._pmc_func)

        self.PMCType_Label = Tkinter.Label(self, text="PMC Model:")
        self.AvailablePMCTypes = ['Sequentially diagnosable', 'One Step Diagnosable']
        self.PMCType = Tkinter.StringVar(self)
        self.PMCType.set('Sequentially diagnosable')
        self.PMCTypeOption = Tkinter.OptionMenu(self, self.PMCType, *self.AvailablePMCTypes,
                                                command=self._t_fault_control)
        self.PMCTypeOption.config(width=self.OptionMenuWidth)

        self.TfaultDiagnosable_Label = Tkinter.Label(self, text="T-Fault Diagnosable:")
        self.TfaultDiagnosable = Tkinter.Entry(self, width=self.EntryWidth)

        self.ErrorMessage = Tkinter.Label(self, text="", font="-weight bold", fg="red")

        self._initialize()

    def _initialize(self):

        self.grid()

        self.label1.grid(row=0, column=1, sticky='eW')
        self.label1.bind("<Enter>", self._on_enter)

        logo = Tkinter.Label(self, text="SCHEDULE AND DEPEND CONFIG GUI", font="-weight bold")
        logo.grid(column=1, row=0, columnspan=7)
        ttk.Separator(self, orient='horizontal').grid(column=0, row=1, columnspan=11, sticky="ew")

        # ----------------------------------------
        Tkinter.Label(self, text="Topology Config", font="-weight bold").grid(column=self.Topology_StartingCol,
                                                                              row=self.Topology_StartingRow,
                                                                              columnspan=2)
        self.Topology.set('2DMesh')
        self.TopologyLabel.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+1)
        self.TopologyOption.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+1, sticky='w')

        x_size_label = Tkinter.Label(self, text="X Size:")
        y_size_label = Tkinter.Label(self, text="Y Size:")
        z_size_label = Tkinter.Label(self, text="Z Size:")

        self.network_size_x.delete(0, 'end')
        self.network_size_x.insert(0, 3)
        self.network_size_y.delete(0, 'end')
        self.network_size_y.insert(0, 3)
        self.network_size_z.delete(0, 'end')
        self.network_size_z.insert(0, 1)

        x_size_label.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+2)
        self.network_size_x.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+2, sticky='w')
        y_size_label.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+3)
        self.network_size_y.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+3, sticky='w')
        z_size_label.grid(column=self.Topology_StartingCol, row=self.Topology_StartingRow+4)
        self.network_size_z.grid(column=self.Topology_StartingCol+1, row=self.Topology_StartingRow+4, sticky='w')
        self.network_size_z.config(state='disabled')

        ttk.Separator(self, orient='vertical').grid(column=self.Topology_StartingCol+2,
                                                    row=self.Topology_StartingRow+1, rowspan=16, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Topology_StartingCol,
                                                      row=self.Topology_StartingRow+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   TG
        # ----------------------------------------
        Tkinter.Label(self, text="Task Graph Settings", font="-weight bold").grid(column=self.TG_StartingCol,
                                                                                  row=self.TG_StartingRow,
                                                                                  columnspan=2)
        self.TG_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+1, sticky='w')
        self.TGTypeOption.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+1, sticky='w')

        self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2, sticky='w')
        self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2, sticky='w')
        self.NumOfTasks.insert(0, '35')

        self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3, sticky='w')
        self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3, sticky='w')
        self.NumOfCritTasks.insert(0, '0')

        self.NumOfEdge_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4, sticky='w')
        self.NumOfEdge.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4, sticky='w')
        self.NumOfEdge.insert(0, '20')

        self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5, sticky='w')
        self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5, sticky='w')
        self.WCET_Range.insert(0, '15')

        self.EdgeWeight_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+6, sticky='w')
        self.EdgeWeight_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+6, sticky='w')
        self.EdgeWeight_Range.insert(0, '7')

        self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+7, sticky='w')
        self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+7, sticky='w')
        self.Release_Range.insert(0, '5')

        ttk.Separator(self, orient='horizontal').grid(column=self.TG_StartingCol,
                                                      row=self.TG_StartingRow+8, columnspan=2, sticky="ew")

        # ---------------------------------------------
        #                   Routing
        # ---------------------------------------------
        Tkinter.Label(self, text="Routing Settings", font="-weight bold").grid(column=self.Routing_StartingCol,
                                                                               row=self.Routing_StartingRow,
                                                                               columnspan=2)
        self.RoutingLabel.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+1)
        self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)

        self.RoutingTypeLabel.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+2)
        self.RoutingTypeOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+2)
        self.RoutingTypeOption.config(state='disable')

        self.flow_control_label.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+4)
        self.FlowControlOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+4)
        self.FlowControlOption.config(state='normal')
        ttk.Separator(self, orient='horizontal').grid(column=self.Routing_StartingCol,
                                                      row=self.Routing_StartingRow+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   CTG
        # ----------------------------------------
        Tkinter.Label(self, text="Clustering Settings", font="-weight bold").grid(column=self.cl_opt_start_col,
                                                                                  row=self.cl_opt_start_row,
                                                                                  columnspan=2)
        self.ClusteringOptVar.set('False')
        self.ClusteringIterations.insert(0, '1000')
        self.ClusteringOptEnable.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+4,
                                                      columnspan=2, sticky="ew")

        # ----------------------------------------
        #                   Mapping
        # ----------------------------------------
        Tkinter.Label(self, text="Mapping Settings", font="-weight bold").grid(column=self.Mapping_OptStartCol,
                                                                               row=self.Mapping_OptStartRow,
                                                                               columnspan=2)
        self.Mapping_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+1)
        self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)

        self.MappingCostLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+2)
        self.MappingCostOpt.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+2)

        self.LS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
        self.LS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)

        ttk.Separator(self, orient='vertical').grid(column=self.cl_opt_start_col+2,
                                                    row=self.cl_opt_start_row+1, rowspan=14, sticky="ns")
        ttk.Separator(self, orient='horizontal').grid(column=self.Mapping_OptStartCol,
                                                      row=self.Mapping_OptStartRow+11, columnspan=2, sticky="ew")
        # ----------------------------------------
        #               Fault
        # ----------------------------------------
        Tkinter.Label(self, text="Fault Settings", font="-weight bold").grid(column=self.Fault_StartingCol,
                                                                             row=self.Fault_StartingRow,
                                                                             columnspan=2)
        self.FaultInjection.set('False')
        self.FaultInjectionEnable.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+1)

        ttk.Separator(self, orient='horizontal').grid(column=self.Fault_StartingCol,
                                                      row=self.Fault_StartingRow+5, columnspan=2, sticky="ew")

        ttk.Separator(self, orient='vertical').grid(column=self.Fault_StartingCol+2,
                                                    row=self.Fault_StartingRow+1, rowspan=12, sticky="ns")
        # ----------------------------------------
        #                   Viz
        # ----------------------------------------
        Tkinter.Label(self, text="Visualization Config", font="-weight bold").grid(column=self.Viz_StartingCol,
                                                                                   row=self.Viz_StartingRow,
                                                                                   columnspan=2)

        self.AllVizEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+1, columnspan=1, sticky='w')

        self.SHM_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+2, sticky='W')
        self.RG_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+3, sticky='W')
        self.Mapping_DrawEnable.grid(column=self.Viz_StartingCol, row=self.Viz_StartingRow+4, sticky='W')
        self.PMCG_DrawEnable.grid(column=self.Viz_StartingCol+1, row=self.Viz_StartingRow+3, sticky='W')
        self.TTG_DrawEnable.grid(column=self.Viz_StartingCol+1, row=self.Viz_StartingRow+4, sticky='W')

        ttk.Separator(self, orient='horizontal').grid(column=self.Viz_StartingCol,
                                                      row=self.Viz_StartingRow+5, columnspan=2, sticky="ew")
        # ----------------------------------------
        #               Animation
        # ----------------------------------------
        Tkinter.Label(self, text="Animation Frames Config", font="-weight bold").grid(column=self.Anim_StartingCol,
                                                                                      row=self.Anim_StartingRow,
                                                                                      columnspan=2)

        self.AnimEnableBox.grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+1,
                                sticky='W')
        ttk.Separator(self, orient='horizontal').grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+3,
                                                      columnspan=2, sticky="ew")
        # ----------------------------------------
        #           Vertical Link Placement
        # ----------------------------------------
        Tkinter.Label(self, text="Vertical Link Placement Optimization", font="-weight bold").grid(column=self.VLPlacement_StartingCol,
                      row=self.VLPlacement_StartingRow, columnspan=2)

        self.VLPlacementEnableBox.grid(column=self.VLPlacement_StartingCol, row=self.VLPlacement_StartingRow+1)
        self.VLPlacementEnableBox.config(state='disable')

        ttk.Separator(self, orient='horizontal').grid(column=self.VLPlacement_StartingCol,
                                                      row=self.VLPlacement_StartingRow+6, columnspan=2, sticky="ew")
        # ----------------------------------------
        #           Dependability section
        # ----------------------------------------
        Tkinter.Label(self, text="Dependability Config", font="-weight bold").grid(column=self.dependability_starting_col,
                                                                                   row=self.dependability_starting_row,
                                                                                   columnspan=2)
        self.SlackNumber_Label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+1)
        self.SlackNumber.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+1)

        self.ComSlackNumber_Label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+2)
        self.ComSlackNumber.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+2)

        self.NumberOfRects_Label.grid(column=self.dependability_starting_col, row=self.dependability_starting_row+3)
        self.NumberOfRects.grid(column=self.dependability_starting_col+1, row=self.dependability_starting_row+3)

        ttk.Separator(self, orient='horizontal').grid(column=self.dependability_starting_col,
                                                      row=self.dependability_starting_row+4, columnspan=2, sticky="ew")
        # ----------------------------------------
        #           PMC Graph
        # ----------------------------------------
        Tkinter.Label(self, text="PMC Config", font="-weight bold").grid(column=self.PMC_StartingCol,
                                                                         row=self.PMC_StartingRow, columnspan=2)

        self.PMCEnableEnableBox.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+1, sticky='w')

        ttk.Separator(self, orient='horizontal').grid(column=self.PMC_StartingCol,
                                                      row=self.PMC_StartingRow+4, columnspan=2, sticky="ew")
        # ----------------------------------------
        #                   Buttons
        # ----------------------------------------
        self.ErrorMessage.grid(column=4, row=19, columnspan=5)

        quitButton = Tkinter.Button(self, text="Apply", command=self._apply_button, width=15)
        quitButton.grid(column=4, row=20, columnspan=2, rowspan=2)

        quitButton = Tkinter.Button(self, text="cancel", command=self._cancel_button)
        quitButton.grid(column=6, row=20, columnspan=2, rowspan=2)

    def network_size_cont(self, Topology):
        if '3D' in Topology:
            self.network_size_z.config(state='normal')
            self.VLPlacementEnableBox.config(state='normal')
            self.RoutingAlgOption.grid_forget()
            del self.RoutingAlgOption
            self.RoutingAlg.set('Please Select...')
            self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *self.RoutingDict['3D'],
                                                       command=self._routing_func)
            self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)
            self.RoutingAlgOption.config(width=self.OptionMenuWidth)

            self.RoutingType.set("Please Select...")
            self.RoutingTypeOption.config(state='disable')
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

            self.network_size_z.delete(0, 'end')
            self.network_size_z.insert(0, 2)
        else:
            self.VLPlacementEnableBox.deselect()
            self.VLPlacementEnableBox.config(state='disable')
            self.VLP_Alg_Label.grid_forget()
            self.VLP_AlgOption.grid_forget()
            self.NumOfVLs_Label.grid_forget()
            self.NumOfVLs.grid_forget()
            self.VLP_IterationsLS_Label.grid_forget()
            self.VLP_IterationsLS.grid_forget()
            self.VLP_IterationsILS_Label.grid_forget()
            self.VLP_IterationsILS.grid_forget()

            self.RoutingAlgOption.grid_forget()
            del self.RoutingAlgOption
            self.RoutingAlg.set('Please Select...')
            self.RoutingAlgOption = Tkinter.OptionMenu(self, self.RoutingAlg, *self.RoutingDict['2D'],
                                                       command=self._routing_func)
            self.RoutingAlgOption.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+1)
            self.RoutingAlgOption.config(width=self.OptionMenuWidth)

            self.RoutingType.set("Please Select...")
            self.RoutingTypeOption.config(state='disable')
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

            self.network_size_z.delete(0, 'end')
            self.network_size_z.insert(0, 1)
            self.network_size_z.config(state='disabled')

    def _tg_type_cont(self, TGType):
        if TGType == 'RandomDependent':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomDependent'],
                                                    command=self._mapping_alg_cont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self._clear_mapping()

            self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.NumOfEdge_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4)
            self.NumOfEdge.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4)
            self.NumOfEdge.delete(0, 'end')
            self.NumOfEdge.insert(0, '20')

            self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5)
            self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5)
            self.WCET_Range.delete(0, 'end')
            self.WCET_Range.insert(0, '15')

            self.EdgeWeight_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+6)
            self.EdgeWeight_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+6)
            self.EdgeWeight_Range.delete(0, 'end')
            self.EdgeWeight_Range.insert(0, '7')

            self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+7)
            self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+7)
            self.Release_Range.delete(0, 'end')
            self.Release_Range.insert(0, '5')

            self.TGBrowse.grid_forget()
            self.TGBrowseButton.grid_forget()

        elif TGType == 'RandomIndependent':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['RandomIndependent'],
                                                    command=self._mapping_alg_cont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self._clear_mapping()

            self.NumOfTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2)
            self.NumOfTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)
            self.NumOfTasks.delete(0, 'end')
            self.NumOfTasks.insert(0, '35')

            self.NumOfCritTasks_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+3)
            self.NumOfCritTasks.delete(0, 'end')
            self.NumOfCritTasks.insert(0, '0')

            self.WCET_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+4)
            self.WCET_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+4)
            self.WCET_Range.delete(0, 'end')
            self.WCET_Range.insert(0, '15')

            self.Release_Range_Label.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+5)
            self.Release_Range.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+5)
            self.Release_Range.delete(0, 'end')
            self.Release_Range.insert(0, '5')

            self.NumOfEdge_Label.grid_forget()
            self.NumOfEdge.grid_forget()

            self.EdgeWeight_Range.grid_forget()
            self.EdgeWeight_Range_Label.grid_forget()

            self.TGBrowse.grid_forget()
            self.TGBrowseButton.grid_forget()

        elif TGType == 'Manual':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['Manual'],
                                                    command=self._mapping_alg_cont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self._clear_mapping()

            self.TGBrowse.grid_forget()
            self.TGBrowseButton.grid_forget()

            self.NumOfTasks_Label.grid_forget()
            self.NumOfTasks.grid_forget()

            self.NumOfCritTasks_Label.grid_forget()
            self.NumOfCritTasks.grid_forget()

            self.NumOfEdge_Label.grid_forget()
            self.NumOfEdge.grid_forget()

            self.WCET_Range_Label.grid_forget()
            self.WCET_Range.grid_forget()

            self.Release_Range_Label.grid_forget()
            self.Release_Range.grid_forget()

            self.EdgeWeight_Range.grid_forget()
            self.EdgeWeight_Range_Label.grid_forget()

        elif TGType == 'FromDOTFile':
            self.MappingOption.grid_forget()
            del self.MappingOption
            self.Mapping.set('Please Select...')
            self.MappingOption = Tkinter.OptionMenu(self, self.Mapping, *self.MappingDict['Manual'],
                                                    command=self._mapping_alg_cont)
            self.MappingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+1)
            self.MappingOption.config(width=self.OptionMenuWidth)
            self._clear_mapping()

            self.TGBrowse.grid(column=self.TG_StartingCol, row=self.TG_StartingRow+2, sticky='e')
            self.TGBrowseButton.grid(column=self.TG_StartingCol+1, row=self.TG_StartingRow+2)

            self.NumOfTasks_Label.grid_forget()
            self.NumOfTasks.grid_forget()

            self.NumOfCritTasks_Label.grid_forget()
            self.NumOfCritTasks.grid_forget()

            self.NumOfEdge_Label.grid_forget()
            self.NumOfEdge.grid_forget()

            self.WCET_Range_Label.grid_forget()
            self.WCET_Range.grid_forget()

            self.Release_Range_Label.grid_forget()
            self.Release_Range.grid_forget()

            self.EdgeWeight_Range.grid_forget()
            self.EdgeWeight_Range_Label.grid_forget()

    def _all_viz_func(self):
        if self.AllViz.get():
            self.PMCG_Draw.set(True)
            self.Mapping_Draw.set(True)
            self.RG_Draw.set(True)
            self.SHM_Draw.set(True)
            self.TTG_Draw.set(True)
        else:
            self.PMCG_Draw.set(False)
            self.Mapping_Draw.set(False)
            self.RG_Draw.set(False)
            self.SHM_Draw.set(False)
            self.TTG_Draw.set(False)

    def _get_tg_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.TGBrowse.delete(0, 'end')
            self.TGBrowse.insert(1, path)

    def _get_routing_file(self):
        path = tkFileDialog.askopenfilename()
        if path:
            self.RoutingBrowse.delete(0, 'end')
            self.RoutingBrowse.insert(1, path)

    def _vl_placement_func(self):
        if self.VLPlacementEnable.get():
            self.VLP_Alg_Label.grid(column=self.VLPlacement_StartingCol,
                                    row=self.VLPlacement_StartingRow+2, sticky='w')
            self.VLP_AlgOption.grid(column=self.VLPlacement_StartingCol+1,
                                    row=self.VLPlacement_StartingRow+2, sticky='w')
            self.NumOfVLs_Label.grid(column=self.VLPlacement_StartingCol,
                                     row=self.VLPlacement_StartingRow+3, sticky='w')
            self.NumOfVLs.grid(column=self.VLPlacement_StartingCol+1,
                               row=self.VLPlacement_StartingRow+3, sticky='w')
            self.NumOfVLs.delete(0, 'end')
            self.NumOfVLs.insert(0, '5')

            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0, 'end')
            self.VLP_IterationsLS.insert(0, '10')

        else:
            self.VLP_Alg_Label.grid_forget()
            self.VLP_AlgOption.grid_forget()
            self.NumOfVLs_Label.grid_forget()
            self.NumOfVLs.grid_forget()
            self.VLP_IterationsLS_Label.grid_forget()
            self.VLP_IterationsLS.grid_forget()
            self.VLP_IterationsILS_Label.grid_forget()
            self.VLP_IterationsILS.grid_forget()

    def _pmc_func(self):
        if self.PMCEnable.get():
            self.PMCType_Label.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+2, sticky='w')
            self.PMCTypeOption.grid(column=self.PMC_StartingCol+1, row=self.PMC_StartingRow+2, sticky='w')
        else:
            self.PMCType_Label.grid_forget()
            self.PMCTypeOption.grid_forget()

    def _t_fault_control(self, pmc_type):
        if self.PMCType.get() == 'One Step Diagnosable':
            self.TfaultDiagnosable_Label.grid(column=self.PMC_StartingCol, row=self.PMC_StartingRow+3, sticky='w')
            self.TfaultDiagnosable.grid(column=self.PMC_StartingCol+1, row=self.PMC_StartingRow+3, sticky='w')
        else:
            self.TfaultDiagnosable_Label.grid_forget()
            self.TfaultDiagnosable.grid_forget()

    def _vlp_alg_func(self, vlp_alg):
        if self.VLP_Alg.get() == 'LocalSearch':
            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0, 'end')
            self.VLP_IterationsLS.insert(0, '10')

            self.VLP_IterationsILS_Label.grid_forget()
            self.VLP_IterationsILS.grid_forget()

        elif self.VLP_Alg.get() == 'IterativeLocalSearch':
            self.VLP_IterationsLS_Label.grid(column=self.VLPlacement_StartingCol,
                                             row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.grid(column=self.VLPlacement_StartingCol+1,
                                       row=self.VLPlacement_StartingRow+4, sticky='w')
            self.VLP_IterationsLS.delete(0, 'end')
            self.VLP_IterationsLS.insert(0, '10')

            self.VLP_IterationsILS_Label.grid(column=self.VLPlacement_StartingCol,
                                              row=self.VLPlacement_StartingRow+5, sticky='w')
            self.VLP_IterationsILS.grid(column=self.VLPlacement_StartingCol+1,
                                        row=self.VLPlacement_StartingRow+5, sticky='w')
            self.VLP_IterationsILS.delete(0, 'end')
            self.VLP_IterationsILS.insert(0, '10')

    def _routing_func(self, routing):
        if self.RoutingAlg.get() in ['XY', 'XYZ']:
            self.RoutingTypeOption.config(state='disable')
        else:
            self.RoutingTypeOption.config(state='normal')

        if self.RoutingAlg.get() == 'From File':
            self.RoutingBrowse.grid(column=self.Routing_StartingCol, row=self.Routing_StartingRow+3, sticky='e')
            self.RoutingBrowseButton.grid(column=self.Routing_StartingCol+1, row=self.Routing_StartingRow+3)
        else:
            self.RoutingBrowse.grid_forget()
            self.RoutingBrowseButton.grid_forget()

    def _clustering_cont(self):
        if self.ClusteringOptVar.get():
            self.ClusteringIterLabel.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+2)
            self.ClusteringIterations.grid(column=self.cl_opt_start_col+1, row=self.cl_opt_start_row+2)
            self.ClusteringIterations.delete(0, 'end')
            self.ClusteringIterations.insert(0, '1000')

            self.ClusteringCostLabel.grid(column=self.cl_opt_start_col, row=self.cl_opt_start_row+3)
            self.ClusterCostOpt.grid(column=self.cl_opt_start_col+1, row=self.cl_opt_start_row+3)
        else:
            self.ClusteringIterLabel.grid_forget()
            self.ClusteringIterations.grid_forget()
            self.ClusteringCostLabel.grid_forget()
            self.ClusterCostOpt.grid_forget()

    def _clear_mapping(self):
        self._clear_sa_mapping()
        self.LS_Iter_Label.grid_forget()
        self.LS_Iter.grid_forget()
        self.ILS_Iter_Label.grid_forget()
        self.ILS_Iter.grid_forget()
        self.MappingCostLabel.grid_forget()
        self.MappingCostOpt.grid_forget()

    def _mapping_alg_cont(self, mapping):
        if self.Mapping.get() in ['SimulatedAnnealing', 'LocalSearch', 'IterativeLocalSearch']:
            self.MappingCostLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+2)
            self.MappingCostOpt.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+2)
        else:
            self.MappingCostLabel.grid_forget()
            self.MappingCostOpt.grid_forget()

        if self.Mapping.get() == 'SimulatedAnnealing':
            self._clear_sa_mapping()
            self.Annealing.set('Linear')
            self.SA_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
            self.AnnealingOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)

            self.SA_InitTemp.delete(0, 'end')
            self.SA_InitTemp.insert(0, '100')
            self.SA_InitTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
            self.SA_InitTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)

            self.Termination.set('StopTemp')
            self.SA_Term_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+5)
            self.TerminationOption.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+5)

            self.SA_Iterations.delete(0, 'end')
            self.SA_Iterations.insert(0, '100000')
            self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
            self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)
        else:
            self._clear_sa_mapping()

        if self.Mapping.get() in ['LocalSearch', 'IterativeLocalSearch']:
            self.LS_Iter.delete(0, 'end')
            self.LS_Iter.insert(0, '100')
            self.LS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+3)
            self.LS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+3)
        else:
            self.LS_Iter_Label.grid_forget()
            self.LS_Iter.grid_forget()

        if self.Mapping.get() == 'IterativeLocalSearch':
            self.ILS_Iter.delete(0, 'end')
            self.ILS_Iter.insert(0, '10')
            self.ILS_Iter_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+4)
            self.ILS_Iter.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+4)
        else:
            self.ILS_Iter_Label.grid_forget()
            self.ILS_Iter.grid_forget()

    def _annealing_termination(self, annealing):
        if self.Mapping.get() == 'SimulatedAnnealing':
            if self.Annealing.get() == 'Linear' or self.Termination.get() == 'IterationNum':
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_IterLabel.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.SA_Iterations.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)

            elif self.Termination.get() == 'StopTemp' and self.Annealing.get() != 'Linear':
                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

                self.SA_StopTemp.delete(0, 'end')
                self.SA_StopTemp.insert(0, '5')
                self.SA_StopTemp_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+6)
                self.SA_StopTemp.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+6)
            else:
                self.SA_StopTemp.grid_forget()
                self.SA_StopTemp_Label.grid_forget()

                self.SA_Iterations.grid_forget()
                self.SA_IterLabel.grid_forget()

            if self.Annealing.get() in ['Exponential', 'Adaptive', 'Aart', 'Huang']:
                self.SA_Alpha.delete(0, 'end')
                self.SA_Alpha.insert(0, '0.999')
                self.SA_Alpha_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.SA_Alpha.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)
            else:
                self.SA_Alpha_Label.grid_forget()
                self.SA_Alpha.grid_forget()

            if self.Annealing.get() == 'Logarithmic':
                self.SA_LoG_Const.delete(0, 'end')
                self.SA_LoG_Const.insert(0, '1000')
                self.SA_LoG_Const_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.SA_LoG_Const.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)
            else:
                self.SA_LoG_Const_Label.grid_forget()
                self.SA_LoG_Const.grid_forget()

            if self.Annealing.get() == 'Adaptive':

                self.CostMonitorSlope.delete(0, 'end')
                self.CostMonitorSlope.insert(0, '0.02')
                self.CostMonitorSlope_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+9)
                self.CostMonitorSlope.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+9)

                self.MaxSteadyState.delete(0, 'end')
                self.MaxSteadyState.insert(0, '30000')
                self.MaxSteadyState_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+10)
                self.MaxSteadyState.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+10)
            else:
                self.MaxSteadyState_Label.grid_forget()
                self.MaxSteadyState.grid_forget()

                self.CostMonitorSlope_Label.grid_forget()
                self.CostMonitorSlope.grid_forget()

            if self.Annealing.get() == 'Markov':
                self.MarkovNum.delete(0, 'end')
                self.MarkovNum.insert(0, '2000')
                self.MarkovNum_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+7)
                self.MarkovNum.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+7)

                self.MarkovTempStep.delete(0, 'end')
                self.MarkovTempStep.insert(0, '1')
                self.MarkovTempStep_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+8)
                self.MarkovTempStep.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+8)
            else:
                self.MarkovNum_Label.grid_forget()
                self.MarkovNum.grid_forget()

                self.MarkovTempStep_Label.grid_forget()
                self.MarkovTempStep.grid_forget()

            if self.Annealing.get() in ['Aart', 'Adaptive', 'Huang']:
                self.CostMonitor.delete(0, 'end')
                self.CostMonitor.insert(0, '2000')
                self.CostMonitor_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+8)
                self.CostMonitor.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+8)
            else:
                self.CostMonitor_Label.grid_forget()
                self.CostMonitor.grid_forget()

            if self.Annealing.get() in ['Aart', 'Huang']:
                self.SA_Delta.delete(0, 'end')
                self.SA_Delta.insert(0, '0.05')
                self.SA_Delta_Label.grid(column=self.Mapping_OptStartCol, row=self.Mapping_OptStartRow+9)
                self.SA_Delta.grid(column=self.Mapping_OptStartCol+1, row=self.Mapping_OptStartRow+9)
            else:
                self.SA_Delta_Label.grid_forget()
                self.SA_Delta.grid_forget()

    def _clear_sa_mapping(self):
        self.SA_InitTemp.grid_forget()
        self.SA_InitTemp_Label.grid_forget()

        self.SA_StopTemp.grid_forget()
        self.SA_StopTemp_Label.grid_forget()

        self.SA_Iterations.grid_forget()
        self.SA_IterLabel.grid_forget()

        self.TerminationOption.grid_forget()
        self.SA_Term_Label.grid_forget()

        self.SA_Label.grid_forget()
        self.AnnealingOption.grid_forget()

        self.SA_Alpha_Label.grid_forget()
        self.SA_Alpha.grid_forget()

        self.SA_LoG_Const_Label.grid_forget()
        self.SA_LoG_Const.grid_forget()

        self.SA_Delta_Label.grid_forget()
        self.SA_Delta.grid_forget()

        self.MaxSteadyState_Label.grid_forget()
        self.MaxSteadyState.grid_forget()

        self.CostMonitorSlope_Label.grid_forget()
        self.CostMonitorSlope.grid_forget()

        self.CostMonitor_Label.grid_forget()
        self.CostMonitor.grid_forget()

        self.MarkovNum_Label.grid_forget()
        self.MarkovNum.grid_forget()

        self.MarkovTempStep_Label.grid_forget()
        self.MarkovTempStep.grid_forget()

    def _fault_injection(self):
        if self.FaultInjection.get():
            self.MTBF_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+2)
            self.MTBF.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+2)

            self.SDMTBF_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+3)
            self.SDMTBF.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+3)

            self.RunTime_Label.grid(column=self.Fault_StartingCol, row=self.Fault_StartingRow+4)
            self.RunTime.grid(column=self.Fault_StartingCol+1, row=self.Fault_StartingRow+4)
        else:
            self.MTBF_Label.grid_forget()
            self.MTBF.grid_forget()
            self.SDMTBF_Label.grid_forget()
            self.SDMTBF.grid_forget()
            self.RunTime_Label.grid_forget()
            self.RunTime.grid_forget()

    def _check_for_errors(self):
        if self.Mapping.get() == 'Please Select...':
            self.ErrorMessage.config(text="Please Select Mapping Algorithm!")
            return False

        elif self.RoutingAlg.get() == 'Please Select...':
            self.ErrorMessage.config(text="Please Select Routing Algorithm!")
            return False

        elif self.RoutingType.get() == 'Please Select...':
            if self.RoutingAlg.get() not in ['XY', 'XYZ']:
                self.ErrorMessage.config(text="Please Select Routing Type!")
                return False
            else:
                self.ErrorMessage.config(text="")
                return True
        elif self.RoutingAlg.get() == 'From File':
            if self.RoutingBrowse.get() == 'Routing File Path...':
                self.ErrorMessage.config(text="Please Select Routing File!")
                return False
        elif int(self.network_size_z.get()) < 2 and '3D' in self.Topology.get():
            if self.VLPlacementEnable.get():
                self.ErrorMessage.config(text="Can not optimize VL placement for 1 layer NoC")
                return False
        else:
            self.ErrorMessage.config(text="")
            return True

    def _on_enter(self, event):
        tkMessageBox.showinfo("License Message", "The logo picture is a derivative of \"Sea Ghost\" by Joey Gannon, " +
                              "used under CC BY-SA. The original version can be found here: " +
                              "https://www.flickr.com/photos/brunkfordbraun/679827214 " +
                              "This work is under same license as the original."
                              "(https://creativecommons.org/licenses/by-sa/2.0/)")

    def _animation_config(self):
        if self.AnimEnable.get() is True:
            self.FrameRezLabel.grid(column=self.Anim_StartingCol, row=self.Anim_StartingRow+2)
            self.FrameRez.grid(column=self.Anim_StartingCol+1, row=self.Anim_StartingRow+2)
        else:
            self.FrameRez.grid_forget()
            self.FrameRezLabel.grid_forget()

    def _apply_button(self):
        # apply changes...
        if self._check_for_errors():
            # TG Config
            Config.TG_Type = self.TGType.get()
            Config.NumberOfTasks = int(self.NumOfTasks.get())
            Config.NumberOfCriticalTasks = int(self.NumOfCritTasks.get())
            Config.NumberOfEdges = int(self.NumOfEdge.get())
            Config.WCET_Range = int(self.WCET_Range.get())
            Config.EdgeWeightRange = int(self.EdgeWeight_Range.get())
            Config.Release_Range = int(self.Release_Range.get())
            if self.TGType.get() == 'FromDOTFile':
                Config.TG_DOT_Path = self.TGBrowse.get()
            # Topology Config
            Config.NetworkTopology = self.Topology.get()
            Config.Network_X_Size = int(self.network_size_x.get())
            Config.Network_Y_Size = int(self.network_size_y.get())
            Config.Network_Z_Size = int(self.network_size_z.get())

            # Clustering Config
            Config.ClusteringIteration = int(self.ClusteringIterations.get())
            Config.Clustering_Optimization = self.ClusteringOptVar.get()
            Config.Clustering_CostFunctionType = self.ClusterCost.get()

            # Mapping Config

            Config.Mapping_CostFunctionType = self.MappingCost.get()

            Config.LocalSearchIteration = int(self.LS_Iter.get())
            Config.IterativeLocalSearchIterations = int(self.ILS_Iter.get())

            Config.Mapping_Function = self.Mapping.get()
            Config.SA_AnnealingSchedule = self.Annealing.get()
            Config.TerminationCriteria = self.Termination.get()
            Config.SimulatedAnnealingIteration = int(self.SA_Iterations.get())
            Config.SA_InitialTemp = int(self.SA_InitTemp.get())
            Config.SA_StopTemp = int(self.SA_StopTemp.get())
            Config.SA_Alpha = float(self.SA_Alpha.get())
            Config.LogCoolingConstant = int(self.SA_LoG_Const.get())
            Config.CostMonitorQueSize = int(self.CostMonitor.get())
            Config.SlopeRangeForCooling = float(self.CostMonitorSlope.get())
            Config.MaxSteadyState = int(self.MaxSteadyState.get())
            Config.MarkovTempStep = float(self.MarkovTempStep.get())
            Config.MarkovNum = int(self.MarkovNum.get())
            Config.Delta = float(self.SA_Delta.get())

            # Fault Config
            Config.EventDrivenFaultInjection = self.FaultInjection.get()
            Config.MTBF = float(self.MTBF.get())
            Config.SD4MTBF = float(self.SDMTBF.get())
            Config.ProgramRunTime = float(self.RunTime.get())

            # Viz Config
            Config.Mapping_Drawing = self.Mapping_Draw.get()
            Config.RG_Draw = self.RG_Draw.get()
            Config.SHM_Drawing = self.SHM_Draw.get()
            Config.PMCG_Drawing = self.PMCG_Draw.get()
            Config.TTG_Drawing = self.TTG_Draw.get()

            Config.GenMappingFrames = self.AnimEnable.get()
            Config.FrameResolution = int(self.FrameRez.get())

            # Routing
            Config.FlowControl = self.FlowControl.get()

            if self.Topology.get() == 'From File':
                Config.SetRoutingFromFile = True
                Config.RoutingFilePath = self.RoutingBrowse.get()
            else:
                if '3D' in self.Topology.get():
                    if self.RoutingAlg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst3D_TurnModel
                    elif self.RoutingAlg.get() == 'XYZ':
                        Config.UsedTurnModel = PackageFile.XYZ_TurnModel
                elif '2D' in self.Topology.get():
                    if self.RoutingAlg.get() == 'XY':
                        Config.UsedTurnModel = PackageFile.XY_TurnModel
                    elif self.RoutingAlg.get() == 'West First':
                        Config.UsedTurnModel = PackageFile.WestFirst_TurnModel
                    elif self.RoutingAlg.get() == 'North Last':
                        Config.UsedTurnModel = PackageFile.NorthLast_TurnModel
                    elif self.RoutingAlg.get() == 'Negative First':
                        Config.UsedTurnModel = PackageFile.NegativeFirst2D_TurnModel

                if self.RoutingAlg.get() in ['XY', 'XYZ']:
                    if self.RoutingType.get() == 'Please Select...':
                        Config.RotingType = 'MinimalPath'
                else:
                    Config.RotingType = self.RoutingType.get()

            # VL Placement
            # todo: There is something with update from 3D to 2D system.
            Config.FindOptimumAG = self.VLPlacementEnable.get()
            if self.VLPlacementEnable.get():
                Config.VL_OptAlg = self.VLP_Alg.get()
                Config.VerticalLinksNum = int(self.NumOfVLs.get())

            # dependability Config
            Config.Communication_SlackCount = int(self.ComSlackNumber.get())
            Config.Task_SlackCount = int(self.SlackNumber.get())
            Config.NumberOfRects = int(self.NumberOfRects.get())

            # PMC Config
            if self.PMCEnable.get():
                Config.GeneratePMCG = self.PMCEnable.get()
                if self.PMCType.get() == 'One Step Diagnosable':
                    Config.OneStepDiagnosable = True
                    Config.OneStepDiagnosable = int(self.TfaultDiagnosable.get())
                else:
                    Config.OneStepDiagnosable = False

            self.apply_button = True
            self.destroy()

    def _cancel_button(self):
        self.destroy()