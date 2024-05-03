const enfa = {'q0': {'': ['q1', 'q2', 'q4']}, 'q1': {'0': ['q3']}, 'q2': {'1': ['q3']}, 'q3': {'1': ['q4']}, 'q4': {}};
const startStateENFA = "q0";
const acceptingStatesENFA = ['q4'];
export { enfa, startStateENFA, acceptingStatesENFA };