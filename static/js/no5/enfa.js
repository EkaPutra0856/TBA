const enfa = {
  q0: { '0': ['q0', 'q1'], 'ε': ['q1'] },
  q1: { '1': ['q2'], 'ε': ['q2'] },
  q2: { 'ε': ['q2', 'q3'] },
  q3: { 'ε': [] }
};

const startStateENFA = 'q0'; // Menambahkan start state
const acceptingStatesENFA = ['q2']; // Menambahkan accepting state(s)

export { enfa, startStateENFA, acceptingStatesENFA };
