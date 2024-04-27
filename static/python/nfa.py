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
                nfa_transitions = json.loads(object_literal)
                return nfa_transitions
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON object for variable '{variable_name}': {e}")
    raise ValueError(f"Variable '{variable_name}' not found in JavaScript code.")

def find_accepting_states(nfa_transitions, accepting_states):
    accepting_states_set = set(accepting_states)
    filtered_states = {}
    for state, transitions in nfa_transitions.items():
        if state in accepting_states_set:
            filtered_states[state] = transitions
    return filtered_states

def find_start_state(start_state):
    return start_state  # Mengambil start state dari objek NFA

def read_js_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def get_nfa():
    nfa_js_code = read_js_file('nfa.js')
    try:
        nfa_value = extract_variable_value(nfa_js_code, 'nfa')
        start_state_nfa = extract_variable_value(nfa_js_code, 'startStateNFA')
        accepting_states_nfa = extract_variable_value(nfa_js_code, 'acceptingStatesNFA')
        accepting_states_nfa = accepting_states_nfa if isinstance(accepting_states_nfa, list) else [accepting_states_nfa]
        nfa_value['_accepting_states'] = find_accepting_states(nfa_value, accepting_states_nfa)
        nfa_value['_start_state'] = find_start_state(start_state_nfa)
        return nfa_value
    except ValueError as e:
        print("Error extracting NFA transitions:", e)
        return None

if __name__ == "__main__":
    nfa = get_nfa()
    if nfa:
        print("NFA transitions:")
        print(nfa)
        print("Accepting states:")
        print(nfa['_accepting_states'])
        print("Start state:")
        print(nfa['_start_state'])
