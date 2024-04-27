import os
import enfa
from graphviz import Digraph

def generate_image(automaton, filename, start_state=None, accepting_states=None):
    dot = Digraph()

    # Add states reachable from start state
    visited_states = set()
    queue = [start_state]
    while queue:
        current_state = queue.pop(0)
        visited_states.add(current_state)
        dot.node(current_state)
        if current_state in automaton:
            transitions = automaton[current_state]
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    if next_state not in visited_states:
                        queue.append(next_state)

    # Add transitions
    for state, transitions in automaton.items():
        if state in visited_states:
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    if next_state in visited_states:
                        dot.edge(state, next_state, label=str(symbol))

    # Add start state
    dot.node(start_state, shape='circle', xlabel='Start')

    # Mark accepting states
    if accepting_states:
        for state in accepting_states:
            if state in visited_states:
                dot.node(state, shape='doublecircle')

    # Render and save the graph
    dot.render(filename, format='png', cleanup=True)


# Set the path for the img folder
current_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.join(current_dir, "img")

# Create the img folder if it doesn't exist
if not os.path.exists(img_folder):
    os.makedirs(img_folder)

# Generate and save images for ε-NFA
enfa_transitions, start_state, accepting_states = enfa.get_enfa()
if enfa_transitions:
    generate_image(enfa_transitions, os.path.join(img_folder, "enfa"), start_state, accepting_states)
