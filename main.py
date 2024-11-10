# Project structure:
# │
# ├── main.py
# ├── src/
# │   ├── __init__.py
# │   ├── interference_graph.py
# │   ├── graph_coloring.py
# │   ├── spill_handler.py
# │   ├── coalesce_handler.py
# │   ├── live_range_splitter.py
# │   └── utils.py
# └── README.md

# main.py
from src.interference_graph import InterferenceGraph
from src.graph_coloring import GraphColoring
from src.spill_handler import SpillHandler
from src.coalesce_handler import CoalesceHandler
from src.live_range_splitter import LiveRangeSplitter
from src.utils import visualize_allocation

class RegisterAllocator:
    def __init__(self, num_registers):
        self.num_registers = num_registers
        self.interference_graph = InterferenceGraph()
        self.graph_coloring = None
        self.spill_handler = None
        self.coalesce_handler = None
        self.live_range_splitter = None
        
    def initialize(self, live_ranges):
        """
        Initialize the register allocator with live ranges
        live_ranges: List of (variable_name, start_point, end_point)
        """
        self.interference_graph.build_from_live_ranges(live_ranges)
        self.graph_coloring = GraphColoring(self.interference_graph, self.num_registers)
        self.spill_handler = SpillHandler(self.interference_graph)
        self.coalesce_handler = CoalesceHandler(self.interference_graph)
        self.live_range_splitter = LiveRangeSplitter(self.interference_graph)
        
    def allocate_registers(self):
        """
        Main register allocation algorithm
        Returns: Dict of variable_name -> register_number or 'spilled'
        """
        allocation = {}
        max_attempts = 3  # Limit number of spilling attempts
        
        for attempt in range(max_attempts):
            success, spill_candidates = self.graph_coloring.color_graph()
            
            if success:
                # Successful allocation
                for var_name, color in self.graph_coloring.colors.items():
                    allocation[var_name] = color
                for var_name, var in self.interference_graph.variables.items():
                    if var.spilled:
                        allocation[var_name] = 'spilled'
                return allocation
                
            # Handle spilling
            self.spill_handler.handle_spills(spill_candidates)
            
        # If we reach here, we couldn't allocate after max attempts
        for var_name in self.interference_graph.variables:
            allocation[var_name] = 'spilled'
        return allocation

def main():
    # Example usage
    print("Register Allocator")
    print("=================")
    
    # Example live ranges
    live_ranges = [
        ("a", 0, 10),  # Variable 'a' lives from point 0 to 10
        ("b", 2, 8),   # Variable 'b' lives from point 2 to 8
        ("c", 5, 15),  # Variable 'c' lives from point 5 to 15
        ("d", 7, 12),  # Variable 'd' lives from point 7 to 12
        ("e", 9, 14)   # Variable 'e' lives from point 9 to 14
    ]
    
    # Create allocator with 3 physical registers
    num_registers = 3
    allocator = RegisterAllocator(num_registers)
    
    print(f"\nAllocating registers for {len(live_ranges)} variables using {num_registers} registers...")
    
    # Initialize with live ranges
    allocator.initialize(live_ranges)
    
    # Perform allocation
    allocation = allocator.allocate_registers()
    
    # Visualize results
    visualize_allocation(allocation, num_registers)
    
    # Print detailed allocation information
    print("\nDetailed Allocation Information:")
    print("--------------------------------")
    for var_name, register in allocation.items():
        if register == 'spilled':
            print(f"Variable {var_name}: Spilled to memory")
        else:
            print(f"Variable {var_name}: Assigned to register {register}")
            
    # Print interference information
    print("\nInterference Information:")
    print("------------------------")
    for var_name in allocator.interference_graph.variables:
        var = allocator.interference_graph.variables[var_name]
        interfering_vars = list(var.interferences)
        print(f"Variable {var_name} interferes with: {', '.join(interfering_vars) if interfering_vars else 'none'}")

if __name__ == "__main__":
    main()