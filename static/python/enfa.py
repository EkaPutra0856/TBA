import re
import json

def extract_variable_value(js_code, variable_name):
    start_index = js_code.find(f'const {variable_name} = ')
    if start_index != -1:
        start_index += len(f'const {variable_name} = ')
        end_index = js_code.find(';', start_index)
        if end_index != -1:
            object_literal = js_code[start_index:end_index]
            # Modify the object literal to ensure property names and string values are enclosed in double quotes
            object_literal = object_literal.replace("'", '"')
            object_literal = re.sub(r'(\b\w+\b):', r'"\1":', object_literal)
            try:
                value = json.loads(object_literal)
                return value
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON object for variable '{variable_name}': {e}")
    raise ValueError(f"Variable '{variable_name}' not found in JavaScript code.")

def find_accepting_states(transitions):
    accepting_states = {}
    for state, state_transitions in transitions.items():
        accepting = True
        for symbol, next_states in state_transitions.items():
            if not isinstance(next_states, list):
                next_states = [next_states]
            if state not in next_states:
                accepting = False
                break
        if accepting:
            accepting_states[state] = state_transitions
    return accepting_states

def find_start_state(js_code, variable_name):
    start_index = js_code.find(f'const {variable_name} = ')
    if start_index != -1:
        start_index += len(f'const {variable_name} = ')
        end_index = js_code.find(';', start_index)
        if end_index != -1:
            object_literal = js_code[start_index:end_index]
            object_literal = object_literal.replace("'", '"')
            object_literal = re.sub(r'(\b\w+\b):', r'"\1":', object_literal)
            try:
                transitions = json.loads(object_literal)
                return variable_name
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON object for variable '{variable_name}': {e}")
    raise ValueError(f"Variable '{variable_name}' not found in JavaScript code.")

def read_js_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def get_enfa():
    enfa_js_code = read_js_file('enfa.js')
    try:
        enfa_value = extract_variable_value(enfa_js_code, 'enfa')
        start_state_enfa = extract_variable_value(enfa_js_code, 'startStateENFA')
        accepting_states_enfa = extract_variable_value(enfa_js_code, 'acceptingStatesENFA')
        return enfa_value, start_state_enfa, accepting_states_enfa
    except ValueError as e:
        print("Error extracting ε-NFA transitions:", e)
        return None, None, None

if __name__ == "__main__":
    enfa, start_state, accepting_states = get_enfa()
    if enfa:
        print("Start state:", start_state)
        print("Accepting states:", accepting_states)
        print("ε-NFA transitions:")
        print(enfa)
