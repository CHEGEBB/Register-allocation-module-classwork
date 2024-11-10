# Register Allocator Implementation

## Overview
This is a graph-coloring based register allocator that assigns variables to a limited number of physical registers. It handles typical constructs like loops, conditionals, and function calls through live range analysis and interference graphs.

## Project Structure
```
register_allocator/
├── main.py                 # Main register allocator implementation
├── src/
│   ├── __init__.py
│   ├── interference_graph.py    # Handles variable interference tracking
│   ├── graph_coloring.py       # Implements graph coloring algorithm
│   ├── spill_handler.py        # Manages register spilling
│   ├── coalesce_handler.py     # Handles variable coalescing
│   ├── live_range_splitter.py  # Splits variable live ranges
│   └── utils.py                # Utility functions
```

## Components and Their Functions

### 1. Main Register Allocator (`main.py`)
- Primary entry point and orchestrator
- Manages the overall allocation process
- Combines all components (interference graph, coloring, spilling, etc.)
- Provides the main `RegisterAllocator` class with initialization and allocation methods

### 2. Interference Graph (`interference_graph.py`)
- Tracks which variables interfere with each other (live at the same time)
- Maintains a graph where:
  - Nodes represent variables
  - Edges represent interference between variables
- Provides methods to:
  - Add variables and their live ranges
  - Add interference between variables
  - Build the complete interference graph from live ranges

### 3. Graph Coloring (`graph_coloring.py`)
- Implements Chaitin's graph coloring algorithm
- Assigns registers (colors) to variables
- Ensures interfering variables get different registers
- Identifies when spilling is necessary

### 4. Spill Handler (`spill_handler.py`)
- Manages cases when there aren't enough registers
- Decides which variables to spill to memory
- Updates the interference graph after spilling

### 5. Coalesce Handler (`coalesce_handler.py`)
- Combines non-interfering variables to reduce register pressure
- Merges variables that can share the same register
- Updates the interference graph after coalescing

### 6. Live Range Splitter (`live_range_splitter.py`)
- Splits variable live ranges to reduce register pressure
- Creates new variables for different parts of a split range
- Updates the interference graph with split ranges

## How It Works

### 1. Initialization
```python
# Create allocator with specified number of registers
allocator = RegisterAllocator(num_registers=3)

# Define live ranges: (variable_name, start_point, end_point)
live_ranges = [
    ("a", 0, 10),
    ("b", 2, 8),
    ("c", 5, 15)
]

# Initialize allocator with live ranges
allocator.initialize(live_ranges)
```

### 2. Allocation Process
1. Build interference graph:
   - Creates nodes for each variable
   - Adds edges between variables with overlapping live ranges

2. Attempt graph coloring:
   - Try to assign registers (colors) to variables
   - Ensure interfering variables get different registers

3. Handle spilling if necessary:
   - If not enough registers, choose variables to spill
   - Update interference graph
   - Retry coloring

4. Return allocation results:
   - Dictionary mapping variables to registers or 'spilled'

### 3. Testing
```python
# Run the test file
python test_allocator.py
```

The test file checks:
- Basic non-overlapping variables
- Overlapping variables
- Complex patterns
- Spill handling

## Example Usage

```python
from main import RegisterAllocator

# Create allocator
allocator = RegisterAllocator(num_registers=3)

# Define live ranges
live_ranges = [
    ("x", 0, 5),   # Variable x lives from point 0 to 5
    ("y", 2, 7),   # Variable y lives from point 2 to 7
    ("z", 6, 10)   # Variable z lives from point 6 to 10
]

# Initialize and allocate
allocator.initialize(live_ranges)
allocation = allocator.allocate_registers()

# Print results
print(allocation)
# Example output: {'x': 0, 'y': 1, 'z': 0}
```

## Understanding the Output

The allocator returns a dictionary where:
- Keys are variable names
- Values are either:
  - Register numbers (0, 1, 2, etc.)
  - 'spilled' (variable must be stored in memory)

Example output:
```python
{
    'x': 0,         # Variable x is in register 0
    'y': 1,         # Variable y is in register 1
    'z': 'spilled'  # Variable z is spilled to memory
}
```

## Common Scenarios

### 1. Non-interfering Variables
```python
live_ranges = [
    ("a", 0, 5),
    ("b", 6, 10)
]
# These can share the same register since their live ranges don't overlap
```

### 2. High Register Pressure
```python
live_ranges = [
    ("a", 0, 10),
    ("b", 0, 10),
    ("c", 0, 10),
    ("d", 0, 10)
]
# With 3 registers, one variable must be spilled
```

### 3. Nested Ranges
```python
live_ranges = [
    ("a", 0, 20),
    ("b", 5, 15),
    ("c", 8, 12)
]
# These all interfere and need different registers
```

## Error Handling
The allocator handles:
- Invalid live ranges
- Insufficient registers
- Maximum spilling attempts
- Graph coloring failures

## Performance Considerations
- Graph coloring is NP-complete
- Uses heuristics for spill decisions
- Maximum attempts limit prevents infinite loops
- Coalescing and splitting help reduce register pressure
