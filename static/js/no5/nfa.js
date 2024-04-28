const nfa = {'q0': {'1': ['q0', 'q1']}, 'q1': {'0': ['q2'], '1': ['q1']}, 'q2': {'1': ['q3']}, 'q3': {'0': ['q3']}};
const startStateNFA = "q1";
const acceptingStatesNFA = ['q2'];
export { nfa, startStateNFA, acceptingStatesNFA };