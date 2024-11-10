from interference_graph import InterferenceGraph
from graph_coloring import GraphColoring
from spilling import SpillingHandler
from coalescing import CoalescingHandler
from live_range_splitter import LiveRangeSplitter

class RegisterAllocator:
    def __init__(self, live_ranges, num_registers=8):
        self.live_ranges = live_ranges
        self.num_registers = num_registers

    def allocate(self):
        # Step 1: Build interference graph
        interference_graph = InterferenceGraph(self.live_ranges)
        
        # Step 2: Apply live range splitting (if necessary)
        splitter = LiveRangeSplitter(self.live_ranges)
        split_points = splitter.split_ranges()

        # Step 3: Apply graph coloring to assign registers
        graph_coloring = GraphColoring(interference_graph.graph, self.num_registers)
        colors = graph_coloring.color_graph()

        # Step 4: Handle spills if registers are insufficient
        spilling_handler = SpillingHandler(interference_graph.graph, colors)
        spills = spilling_handler.handle_spills()

        # Step 5: Coalesce non-interfering variables
        coalescing_handler = CoalescingHandler(interference_graph.graph)
        coalesced_pairs = coalescing_handler.coalesce()

        # Final register assignments and spills
        return colors, spills, coalesced_pairs

if __name__ == "__main__":

