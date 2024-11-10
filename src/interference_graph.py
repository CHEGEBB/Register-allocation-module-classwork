# interference_graph.py
class Variable:
    def __init__(self, name, start_point, end_point):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.spilled = False
        self.register = None
        self.interferences = set()

class InterferenceGraph:
    def __init__(self):
        self.variables = {}  # name -> Variable
        self.edges = set()   # set of (var1, var2) tuples
        
    def add_variable(self, name, start_point, end_point):
        var = Variable(name, start_point, end_point)
        self.variables[name] = var
        return var
        
    def add_interference(self, var1_name, var2_name):
        if var1_name not in self.variables or var2_name not in self.variables:
            return
        
        var1 = self.variables[var1_name]
        var2 = self.variables[var2_name]
        
        if (var1.name, var2.name) not in self.edges:
            self.edges.add((var1.name, var2.name))
            self.edges.add((var2.name, var1.name))
            var1.interferences.add(var2.name)
            var2.interferences.add(var1.name)
            
    def build_from_live_ranges(self, live_ranges):
        """
        Build interference graph from live ranges
        live_ranges: List of (variable_name, start_point, end_point)
        """
        # First add all variables
        for var_name, start, end in live_ranges:
            self.add_variable(var_name, start, end)
            
        # Then add interferences
        for var1_name, start1, end1 in live_ranges:
            for var2_name, start2, end2 in live_ranges:
                if var1_name != var2_name:
                    # Check if ranges overlap
                    if not (end1 < start2 or end2 < start1):
                        self.add_interference(var1_name, var2_name)
