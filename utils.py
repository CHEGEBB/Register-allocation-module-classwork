def visualize_allocation(allocation, num_registers):
    """Utility function to visualize register allocation"""
    print("\nRegister Allocation Results:")
    print("-" * 40)
    
    # Group by register
    by_register = {}
    spilled = []
    
    for var, reg in allocation.items():
        if reg == 'spilled':
            spilled.append(var)
        else:
            if reg not in by_register:
                by_register[reg] = []
            by_register[reg].append(var)
            
    # Print register assignments
    for reg in range(num_registers):
        vars_in_reg = by_register.get(reg, [])
        print(f"Register {reg}: {', '.join(vars_in_reg) if vars_in_reg else '(empty)'}")
        
    # Print spilled variables
    print("\nSpilled Variables:", ', '.join(spilled) if spilled else "(none)")
