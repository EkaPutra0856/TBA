
from flask import Flask, render_template, jsonify, request, redirect, url_for
import logging
import json
import sys
import os
import graphviz



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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Aktifkan logging debug
    app.run(debug=True)