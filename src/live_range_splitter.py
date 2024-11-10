# live_range_splitter.py
class LiveRangeSplitter:
    def __init__(self, interference_graph):
        self.graph = interference_graph
        
    def split_range(self, var_name, split_point):
        """
        Split variable's live range at given point
        Returns: (new_var_name, success)
        """
        if var_name not in self.graph.variables:
            return None, False
            
        var = self.graph.variables[var_name]
        if split_point <= var.start_point or split_point >= var.end_point:
            return None, False
            
        # Create new variable for second part of range
        new_var_name = f"{var_name}_split_{split_point}"
        self.graph.add_variable(new_var_name, split_point, var.end_point)
        
        # Update original variable's range
        var.end_point = split_point
        
        # Copy interferences that overlap with new range
        new_var = self.graph.variables[new_var_name]
        for interfering_var_name in var.interferences:
            interfering_var = self.graph.variables[interfering_var_name]
            if interfering_var.start_point < new_var.end_point and \
               interfering_var.end_point > new_var.start_point:
                self.graph.add_interference(new_var_name, interfering_var_name)
                
        return new_var_name, True
