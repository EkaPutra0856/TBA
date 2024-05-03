def tranform_transition(transition):
    result = {}
    for i in range(0, len(transition), 3):
        start_state = transition[i].lower()
        alphabet = transition[i+1]
        next_state = transition[i+2].lower()
        key = (start_state,alphabet)
        result[key] = next_state
    return result

def get_states(transisi):
    states = set()
    for key in transisi.keys():
        states.add(key[0])
    return states

def get_start_and_final_states(states):
    if not states:
        return ''
    states_set = {state.lower() for state in states}
    return states_set

def get_alphabet(transition):
    alphabet = set(item for item in transition if item.isdigit() or item == 'e')
    return alphabet

def set_to_string(s):
    # Mengambil item dari set
    item = s.pop()
    # Mengonversi item menjadi string dan mengubahnya menjadi lowercase
    s_string = str(item).lower()
    return s_string

def change_format(input_list):
    output_list = []
    temp = []
    for item in input_list:
        if item == 'e':
            temp.append('e')
        else:
            temp.append(item.lower())
        if len(temp) == 3:
            output_list.append(temp)
            temp = []
    return output_list

def change_format_to_list(input_set):
    return [item.lower() for item in input_set]

def convert_data(data):
    result = []
    seen = set()
    for item in data:
        if item.startswith('Q') and item.lower() not in seen:
            result.append(item.lower())
            seen.add(item.lower())
    return result

def convert_transitions(transitions):
    # Buat dictionary baru untuk menyimpan hasil konversi
    converted_transitions = {}

    # Loop melalui setiap item dalam transitions
    for key, value in transitions.items():
        # Periksa apakah kunci sudah ada di converted_transitions
        if key in converted_transitions:
            # Jika sudah ada, tambahkan nilai baru ke set yang ada di dalamnya
            converted_transitions[key].add(value)
        else:
            # Jika belum ada, buat set baru dengan nilai tersebut
            converted_transitions[key] = {value}
    
    return converted_transitions

def change_transition_5(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        state, symbol = key
        if symbol != 'e':  # Hanya tambahkan ke kamus baru jika simbolnya bukan 'e'
            if (state, symbol) in new_dict:
                new_dict[(state, symbol)].append(value)
            else:
                new_dict[(state, symbol)] = [value]
    return new_dict


def change_epsilon_transitions_5(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        state, symbol = key
        if symbol == 'e':  # Jika simbolnya adalah 'e'
            if state in new_dict:
                new_dict[state].append(value)
            else:
                new_dict[state] = [value]
    return new_dict

def change_format_4(transitions):
    transformed = {}
    for (state, symbol), next_state in transitions.items():
        if state not in transformed:
            transformed[state] = {}
        transformed[state][symbol] = next_state
    return transformed
