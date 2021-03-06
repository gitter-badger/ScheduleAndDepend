# Copyright (C) 2015 Siavoosh Payandeh Azad

# This approach is based on the following paper: "A Fault Prediction Module for a Fault Tolerant NoC Operation"
# by Silveira, J.; Bodin, M.; Ferreira, J.M.; Cadore Pinheiro, A.; Webber, T.; Marcon, C.

from ConfigAndPackages import Config
from math import ceil, log


class CounterThreshold():

    def __init__(self, fault_threshold, health_threshold, intermittent_threshold):
        # These dictionaries keep the values of the counters where the key is the location!
        # locations are either Processing Elements which are represented by their number (1,2,...)
        # or are Routers which are represented like R0, R1,...
        # or links which are represented like L01 which describes the link from node 0 to node 1
        self.fault_counters = {}
        self.intermittent_counters = {}
        self.health_counters = {}

        # these values are the threshold used by the system for deciding about components health and reseting them
        self.fault_threshold = fault_threshold
        self.intermittent_threshold = intermittent_threshold
        self.health_threshold = health_threshold

        # these lists keep the location of intermittent or permanently damaged components.
        self.dead_components = []
        self.intermittent_components = []
        self.comp_of_interest = []
        # used for reports
        self.memory_counter = 0
        self.number_of_faults = 0
        self.max_comp_of_interest = 0
        self.counters_f_report = {}
        self.counters_i_report = {}
        self.counters_h_report = {}
        self.viz_counter_list = {}

    def increase_health_counter(self, ag, location, logging):
        if type(location) is dict:
            # location is a router: {node_1: [turn]}
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            location = "R"+str(location.keys()[0])
        elif type(location) is tuple:
            # location is a link: (node1, node 2)
            # print location, location[0], location[1]
            location = "L"+str(location[0])+str(location[1])
        elif type(location) is int:
            # location is a node
            # print location
            location = str(location)
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")

        if location in self.dead_components:
            # do not increase the counter if component is dead
            return None
        if location in self.fault_counters.keys() or location in self.intermittent_counters.keys():
            pass
        else:
            # do not start the health counter if there is no fault or intermittent counter
            return None

        # increase the health counter
        if location in self.health_counters.keys():
            self.health_counters[location] += 1
        else:
            self.health_counters[location] = 1
        self.update_report_dict(ag)
        logging.info("Increasing health counter at location: "+location +
                     " Counter: "+str(self.health_counters[location]))
        # check for reaching the threshold
        if self.health_counters[location] == self.health_threshold:
            logging.info("resetting component: "+location+" counters")
            # heal the intermittent component
            if location in self.intermittent_components:
                self.intermittent_components.remove(location)
            self.reset_counters(location)

        current_memory_usage = self.return_allocated_memory()
        if current_memory_usage > self.memory_counter:
            self.memory_counter = current_memory_usage
        if len(self.comp_of_interest) > self.max_comp_of_interest:
            self.max_comp_of_interest = len(self.comp_of_interest)
        return None

    def increase_intermittent_counter(self, ag, location, logging):
        if type(location) is dict:
            # location is a router: {node_1: [turn]}
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            if Config.enable_router_counters:
                location = "R"+str(location.keys()[0])
            else:
                return None
        elif type(location) is tuple:
            # location is a link: (node1, node 2)
            # print location, location[0], location[1]
            if Config.enable_link_counters:
                location = "L"+str(location[0])+str(location[1])
            else:
                return None
        elif type(location) is int:
            # location is a node
            # print location
            if Config.enable_pe_counters:
                location = str(location)
            else:
                return None
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")

        if location in self.dead_components:
            # do not increase the counter if component is dead
            return None

        if location not in self.health_counters:
            self.generate_counters(location)

        self.number_of_faults += 1
        # Increase the intermittent counter for the specified location
        if location in self.intermittent_counters.keys():
            self.intermittent_counters[location] += 1
        self.update_report_dict(ag)
        logging.info("Increasing intermittent counter at location: "+location+" Counter: " +
                     str(self.intermittent_counters[location]))

        # Check for reaching Threshold
        if self.intermittent_counters[location] == self.fault_threshold:
            logging.info("Declaring component: "+location+" intermittent!")
            if location not in self.intermittent_components:
                self.intermittent_components.append(location)
            self.reset_counters(location)

        current_memory_usage = self.return_allocated_memory()
        if current_memory_usage > self.memory_counter:
            self.memory_counter = current_memory_usage
        if len(self.comp_of_interest) > self.max_comp_of_interest:
            self.max_comp_of_interest = len(self.comp_of_interest)
        return None

    def increase_fault_counter(self, ag, location, logging):
        if type(location) is dict:
            # location is a router: {node_1: [turn]}
            # print location, str(location.keys()[0])+str(location[location.keys()[0]])
            if Config.enable_router_counters:
                location = "R"+str(location.keys()[0])
            else:
                return None
        elif type(location) is tuple:
            # location is a link: (node1, node 2)
            # print location, location[0], location[1]
            if Config.enable_link_counters:
                location = "L"+str(location[0])+str(location[1])
            else:
                return None
        elif type(location) is int:
            # location is a node
            # print location
            if Config.enable_pe_counters:
                location = str(location)
            else:
                return None
        else:
            print location, type(location)
            raise ValueError("location type is wrong!")

        if location in self.dead_components:
            # do not increase the counter if component is dead
            return None

        if location not in self.health_counters:
            self.generate_counters(location)
        self.number_of_faults += 1
        # increase the fault Counter
        if location in self.fault_counters.keys():
            self.fault_counters[location] += 1
        self.update_report_dict(ag)
        logging.info("Increasing counter at location: "+location+" Counter: "+str(self.fault_counters[location]))

        # Check for reaching threshold
        if self.fault_counters[location] == self.fault_threshold:
            logging.info("Declaring component: "+location+" dead!")
            self.dead_components.append(location)
            if location in self.intermittent_components:
                self.intermittent_components.remove(location)
            self.reset_counters(location)

        current_memory_usage = self.return_allocated_memory()
        if current_memory_usage > self.memory_counter:
            self.memory_counter = current_memory_usage
        if len(self.comp_of_interest) > self.max_comp_of_interest:
            self.max_comp_of_interest = len(self.comp_of_interest)
        return None

    def reset_counters(self, location):
        """
        resets the counters in a specific location and releases the memory
        :param location: location of the counters to be reset
        :return: None
        """
        if location in self.fault_counters.keys():
            del self.fault_counters[location]
        if location in self.intermittent_counters.keys():
            del self.intermittent_counters[location]
        if location in self.health_counters.keys():
            del self.health_counters[location]
        if location in self.comp_of_interest:
            self.comp_of_interest.remove(location)
        return None

    def generate_counters(self, location):
        self.fault_counters[location] = 0
        self.intermittent_counters[location] = 0
        self.health_counters[location] = 0
        self.comp_of_interest.append(location)
        return None

    def update_report_dict(self, ag):
        for node in ag.nodes():
            location = str(node)
            self.update_report_list(location)
            location = "R"+str(node)
            self.update_report_list(location)
        for link in ag.edges():
            location = "L"+str(link[0])+str(link[1])
            self.update_report_list(location)

    def update_report_list(self, location):
        if location not in self.counters_f_report.keys():
            self.counters_f_report[location] = []
            self.counters_h_report[location] = []
            self.counters_i_report[location] = []
            self.viz_counter_list[location] = []
        if location in self.fault_counters.keys():

            if self.fault_counters[location] > self.counters_f_report[location][-1]:
                self.counters_f_report[location].append(self.counters_f_report[location][-1])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.health_counters[location])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1]+1)

                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.health_counters[location])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1])

            elif self.intermittent_counters[location] > self.counters_i_report[location][-1]:
                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.counters_i_report[location][-1])
                self.counters_h_report[location].append(self.health_counters[location])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1]+1)

                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.health_counters[location])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1])

            elif self.health_counters[location] > self.counters_h_report[location][-1]:
                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.counters_h_report[location][-1])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1]+1)

                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.health_counters[location])
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1])
            else:
                self.counters_f_report[location].append(self.fault_counters[location])
                self.counters_i_report[location].append(self.intermittent_counters[location])
                self.counters_h_report[location].append(self.health_counters[location])
                if len(self.viz_counter_list[location]) == 0:
                    self.viz_counter_list[location].append(0)
                else:
                    self.viz_counter_list[location].append(self.viz_counter_list[location][-1]+1)

            if self.fault_counters[location] == self.fault_threshold or \
               self.intermittent_counters[location] == self.intermittent_threshold or\
               self.health_counters[location] == self.health_threshold:

                self.counters_f_report[location].append(0)
                self.counters_i_report[location].append(0)
                self.counters_h_report[location].append(0)
                if len(self.viz_counter_list[location]) == 0:
                    self.viz_counter_list[location].append(0)
                else:
                    self.viz_counter_list[location].append(self.viz_counter_list[location][-1])
        else:
            self.counters_f_report[location].append(0)
            self.counters_i_report[location].append(0)
            self.counters_h_report[location].append(0)
            if len(self.viz_counter_list[location]) == 0:
                self.viz_counter_list[location].append(0)
            else:
                self.viz_counter_list[location].append(self.viz_counter_list[location][-1]+1)
        return None

    def return_allocated_memory(self):
        return len(self.health_counters) + len(self.fault_counters) + len(self.intermittent_counters)

    def report(self, number_of_nodes, number_of_links):
        print "==========================================="
        print "        COUNTER-THRESHOLD REPORT"
        print "==========================================="
        print "DEAD Components:", self.dead_components
        print "Intermittent Components:", self.intermittent_components
        # number of links + number of routers + number of PEs
        number_of_components = number_of_links + 2 * number_of_nodes
        bits_required_for_address = ceil(log(number_of_components, 2))

        print "MAX NUMBER OF COUNTERS:", self.memory_counter
        print "\t| NUMBER OF BITS FOR ADDRESS FOR EACH COUNTER:", bits_required_for_address
        max_counter_bits = max(ceil(log(Config.fault_counter_threshold)), ceil(log(Config.health_counter_threshold)),
                               ceil(log(Config.intermittent_counter_threshold)))
        print "\t| MAX NUMBER OF BITS FOR EACH COUNTER:", max_counter_bits
        counter_total_bits = max_counter_bits + bits_required_for_address
        print "\t| TOTAL BITS PER COUNTER:", counter_total_bits

        print "\t| MAX LEN OF COMP OF INTEREST:", self.max_comp_of_interest

        print "MAX MEM USAGE:", self.memory_counter * counter_total_bits, " BITS"
        print "AVERAGE COUNTER PER Node: ", float(self.memory_counter)/number_of_nodes
        print "AVERAGE BITS PER Node: ", float(self.memory_counter * counter_total_bits)/number_of_nodes
        print "NUMBER OF FAULTS:", self.number_of_faults
        return None