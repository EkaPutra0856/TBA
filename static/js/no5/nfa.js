// nfa.js

const nfa = {
  q0: { '1': ['q0', 'q1'] },
  q1: { '0': ['q2'], '1': ['q1'] },
  q2: { '1': ['q3'] },
  q3: { '0': ['q3'] }
};

const startStateNFA = 'q0'; // Menambahkan start state
const acceptingStatesNFA = ['q2']; // Menambahkan accepting state(s)

export { nfa, startStateNFA, acceptingStatesNFA };
