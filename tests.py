import pytest
from src.interference_graph import InterferenceGraph, Variable
from src.graph_coloring import GraphColoring
from src.spill_handler import SpillHandler
from src.coalesce_handler import CoalesceHandler
from src.live_range_splitter import LiveRangeSplitter
from src.utils import visualize_allocation
from main import RegisterAllocator

# =========================
# Tests for InterferenceGraph
# =========================

def test_add_variable():
    graph = InterferenceGraph()
    graph.add_variable("x", 0, 10)
    assert "x" in graph.variables
    assert graph.variables["x"].start_point == 0
    assert graph.variables["x"].end_point == 10

def test_add_interference():
    graph = InterferenceGraph()
    graph.add_variable("x", 0, 10)
    graph.add_variable("y", 5, 15)
    graph.add_interference("x", "y")
    assert "y" in graph.variables["x"].interferences
    assert "x" in graph.variables["y"].interferences

def test_build_from_live_ranges():
    graph = InterferenceGraph()
    live_ranges = [("x", 0, 10), ("y", 5, 15), ("z", 12, 20)]
    graph.build_from_live_ranges(live_ranges)
    assert "x" in graph.variables
    assert "y" in graph.variables
    assert "z" in graph.variables
    assert "y" in graph.variables["x"].interferences
    assert "x" in graph.variables["y"].interferences
    assert "z" in graph.variables["y"].interferences

# =========================
# Tests for GraphColoring
# =========================

def test_color_graph_success():
    graph = InterferenceGraph()
    graph.add_variable("x", 0, 10)
    graph.add_variable("y", 5, 15)
    graph.add_interference("x", "y")
    coloring = GraphColoring(graph, 2)
    success, spill_candidates = coloring.color_graph()
    assert success
    assert not spill_candidates
    assert coloring.colors["x"] != coloring.colors["y"]

def test_color_graph_with_spill():
    graph = InterferenceGraph()
    # Add more variables than registers
    live_ranges = [("a", 0, 10), ("b", 5, 15), ("c", 10, 20), ("d", 15, 25)]
    graph.build_from_live_ranges(live_ranges)
    coloring = GraphColoring(graph, 2)
    success, spill_candidates = coloring.color_graph()
    assert success
    assert spill_candidates

# =========================
# Tests for SpillHandler
# =========================

def test_handle_spills():
    graph = InterferenceGraph()
    live_ranges = [("a", 0, 10), ("b", 5, 15)]
    graph.build_from_live_ranges(live_ranges)
    spill_handler = SpillHandler(graph)
    spill_handler.handle_spills({"a"})
    assert graph.variables["a"].spilled
    assert "b" not in graph.variables["a"].interferences
    assert "a" not in graph.variables["b"].interferences

# =========================
# Tests for CoalesceHandler
# =========================

def test_can_coalesce():
    graph = InterferenceGraph()
    graph.add_variable("a", 0, 10)
    graph.add_variable("b", 5, 15)
    coalesce_handler = CoalesceHandler(graph)
    assert not coalesce_handler.can_coalesce("a", "b")

def test_coalesce_variables():
    graph = InterferenceGraph()
    graph.add_variable("a", 0, 10)
    graph.add_variable("b", 11, 20)
    coalesce_handler = CoalesceHandler(graph)
    assert coalesce_handler.coalesce_variables("a", "b")
    assert "b" not in graph.variables
    assert graph.variables["a"].end_point == 20

# =========================
# Tests for LiveRangeSplitter
# =========================

def test_split_range_success():
    graph = InterferenceGraph()
    graph.add_variable("x", 0, 20)
    splitter = LiveRangeSplitter(graph)
    new_var_name, success = splitter.split_range("x", 15)
    assert success
    assert new_var_name == "x_split_15"
    assert graph.variables["x"].end_point == 15
    assert graph.variables[new_var_name].start_point == 15
    assert graph.variables[new_var_name].end_point == 20

def test_split_range_fail():
    graph = InterferenceGraph()
    graph.add_variable("x", 0, 10)
    splitter = LiveRangeSplitter(graph)
    new_var_name, success = splitter.split_range("x", 5)  # within range, should succeed
    assert success

# =========================
# Tests for RegisterAllocator
# =========================

def test_register_allocator_allocate_registers():
    allocator = RegisterAllocator(2)
    live_ranges = [("x", 0, 10), ("y", 5, 15), ("z", 12, 20)]
    allocator.initialize(live_ranges)
    allocation = allocator.allocate_registers()
    assert allocation["x"] != allocation["y"]
    assert allocation["y"] != allocation["z"]
    assert allocation["x"] != allocation["z"]

# =========================
# Tests for visualize_allocation utility
# =========================

def test_visualize_allocation(capsys):
    allocation = {"x": 0, "y": 1, "z": "spilled"}
    visualize_allocation(allocation, 2)
    captured = capsys.readouterr()
    assert "Register 0: x" in captured.out
    assert "Register 1: y" in captured.out
    assert "Spilled Variables: z" in captured.out
