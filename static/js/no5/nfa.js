const nfa = {'q0': {'a': ['q0', 'q1'], 'b': ['q0']}, 'q1': {'b': ['q2']}, 'q2': {}};
const startStateNFA = "q0";
const acceptingStatesNFA = ['q2'];
export { nfa, startStateNFA, acceptingStatesNFA };