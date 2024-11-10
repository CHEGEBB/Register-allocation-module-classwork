class GraphColoring:
    def __init__(self, interference_graph, num_registers):
        self.graph = interference_graph
        self.num_registers = num_registers
        self.colors = {}  # variable_name -> color (register number)
        
    def color_graph(self):
        """
        Implements graph coloring using Chaitin's algorithm
        Returns: (success, spill_candidates)
        """
        for var in self.graph.variables:
            # Ensure all nodes are either colored or marked for spilling
            if len(self.colors) >= self.num_registers:
                return False, [var for var in self.graph.variables if var not in self.colors]
        stack = []
        remaining_nodes = set(self.graph.variables.keys())
        spill_candidates = set()
        
        # Build stack of nodes
        while remaining_nodes:
            found_node = None
            for node in remaining_nodes:
                if len(self.graph.variables[node].interferences) < self.num_registers:
                    found_node = node
                    break
                    
            if found_node is None:
                # Need to spill - choose highest degree node
                spill_node = max(remaining_nodes, 
                               key=lambda x: len(self.graph.variables[x].interferences))
                spill_candidates.add(spill_node)
                remaining_nodes.remove(spill_node)
            else:
                stack.append(found_node)
                remaining_nodes.remove(found_node)
                
        # Assign colors
        success = True
        while stack and success:
            node = stack.pop()
            used_colors = set()
            for neighbor in self.graph.variables[node].interferences:
                if neighbor in self.colors:
                    used_colors.add(self.colors[neighbor])
                    
            available_colors = set(range(self.num_registers)) - used_colors
            if available_colors:
                self.colors[node] = min(available_colors)
            else:
                success = False
                
        return success, spill_candidates
