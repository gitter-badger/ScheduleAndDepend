# Copyright (C) 2015 Siavoosh Payandeh Azad

# starting to write the simulator with SimPy...
import simpy
import numpy

from ConfigAndPackages import Config
from FaultInjector import fault_event
from SystemHealthMonitoring.FaultClassifier import CounterThreshold     # Rene's addition
from SystemHealthMonitoring.FaultClassifier import MachineLearning      # Rene's addition
from Scheduler import Scheduling_Reports, Scheduling_Functions


def processor_sim(env, node, schedule, schedule_length, counter_threshold, logging):
    """
    Runs tasks on each node
    :param env: simulation environment
    :param node: Node ID number
    :param schedule: schedule of the tasks on the Node
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    while True:
        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0]:
                length = schedule[key][1]-schedule[key][0]
                print float("{0:.1f}".format(env.now)), "\tNODE:: Found Task", key, " to run on Node:", node, "For:", \
                    length, "Cycles"
                found = True
                task_num = key
                break
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tNODE:: Starting Task", task_num, "on Node:", node
            for i in range(0, int(length)):
                yield env.timeout(1)
                counter_threshold.increase_health_counter(node, logging)

            print float("{0:.1f}".format(env.now)), "\tNODE:: Task", task_num, "execution finished on Node", node
            found = False
        else:
            yield env.timeout(1)


def router_sim(env, node, schedule, schedule_length, counter_threshold, logging):
    """
    runs tasks on the routers
    :param env: simulation environment
    :param node: ID of the node to be simulated
    :param schedule: schedule of the tasks on the Router
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    # print "HERE:",Schedule
    while True:

        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0][0]:
                length = schedule[key][0][1]-schedule[key][0][0]
                print float("{0:.1f}".format(env.now)), "\tRouter:: Found Task", key, " to run on Router:", node,\
                    "For:", length, "Cycles"
                found = True
                task_num = key
                break
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tRouter:: Starting Task", task_num, "on Router:", node
            location_dict = {node: "R"}
            for i in range(0, int(length)):
                yield env.timeout(1)
                counter_threshold.increase_health_counter(location_dict, logging)
            print float("{0:.1f}".format(env.now)), "\tRouter:: Task", task_num, "execution finished on Router", node
            found = False
        else:
            yield env.timeout(1)


def link_sim(env, link, schedule, schedule_length, counter_threshold, logging):
    """
    Runs tasks on each link
    :param env: simulation environment
    :param link: link number
    :param schedule: schedule of the tasks on the link
    :param counter_threshold: counter threshold object
    :param logging: logging file
    :return:
    """
    found = False
    task_num = None
    length = 0
    while True:
        for key in schedule.keys():
            # checks if there is a task that starts at this time!
            if env.now % schedule_length == schedule[key][0][0]:
                length = schedule[key][0][1]-schedule[key][0][0]
                print float("{0:.1f}".format(env.now)), "\tLINK:: Found Task", key, " to run on Link:", link, \
                    "For:", length, "Cycles"
                found = True
                task_num = key
        # found a task that starts at this time!
        if found:
            print float("{0:.1f}".format(env.now)), "\tLINK:: Starting Task", task_num, "on Link:", link
            for i in range(0, int(length)):
                yield env.timeout(1)
                counter_threshold.increase_health_counter(link, logging)
            yield env.timeout(length)
            print float("{0:.1f}".format(env.now)), "\tLINK:: Task", task_num, "execution finished on Link", link
            found = False
        else:
            yield env.timeout(1)


def run_simulator(runtime, ag, shmu, noc_rg, logging):
    """
    prepares and runs the simulator
    :param runtime: duration of which the user wants to run the program in cycles
    :param ag: architecture graph
    :param shmu: system health monitoring unit
    :param noc_rg: noc routing graph
    :param logging: logging file
    :return: None
    """
    print "==========================================="
    print "SETTING UP THE SIMULATOR..."
    env = simpy.Environment()
    print "SETTING UP counter-threshold MODULE..."
    if Config.classification_method == "counter_threshold":

        counter_threshold = CounterThreshold.CounterThreshold(Config.fault_counter_threshold,
                                                              Config.health_counter_threshold,
                                                              Config.intermittent_counter_threshold)
    elif Config.classification_method == "machine_learning":
        counter_threshold = MachineLearning.MachineLearning(Config.fault_counter_threshold,     # Rene's addition
                                                            Config.health_counter_threshold*3,
                                                            Config.intermittent_counter_threshold)
    else:
        raise ValueError("Unknown Classification Method!! Check config file")

    fault_time_list = []
    fault_time = 0
    schedule_length = Scheduling_Functions.FindScheduleMakeSpan(ag)
    if Config.EventDrivenFaultInjection:
        time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
        fault_time += time_until_next_fault
        while fault_time < runtime:
            fault_time_list.append(float("{0:.1f}".format(fault_time)))
            time_until_next_fault = numpy.random.normal(Config.MTBF, Config.SD4MTBF)
            fault_time += time_until_next_fault

        # print "------------------------"
        # print "RANDOMLY GENERATED FAULT TIME LIST:",
        # for i in range(0, len(fault_time_list)):
        #     if i % 10 == 0:
        #         print ""
        #         print "\t\t",
        #     else:
        #         print fault_time_list[i], ", ",
        # print ""
        # print "-----------------------"

        env.process(fault_event(env, ag, shmu, noc_rg, schedule_length, fault_time_list, counter_threshold, logging))

    print "SETTING UP ROUTERS AND PES..."
    for node in ag.nodes():
        # print node, AG.node[node]["Scheduling"]
        env.process(processor_sim(env, node, ag.node[node]['PE'].Scheduling, schedule_length,
                                  counter_threshold, logging))
        env.process(router_sim(env, node, ag.node[node]['Router'].Scheduling, schedule_length,
                               counter_threshold, logging))

    print "SETTING UP LINKS..."
    for link in ag.edges():
        # print link, AG.edge[link[0]][link[1]]["Scheduling"]
        env.process(link_sim(env, link, ag.edge[link[0]][link[1]]["Scheduling"], schedule_length,
                             counter_threshold, logging))

    print "STARTING SIMULATION..."
    env.run(until=runtime)
    print "SIMULATION FINISHED..."
    counter_threshold.report(len(ag.nodes()), len(ag.edges()))
    Scheduling_Reports.report_scheduling_memory_usage(ag)
    return None
