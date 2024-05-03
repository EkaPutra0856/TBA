const enfa = {'q0': {'0': ['q0'], '': ['q1']}, 'q1': {'1': ['q2'], '': ['q2']}, 'q2': {'': ['q2', 'q3']}, 'q3': {}};
const startStateENFA = "q0";
const acceptingStatesENFA = ['q2'];
export { enfa, startStateENFA, acceptingStatesENFA };