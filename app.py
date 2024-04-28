
from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
import json
import sys
import os
import graphviz
import re



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

       
        # Tulis nilai-nilai yang diperbarui ke dalam file dfa.js
        with open('static/js/no5/dfa.js', 'w') as f:
            f.write('const dfa = ' + str(dfa) + ';\n')  # Ubah objek kamus menjadi string sebelum menggabungkannya
            f.write('const startState = \'' + start_state + '\';\n')
            f.write('const acceptingStates = ' + str(accepting_states) + ';\n')  # Ubah objek daftar menjadi string sebelum menggabungkannya
            f.write('export { dfa, startState, acceptingStates };')

    
        dot = graphviz.Digraph()
        
        # Add nodes
        for state in dfa.keys():
            if state == start_state:
                dot.node(state, shape='circle', xlabel='Start')
            elif state in accepting_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state)
        
        # Add edges
        for state, transitions in dfa.items():
            for symbol, next_state in transitions.items():
                dot.edge(state, next_state, label=symbol)
        
        dot.render("static/img/dfa", format='png', cleanup=True)


        return render_template('index.html')
    except Exception as e:
        return str(e), 500

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
        start_states = data.get('startStates')
        logging.debug(f"start states: {start_states}")
        accepting_states = eval(data.get('acceptingStates'))
        logging.debug(f"accepting states: {accepting_states}")

        # Tulis nilai-nilai yang diperbarui ke dalam file nfa.js
        with open('static/js/no5/nfa.js', 'w') as f:
            f.write('const nfa = ' + str(nfa) + ';\n')  # Ubah objek kamus menjadi string sebelum menggabungkannya
            f.write('const startStateNFA = ' + str(start_states) + ';\n')
            f.write('const acceptingStatesNFA = ' + str(accepting_states) + ';\n')  # Ubah objek daftar menjadi string sebelum menggabungkannya
            f.write('export { nfa, startStateNFA, acceptingStatesNFA };')
        
        dot = graphviz.Digraph()
        
        # Add nodes
        for state in nfa.keys():
            if state in start_states:
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

        return render_template('index.html')
    except Exception as e:
        return str(e), 500


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
        start_states = data.get('startStates')
        logging.debug(f"start states: {start_states}")
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
            f.write('const startStateENFA = ' + str(start_states) + ';\n')
            f.write('const acceptingStatesENFA = ' + str(accepting_states) + ';\n')  
            f.write('export { enfa, startStateENFA, acceptingStatesENFA };')
        
        dot = graphviz.Digraph()


        # Add nodes
        for state in enfa.keys():
            if state in start_states:
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

        return render_template('index.html')
    except Exception as e:
        return str(e), 500


# Regular expression pattern
regex_pattern = ""

# Render the page for editing the regular expression
@app.route('/edit_regex')
def edit_regex():
    return render_template('edit_regex.html', regex_pattern=regex_pattern)

# Rute untuk menampilkan nilai regexPattern saat ini
@app.route('/get_regex_pattern', methods=['GET'])
def get_regex_pattern():
    global regexPattern
    return {"regexPattern": regexPattern}, 200

# Rute untuk memperbarui nilai regexPattern
@app.route('/update_regex_pattern', methods=['POST'])
def update_regex_pattern():
    global regexPattern
    newPattern = request.json.get('regexPattern')
    regexPattern = newPattern
    return "Regex pattern updated successfully", 200

@app.route('/clear_and_rewrite_regex_js', methods=['POST'])
def clear_and_rewrite_regex_js():
    newPattern = request.json.get('regexPattern')
    with open('static/js/regex.js', 'w') as f:
        f.write(f"const regexPattern = {newPattern};\nexport {{ regexPattern }};")
    return "Regex.js file cleared and rewritten successfully", 200

if __name__ == "__main__":
    app.run(debug=True)