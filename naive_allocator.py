class NaiveAllocator:
    def __init__(self, num_registers):
        self.num_registers = num_registers
    
    def allocate_registers(self, live_ranges):
        """
        Naively allocate registers to variables without considering interference.
        Returns a dictionary of variable_name -> register_number or 'spilled'
        """
        allocation = {}
        for i, (var_name, _, _) in enumerate(live_ranges):
            if i < self.num_registers:
                allocation[var_name] = i  # Assign a register if available
            else:
                allocation[var_name] = 'spilled'  # Spill if no registers are available
        return allocation
