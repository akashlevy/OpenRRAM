import globals
import design
from math import log
import design
from tech import GDS,layer,spice,parameter
import utils

class dff(design.design):
    """
    Memory address flip-flop
    """

    pin_names = ["D", "Q", "clk", "vdd", "gnd"]
    (width,height) = utils.get_libcell_size("dff", GDS["unit"], layer["boundary"])
    pin_map = utils.get_libcell_pins(pin_names, "dff", GDS["unit"])
    
    def __init__(self, name="dff"):
        design.design.__init__(self, name)

        self.width = dff.width
        self.height = dff.height
        self.pin_map = dff.pin_map
    
    def analytical_power(self, corner, load):
        """Returns dynamic and leakage power. Results in nW"""
        c_eff = self.calculate_effective_capacitance(load)
        freq = spice["default_event_rate"]
        power_dyn = self.calc_dynamic_power(corner, c_eff, freq)
        power_leak = spice["msflop_leakage"]
        
        total_power = self.return_power(power_dyn, power_leak)
        return total_power
        
    def calculate_effective_capacitance(self, load):
        """Computes effective capacitance. Results in fF"""
        from tech import parameter
        c_load = load
        c_para = spice["flop_para_cap"]#ff
        transition_prob = spice["flop_transition_prob"]
        return transition_prob*(c_load + c_para) 

    def analytical_delay(self, corner, slew, load = 0.0):
        # dont know how to calculate this now, use constant in tech file
        result = self.return_delay(spice["dff_delay"], spice["dff_slew"])
        return result
        
    def get_clk_cin(self):
        """Return the total capacitance (in relative units) that the clock is loaded by in the dff"""
        #This is a handmade cell so the value must be entered in the tech.py file or estimated.
        #Calculated in the tech file by summing the widths of all the gates and dividing by the minimum width.
        return parameter["dff_clk_cin"]

    def build_graph(self, graph, inst_name, port_nets):        
        """Adds edges to graph. Handmade cells must implement this manually."""
        #The cell has 5 net ports hard-coded in self.pin_names. The edges
        #are based on the hard-coded name positions.
        # The edges added are: clk->Q.
        # Internal nodes of the handmade cell not considered, only ports. vdd/gnd ignored for graph.
        graph.add_edge(port_nets[2],port_nets[1])
        