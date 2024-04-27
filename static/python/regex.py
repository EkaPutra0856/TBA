import re
from graphviz import Digraph

def generate_regex_image(regex_pattern, filename):
    dot = Digraph()

    # Add nodes and edges for the regex pattern
    dot.node('Start', shape='none')  # Add start node
    dot.node('End', shape='doublecircle')  # Add end (accepting) node
    dot.edge('Start', 'End', label=regex_pattern)  # Add edge from start to end with regex pattern as label

    # Render and save the graph
    dot.render(filename, format='png', cleanup=True)
