
from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import logging
import json

import graphviz
from graphviz import Digraph
import re
from static.py.convertENFA import convertToNFA, remove_slashes
from static.py.visualize import visualize_enfa

from static.py.no3 import DFA

from static.py.no2 import NFAState, regexToNFA, printTransitionTable, visualizeNFA
from static.py.no4 import equivalent, visualize_dfa


# from static.py.no5 import test_regex


app = Flask(__name__)


@app.route('/edit_dfa')
def editdfa():
    return render_template('edit_dfa.html')

# Endpoint untuk menampilkan nilai DFA
@app.route('/get_dfa', methods=['GET'])
def get_dfa():
    try:
        # Baca nilai-nilai saat ini dari file dfa.js
        with open('static/js/no5/dfa.js', 'r') as f:
            current_data = f.read()
        
        # Ubah data saat ini menjadi objek JSON
        current_values = json.loads(current_data.strip().strip(';'))
        
        return jsonify(current_values), 200
    except Exception as e:
        return str(e), 500

# Endpoint untuk memperbarui nilai DFA
@app.route('/update_dfa', methods=['POST'])
def update_dfa():
    try:
        # Ambil data JSON dari permintaan POST
        data = request.form
        dfa = eval(request.form.get('dfa'))
        logging.debug(f"dfa: {dfa}")
        start_state = data.get('startState')
        logging.debug(f"dfa: {start_state}")
        accepting_states = eval(data.get('acceptingStates'))
        logging.debug(f"dfa: {accepting_states}")

        # # Cek apakah start state dan accepting states ada dalam transition state
        # all_states = set(dfa.keys())  # Ambil semua state dalam DFA
        # all_transitions = {state for transitions in dfa.values() for state in transitions.values()}  # Ambil semua transition state
        # if start_state not in all_states or start_state not in all_transitions or not all_transitions:
        #     error_message = "Start state tidak ada dalam transition state yang disebutkan."
        #     return render_template('index5.html', error=error_message)
        # for state in accepting_states:
        #     if state not in all_states or state not in all_transitions:
        #         error_message = "Accepting state tidak ada dalam transition state yang disebutkan."
        #         return render_template('index5.html', error=error_message)

        # Tulis nilai-nilai yang diperbarui ke dalam file dfa.js
        with open('static/js/no5/dfa.js', 'w') as f:
            f.write('const dfa = ' + str(dfa) + ';\n')  # Ubah objek kamus menjadi string sebelum menggabungkannya
            f.write('const startState = \'' + start_state + '\';\n')
            f.write('const acceptingStates = ' + str(accepting_states) + ';\n')  # Ubah objek daftar menjadi string sebelum menggabungkannya
            f.write('export { dfa, startState, acceptingStates };')

        dot = graphviz.Digraph()
        dot.attr(rankdir='LR')

        for state in dfa.keys():
            if state in accepting_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)

        # Tambahkan node "Start" dan edge ke start state
        dot.node('Start', shape='none', label='Start', width='0', height='0')
        dot.edge('Start', start_state, arrowhead='normal')

        # Add edges
        for state, transitions in dfa.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)

        dot.render("static/img/dfa", format='png', cleanup=True)

        return render_template('index5.html')
    except Exception as e:
        error_message = "Masukkan input sesuai template."
        return render_template('index5.html', error=error_message)

@app.route('/edit_nfa')
def edit_nfa():
    return render_template('edit_nfa.html')

# Endpoint untuk menampilkan nilai NFA
@app.route('/get_nfa', methods=['GET'])
def get_nfa():
    try:
        # Baca nilai-nilai saat ini dari file nfa.js
        with open('static/js/no5/nfa.js', 'r') as f:
            current_data = f.read()
        
        # Ubah data saat ini menjadi objek JSON
        current_values = json.loads(current_data.strip().strip(';'))
        
        return jsonify(current_values), 200
    except Exception as e:
        return str(e), 500

# Endpoint untuk memperbarui nilai NFA
@app.route('/update_nfa', methods=['POST'])
def update_nfa():
    try:
        # Ambil data JSON dari permintaan POST
        data = request.form
        nfa = eval(request.form.get('nfa'))
        logging.debug(f"nfa: {nfa}")
        start_state = data.get('startStates')
        logging.debug(f"start states: {start_state}")
        accepting_states = eval(data.get('acceptingStates'))
        logging.debug(f"accepting states: {accepting_states}")
    
        # Tulis nilai-nilai yang diperbarui ke dalam file nfa.js
        with open('static/js/no5/nfa.js', 'w') as f:
            f.write('const nfa = ' + str(nfa) + ';\n')  # Ubah objek kamus menjadi string sebelum menggabungkannya
            f.write('const startStateNFA = ' + str(start_state) + ';\n')
            f.write('const acceptingStatesNFA = ' + str(accepting_states) + ';\n')  # Ubah objek daftar menjadi string sebelum menggabungkannya
            f.write('export { nfa, startStateNFA, acceptingStatesNFA };')
        
        dot = graphviz.Digraph()
        dot.attr(rankdir='LR') 
        
        # Add nodes
        for state in nfa.keys():
            if state in start_state:
                dot.node(state, shape='circle', xlabel='Start')
            elif state in accepting_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        
        # Add edges
        for state, transitions in nfa.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)
        
        dot.render("static/img/nfa", format='png', cleanup=True)

        return render_template('index5.html')
    except Exception as e:
        error_message = "Masukkan input sesuai template."
        return render_template('index5.html', error=error_message)


@app.route('/edit_enfa')
def edit_enfa():
    return render_template('edit_enfa.html')

