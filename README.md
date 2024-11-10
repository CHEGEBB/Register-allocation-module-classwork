# Register Allocator

## Overview
This project implements a register allocator using a graph-coloring algorithm to optimize register assignment in a compiler backend. It handles variable interference, spilling, coalescing, and live range splitting.

## Usage
1. Install Python 3.x if not already installed.
2. Place all Python files in the `register_allocator` directory.
3. Run the allocator by executing the following command:

    ```bash
    python main.py
    ```

## How It Works
- `interference_graph.py`: Builds an interference graph for variable live ranges.
- `graph_coloring.py`: Applies the graph-coloring algorithm to allocate registers.
- `spilling.py`: Manages spilling by moving excess variables to memory.
- `coalescing.py`: Reduces register usage by merging variables with no interference.
- `live_range_splitter.py`: Splits live ranges to reduce high register demand.

## Output
The `main.py` script will output the assigned registers, spilled variables, and coalesced pairs.
