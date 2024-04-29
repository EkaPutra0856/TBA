import graphviz

def visualize_nfa (data):
    # Membuat objek Graphviz dengan orientasi horizontal
    dot = graphviz.Digraph()
    

    # Menambahkan node
    for state in data["states"]:
        if state in data["final_states"]:
            dot.node(state, shape='doublecircle')
        else:
            dot.node(state)
    dot.node("start", label="start", shape="none", fontsize="24")
    dot.edge("start", data["start_states"][0])
    # Menambahkan edge
    for transition in data["transition_matrix"]:
        dot.edge(transition[0], transition[2], label=transition[1])

    dot.graph_attr['bgcolor'] = '#e5e7eb'
    # Menyimpan dan menampilkan graf
    dot.render('static/img/regex', format='png' , cleanup=True, view=False)  # Tidak perlu format karena sudah diatur di awal