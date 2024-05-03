from collections import defaultdict
import os
import subprocess

class DFA:
    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = accept_states

    def is_accepting(self, state):
        return state in self.accept_states

    def transition(self, state, symbol):
        return self.transition_function.get((state, symbol))

    def test_string(self, input_string, display_prefix=False):
        current_state = self.start_state
        prefix_accepted = []  # Prefiks yang diterima
        for i, symbol in enumerate(input_string, 1):
            if symbol not in self.alphabet:
                return False, prefix_accepted  # Simbol tidak valid
            current_state = self.transition(current_state, symbol)
            if current_state is None:
                return False, prefix_accepted  # Transisi tidak valid
            if self.is_accepting(current_state):
                prefix_accepted.append(input_string[:i])
        return self.is_accepting(current_state), prefix_accepted

    def minimize(self):
        # Implementasi algoritma minimisasi DFA
        partition = [self.accept_states, self.states - self.accept_states]
        changed = True
        while changed:
            changed = False
            new_partition = []
            for part in partition:
                split_dict = defaultdict(list)
                for state in part:
                    transition_key = tuple(self.transition(state, symbol) for symbol in self.alphabet)
                    split_dict[transition_key].append(state)
                if len(split_dict) > 1:
                    changed = True
                    new_partition.extend(split_dict.values())
                else:
                    new_partition.append(part)
            partition = new_partition

        state_map = {}
        minimized_states = set()
        minimized_accept_states = set()
        minimized_transition_function = {}

        for part in partition:
            representative = next(iter(part))
            minimized_states.add(representative)
            if representative in self.accept_states:
                minimized_accept_states.add(representative)
            for state in part:
                state_map[state] = representative

        for (state, symbol), next_state in self.transition_function.items():
            new_state = state_map[state]
            new_next_state = state_map[next_state]
            minimized_transition_function[(new_state, symbol)] = new_next_state

        self.states = minimized_states
        self.transition_function = minimized_transition_function
        self.accept_states = minimized_accept_states
        self.start_state = state_map[self.start_state]

    def to_graphviz(self, file_path, before_minimization=True):
        dot_representation = "digraph {\n"
        dot_representation += "    graph [rankdir=LR]\n"
        dot_representation += "    node [shape=circle]\n"

        for state in self.states:
            if state in self.accept_states:
                dot_representation += f"    {state} [shape=doublecircle]\n"

        for (state, symbol), next_state in self.transition_function.items():
            dot_representation += f"    {state} -> {next_state} [label={symbol}]\n"

        dot_representation += f'    start [label="Start" shape=none]\n'
        dot_representation += f'    start -> {self.start_state}\n'

        dot_representation += "}\n"

        file_name = "before" if before_minimization else "after"
        with open(file_path + f"_{file_name}_minimization.dot", "w") as file:
            file.write(dot_representation)


    def display_graph(self, before_minimization=True):
        dot_representation = "digraph {\n"
        dot_representation += "    graph [rankdir=LR]\n"
        dot_representation += "    node [shape=circle]\n"

        for state in self.states:
            if state in self.accept_states:
                dot_representation += f"    {state} [shape=doublecircle]\n"

        for (state, symbol), next_state in self.transition_function.items():
            dot_representation += f'    {state} -> {next_state} [label="{symbol}"]\n'

        dot_representation += f'    start [label="Start" shape=none]\n'
        dot_representation += f'    start -> {self.start_state}\n'

        dot_representation += "}\n"

        output_format = 'png'
        file_name = "before" if before_minimization else "after"
        output_file_path = os.path.join('static', f'dfa_{file_name}_minimization.{output_format}')

        with open(f'dfa_{file_name}_minimization.dot', 'w') as dot_file:
            dot_file.write(dot_representation)

        subprocess.run(['dot', '-T' + output_format, f'dfa_{file_name}_minimization.dot', '-o', output_file_path], check=True)

        return f'dfa_{file_name}_minimization.{output_format}'