# Endpoint untuk menampilkan nilai ENFA
@app.route('/get_enfa', methods=['GET'])
def get_enfa():
    try:
        # Baca nilai-nilai saat ini dari file nfa.js
        with open('static/js/no5/enfa.js', 'r') as f:
            current_data = f.read()
        
        # Ubah data saat ini menjadi objek JSON
        current_values = json.loads(current_data.strip().strip(';'))
        
        return jsonify(current_values), 200
    except Exception as e:
        return str(e), 500
    
@app.route('/update_enfa', methods=['POST'])
def update_enfa():
    try:
        current_data = ''  # Inisialisasi current_data sebelum digunakan

        # Ambil data JSON dari permintaan POST
        data = request.form
        enfa = eval(request.form.get('enfa'))
        logging.debug(f"enfa: {enfa}")
        start_state = data.get('startStates')
        logging.debug(f"start states: {start_state}")
        accepting_states = eval(data.get('acceptingStates'))
        logging.debug(f"accepting states: {accepting_states}")

        # Baca nilai-nilai saat ini dari file enfa.js
        with open('static/js/no5/enfa.js', 'r') as f:
            current_data = f.read()

        # Ubah nilai-nilai ENFA dalam current_data tanpa mengubah ε
        current_data = re.sub(r"enfa\s*:\s*{([^}]*)}", r"enfa: {\1}".replace("0", "'0'").replace("1", "'1'"), current_data)
        current_data = current_data.replace("' '", "'ε'")  # Mengganti karakter kosong dengan simbol epsilon

        # Saat menyimpan nilai-nilai ENFA dalam file enfa.js
        with open('static/js/no5/enfa.js', 'w') as f:
            f.write('const enfa = ' + str(enfa).replace("'ε'", "''") + ';\n')
            f.write('const startStateENFA = ' + str(start_state) + ';\n')
            f.write('const acceptingStatesENFA = ' + str(accepting_states) + ';\n')  
            f.write('export { enfa, startStateENFA, acceptingStatesENFA };')
        
            dot = graphviz.Digraph()
            dot.attr(rankdir='LR')  # Atur tata letak dari kiri ke kanan (left to right)


        # Add nodes
        for state in enfa.keys():
            if state in start_state:
                dot.node(state, shape='circle', xlabel='Start')
            elif state in accepting_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        
        # Add edges
        for state, transitions in enfa.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    if symbol == "":
                         symbol = "ε"  # Ganti simbol kosong dengan epsilon
                    dot.edge(state, next_state, label=symbol)
      
        dot.render("static/img/enfa", format='png', cleanup=True)

        return render_template('index5.html')
    except Exception as e:
        error_message = "Masukkan input sesuai template."
        return render_template('index5.html', error=error_message)

    


# Render the page for editing the regular expression
@app.route('/edit_regex')
def edit_regex():
    return render_template('edit_regex.html')

# Rute untuk memperbarui nilai regexPattern
@app.route('/update_regex_pattern', methods=['POST'])
def update_regex_pattern():
    try:
        newPattern = request.form.get('regexPattern')
        newPattern = newPattern.replace('+', '|')
        logging.debug(f"Regex : {newPattern}")
        with open('static/js/no5/regex.js', 'w') as f:
            f.write(f"const regexPattern = '{newPattern}';\nexport {{ regexPattern }};")
        
        newPattern = remove_slashes(newPattern)
        enfa = convertToNFA(newPattern)
        
        visualize_enfa(enfa)
        
        # test_regex(newPattern, string)

        return render_template('index5.html')
    
    except Exception as e:
        return str(e), 500

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/menu0')
def menu0():
    return render_template('index.html')  
@app.route('/menu1')
def menu1():
    return render_template('index1.html')

@app.route('/menu2')
def menu2():
    return render_template('index2.html')

@app.route('/menu3')
def menu3():
    return render_template('index3.html')

@app.route('/menu4')
def menu4():
    return render_template('index4.html')

@app.route('/menu5')
def menu5():
    return render_template('index5.html')

@app.route('/menu2', methods=['GET', 'POST'])
def no2():
    if request.method == 'POST':
        regex = request.form['regex']
        input_string = request.form['input_string']

        nfa = regexToNFA(regex)
        transition_table = printTransitionTable(nfa)
        nfa_image = visualizeNFA(nfa)

        if nfa.test(input_string):
            accepted = True
        else:
            accepted = False

        return render_template('index2.html', result=True, accepted=accepted, transition_table=transition_table, nfa_image=nfa_image)

    return render_template('index2.html', result=None, transition_table=None)

@app.route('/menu3', methods=['GET', 'POST'])
def no3():
    if request.method == 'POST':
        states = set(request.form['states'].split(','))
        alphabet = set(request.form['alphabet'].split(','))
        transition_function = {}
        transition_lines = request.form['transition_function'].replace('\r', '').split('\n')
        for line in transition_lines:
            if line:
                state_symbol, next_state = line.split('->')
                state, symbol = state_symbol.split(',')
                transition_function[(state, symbol)] = next_state
        start_state = request.form['start_state']
        accept_states = set(request.form['accept_states'].split(','))

        dfa = DFA(states, alphabet, transition_function, start_state, accept_states)

        file_before = dfa.display_graph(before_minimization=True)
        dfa.minimize()
        file_after = dfa.display_graph(before_minimization=False)

        return render_template('result3.html', file_before=file_before, file_after=file_after)

    return render_template('index3.html')

if __name__ == '__main__':
    NFAState.reset_state_count()
    app.run(debug=True)

