const dfa = {'q1': {'d': 'q1', 'c': 'q2'}, 'q2': {'d': 'q2', 'c': 'q1'}};
const startState = 'q1';
const acceptingStates = ['q1'];
export { dfa, startState, acceptingStates };