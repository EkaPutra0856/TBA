const dfa = {'q0': {'0': 'q1', '1': 'q2'}, 'q1': {'0': 'q1', '1': 'q2'}, 'q2': {'0': 'q3', '1': 'q2'}, 'q3': {'0': 'q3', '1': 'q3'}};
const startState = 'q1';
const acceptingStates = ['q2'];
export { dfa, startState, acceptingStates };