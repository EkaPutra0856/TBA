const enfa = {
  q0: { '0': ['q0', 'q1'], 'e': ['q1'] },
  q1: { '1': ['q2'], 'e': ['q2'] },
  q2: { 'e': ['q2', 'q3'] },
  q3: { 'e': [] }
};

const startStateENFA = 'q0'; // Menambahkan start state
const acceptingStatesENFA = ['q2']; // Menambahkan accepting state(s)

export { enfa, startStateENFA, acceptingStatesENFA };
