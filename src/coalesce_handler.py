# coalesce_handler.py
class CoalesceHandler:
    def __init__(self, interference_graph):
        self.graph = interference_graph
        
    def can_coalesce(self, var1, var2):
        v1 = self.graph.variables[var1]
        v2 = self.graph.variables[var2]
        # Check for overlap
        return not (v1.start_point < v2.end_point and v2.start_point < v1.end_point)

        
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
