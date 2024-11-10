class SpillHandler:
    def __init__(self, interference_graph):
        self.graph = interference_graph
        
    def handle_spills(self, spill_candidates):
        """
        Marks variables for spilling and updates interference graph
        Returns modified interference graph
        """
        for var_name in spill_candidates:
            var = self.graph.variables[var_name]
            var.spilled = True
            
            # Remove interferences for spilled variable
            for interfering_var in var.interferences.copy():
                self.graph.variables[interfering_var].interferences.remove(var_name)
                var.interferences.remove(interfering_var)
                self.graph.edges.remove((var_name, interfering_var))
                self.graph.edges.remove((interfering_var, var_name))
                
        return self.graph
