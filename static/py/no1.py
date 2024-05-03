from graphviz import Digraph

def visualize_DFA(DFA, filename):
    dot = Digraph(comment='DFA', format='png')
    dot.attr(rankdir='LR')

    for state in DFA['states']:
        if state in DFA['final_states']:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)

    for start_state, transitions in DFA['transitions'].items():
        for symbol, next_state in transitions.items():
            dot.edge(start_state, next_state, label=symbol)

    dot.attr('node', shape='none', label='start')
    dot.node('')
    dot.edge('', DFA['initial_state'])

    dot.render(filename, cleanup=True)

def get_next_state(current_state, symbol, transitions):
    return transitions.get(current_state, {}).get(symbol)

def are_states_equivalent(state1, state2, DFA1, DFA2, equivalent_table):
    return equivalent_table[state1][state2]

def equivalent(DFA1, DFA2):
    def initialize_equivalence_table(DFA1, DFA2):
        equivalent_table = {}
        for state1 in DFA1['states']:
            equivalent_table[state1] = {}
            for state2 in DFA2['states']:
                equivalent_table[state1][state2] = (state1 in DFA1['final_states']) == (state2 in DFA2['final_states'])
        return equivalent_table

    equivalent_table = initialize_equivalence_table(DFA1, DFA2)

    if not equivalent_table[DFA1['initial_state']][DFA2['initial_state']]:
        return False

    for state1 in DFA1['states']:
        for state2 in DFA2['states']:
            for symbol in DFA1['input_symbols']:
                next_state1 = get_next_state(state1, symbol, DFA1['transitions'])
                next_state2 = get_next_state(state2, symbol, DFA2['transitions'])
                if (next_state1 is None and next_state2 is not None) or (next_state1 is not None and next_state2 is None):
                    equivalent_table[state1][state2] = False

    while True:
        changed = False
        for state1 in DFA1['states']:
            for state2 in DFA2['states']:
                if not equivalent_table[state1][state2]:
                    continue
                for symbol in DFA1['input_symbols']:
                    next_state1 = get_next_state(state1, symbol, DFA1['transitions'])
                    next_state2 = get_next_state(state2, symbol, DFA2['transitions'])
                    if not are_states_equivalent(next_state1, next_state2, DFA1, DFA2, equivalent_table):
                        equivalent_table[state1][state2] = False
                        changed = True
                        break
            if changed:
                break
        if not changed:
            break

    for state1 in DFA1['states']:
        for state2 in DFA2['states']:
            if are_states_equivalent(state1, state2, DFA1, DFA2, equivalent_table):
                for symbol in DFA1['input_symbols']:
                    next_state1 = get_next_state(state1, symbol, DFA1['transitions'])
                    next_state2 = get_next_state(state2, symbol, DFA2['transitions'])
                    if not are_states_equivalent(next_state1, next_state2, DFA1, DFA2, equivalent_table):
                        return False
            else:
                if state1 in DFA1['final_states'] != state2 in DFA2['final_states']:
                    return False
    return True


DFA1 = {}
DFA1['states'] = input("Enter states for DFA 1 (seperate with a space): ").split()
DFA1['initial_state'] = input("Initial state: ")
DFA1['final_states'] = input("Final state (seperate with a space > 1): ").split()
DFA1['input_symbols'] = input("Enter input symbol for DFA 1 (seperate with a space): ").split()
DFA1['transitions'] = {}
for state in DFA1['states']:
    DFA1['transitions'][state] = {}
    for symbol in DFA1['input_symbols']:
        next_state = input(f"Transition from state {state} with symbol {symbol}: ")
        DFA1['transitions'][state][symbol] = next_state

DFA2 = {}
DFA2['states'] = input("Enter states for DFA 2 (seperate with a space): ").split()
DFA2['initial_state'] = input("Initial state: ")
DFA2['final_states'] = input("Final state (seperate with a space > 1): ").split()
DFA2['input_symbols'] = input("Enter input symbol for DFA 2 (seperate with a space): ").split()
DFA2['transitions'] = {}
for state in DFA2['states']:
    DFA2['transitions'][state] = {}
    for symbol in DFA2['input_symbols']:
        next_state = input(f"Transition from state {state} with symbol {symbol}: ")
        DFA2['transitions'][state][symbol] = next_state

    # Function for graphic
    visualize_DFA(DFA1.states, DFA1.input_symbols, DFA1.transitions, DFA1.initial_state, DFA1.final_states, 'DFA1')
    visualize_DFA(DFA2.states, DFA2.input_symbols, DFA2.transitions, DFA2.initial_state, DFA2.final_states, 'DFA2')    
    

if equivalent(DFA1, DFA2):
    print("Both DFA Are Equivalent!")
else:
    print("Both DFA Are Not Equivalent!")