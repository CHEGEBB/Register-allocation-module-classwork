# coalesce_handler.py
class CoalesceHandler:
    def __init__(self, interference_graph):
        self.graph = interference_graph
        
    def can_coalesce(self, var1_name, var2_name):
        """Check if two variables can be coalesced"""
        var1 = self.graph.variables[var1_name]
        var2 = self.graph.variables[var2_name]
        
        # Cannot coalesce if they interfere
        if var2_name in var1.interferences:
            return False
            
        # Cannot coalesce if combined interference set would be too large
        combined_interferences = var1.interferences.union(var2.interferences)
        if len(combined_interferences) >= len(self.graph.variables):
            return False
            
        return True
        
    def coalesce_variables(self, var1_name, var2_name):
        """
        Coalesce two variables by merging their live ranges
        Returns True if successful
        """
        if not self.can_coalesce(var1_name, var2_name):
            return False
            
        var1 = self.graph.variables[var1_name]
        var2 = self.graph.variables[var2_name]
        
        # Merge live ranges
        var1.start_point = min(var1.start_point, var2.start_point)
        var1.end_point = max(var1.end_point, var2.end_point)
        
        # Merge interference sets
        for interfering_var in var2.interferences:
            self.graph.add_interference(var1_name, interfering_var)
            
        # Remove var2
        del self.graph.variables[var2_name]
        return True
