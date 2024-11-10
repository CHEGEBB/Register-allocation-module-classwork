def visualize_allocation(allocation, num_registers):
    """Utility function to visualize register allocation"""
    print("\nRegister Allocation Results:")
    print("-" * 40)
    
    by_register = {}
    spilled = []
    
    for var, reg in allocation.items():
        if reg == 'spilled':
            spilled.append(var)
        else:
            if reg not in by_register:
                by_register[reg] = []
            by_register[reg].append(var)
    
    for reg in range(num_registers):  # Fixed line
        if reg in by_register:
            print(f"Register {reg}: {', '.join(by_register[reg])}")
        else:
            print(f"Register {reg}: (empty)")
    
    if spilled:
        print("Spilled Variables:", ", ".join(spilled))
