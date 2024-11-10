from interference_graph import InterferenceGraph
from graph_coloring import GraphColoring
from spill_handler import SpillHandler
from coalesce_handler import CoalesceHandler
from live_range_splitter import LiveRangeSplitter

class RegisterAllocator:
    def __init__(self, num_registers):
        self.num_registers = num_registers
        self.interference_graph = InterferenceGraph()
        self.graph_coloring = None
        self.spill_handler = None
        self.coalesce_handler = None
        self.live_range_splitter = None

    def initialize(self, live_ranges):
        self.interference_graph.build_from_live_ranges(live_ranges)
        self.graph_coloring = GraphColoring(self.interference_graph, self.num_registers)
        self.spill_handler = SpillHandler(self.interference_graph)
        self.coalesce_handler = CoalesceHandler(self.interference_graph)
        self.live_range_splitter = LiveRangeSplitter(self.interference_graph)

    def get_next_available_register(self, current_time, register_usage, used_registers):
        """
        Find the next available register at the given time.
        """
        for reg in range(self.num_registers):
            if reg not in used_registers:
                is_available = True
                for time, regs in register_usage.items():
                    if time <= current_time and reg in regs:
                        is_available = False
                        break
                if is_available:
                    return reg
        return None

    def allocate_registers(self):
        # Initialize register allocation
        allocation = {}
        register_usage = {}  # time -> set of registers in use
        
        # Create timeline of all start and end points
        timeline = []
        for var_name, var in self.interference_graph.variables.items():
            timeline.append((var.start_point, 'start', var_name))
            timeline.append((var.end_point, 'end', var_name))
        
        # Sort timeline by time
        timeline.sort()
        
        # Keep track of active variables at each point
        active_vars = set()
        
        # Process timeline events
        for time, event_type, var_name in timeline:
            if event_type == 'start':
                var = self.interference_graph.variables[var_name]
                
                # Get current register usage
                used_registers = set()
                for active_var in active_vars:
                    if active_var in allocation and allocation[active_var] != 'spilled':
                        used_registers.add(allocation[active_var])
                
                # Find an available register
                reg = None
                for r in range(self.num_registers):
                    if r not in used_registers:
                        # Check if this register is compatible with all active variables
                        is_compatible = True
                        for active_var in active_vars:
                            if active_var in allocation and allocation[active_var] == r:
                                active_var_obj = self.interference_graph.variables[active_var]
                                if not (active_var_obj.end_point <= var.start_point or 
                                      var.end_point <= active_var_obj.start_point):
                                    is_compatible = False
                                    break
                        if is_compatible:
                            reg = r
                            break
                
                if reg is not None:
                    allocation[var_name] = reg
                    if time not in register_usage:
                        register_usage[time] = set()
                    register_usage[time].add(reg)
                else:
                    # If no register is available, mark as spilled
                    allocation[var_name] = 'spilled'
                
                active_vars.add(var_name)
            
            else:  # event_type == 'end'
                active_vars.remove(var_name)
                # Free up the register
                if time in register_usage and var_name in allocation:
                    register_usage[time].discard(allocation[var_name])

        # Post-process to ensure no overlapping variables have same register
        for var1_name, var1 in self.interference_graph.variables.items():
            if allocation[var1_name] != 'spilled':
                for var2_name, var2 in self.interference_graph.variables.items():
                    if (var1_name != var2_name and 
                        allocation[var2_name] != 'spilled' and 
                        allocation[var1_name] == allocation[var2_name]):
                        
                        # Check if their live ranges overlap
                        if not (var1.end_point <= var2.start_point or 
                               var2.end_point <= var1.start_point):
                            
                            # Try to find a different register for var2
                            new_reg = None
                            for reg in range(self.num_registers):
                                if reg != allocation[var1_name]:
                                    can_use = True
                                    for other_var, _ in self.interference_graph.variables.items():
                                        if (other_var != var2_name and 
                                            allocation.get(other_var) == reg):
                                            can_use = False
                                            break
                                    if can_use:
                                        new_reg = reg
                                        break
                            
                            if new_reg is not None:
                                allocation[var2_name] = new_reg
                            else:
                                allocation[var2_name] = 'spilled'

        return allocation