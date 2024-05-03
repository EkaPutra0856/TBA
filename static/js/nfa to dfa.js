let LAST_COMPLETED_STEP_COUNT = 0;

class Transition {
    constructor(state, nextStates, symbol) {
        if (typeof state !== 'string')
            throw new Error("Expected a single state (string)");
        if (!Array.isArray(nextStates)) {
            console.warn("Expected nextStates in transition to be an array");
            nextStates = [String(nextStates)];
        }
        if (typeof symbol !== 'string')
            throw new Error("Expected a string symbol");
        this.state = state;
        this.nextStates = nextStates;
        this.symbol = symbol;
    }
}

class NFA {
    constructor(startState, finalStates, states, alphabet, transitions) {
        this.startState = startState;
        this.finalStates = Array.isArray(finalStates) ? finalStates : [String(finalStates)];
        this.states = states;
        this.alphabet = Array.isArray(alphabet) ? alphabet : [String(alphabet)];
        this.transitions = Array.isArray(transitions) ? transitions : [transitions];
    }

    toDotString() {
        let dotStr = "digraph fsm {\n";
        dotStr += "rankdir=LR;\n";
        dotStr += "size=\"8,5\";\n";
        dotStr += "node [shape = point]; START_STATE\n";
        dotStr += "node [shape = doublecircle]; " + this.finalStates.join(',') + ";\n";
        dotStr += "node [shape = circle];\n";
        dotStr += "START_STATE -> " + this.formatDotState(this.startState) + ";\n";
        for (let i = 0; i < this.transitions.length; i++) {
            let t = this.transitions[i];
            dotStr += "" + this.formatDotState(t.state) + " -> " + this.formatDotState(t.nextStates) + " [label=" + t.symbol + "];\n";
        }
        dotStr += "}";
        return dotStr;
    }
    formatDotState(state_str) {
        state_str = state_str.toString();
        if (isMultiState(state_str)) {
            state_str = state_str.substring(1, state_str.length - 1);
            state_str = state_str.replace(/,/g, '');
            return state_str;
        } else {
            return state_str;
        }
    }}

function epsilonClosureNFA(nfa) {
    let hasEpsilon = nfa.transitions.some(t => t.symbol === '' || t.symbol === '\u03B5');
    if (!hasEpsilon) return nfa;
    
    let nfa_closed_transitions = [];
    let nfa_closed_final_states = [];
    for (let i = 0; i < nfa.states.length; i++) {
        let state = nfa.states[i];
        let state_closure = fetch_E_Closure(state, nfa.transitions);
        console.debug("Epsilon-closure of " + state + ": " + state_closure);
        for (let j = 0; j < nfa.alphabet.length; j++) {
            let symbol = nfa.alphabet[j];
            let symbol_next_states = [];
            for (let k = 0; k < state_closure.length; k++) {
                let next_states = findNextStates(state_closure[k], symbol, nfa.transitions);
                if (next_states.length !== 0) {
                    for (let n = 0; n < next_states.length; n++) {
                        let closure = fetch_E_Closure(next_states[n], nfa.transitions);
                        for (let m = 0; m < closure.length; m++) {
                            let to_add = closure[m];
                            if (!symbol_next_states.includes(to_add))
                                symbol_next_states.push(to_add);
                        }
                    }
                }
            }
            symbol_next_states.sort();
            console.log("NFA Closure: " + state + " -> " + symbol + " = " + symbol_next_states + " (Length " + symbol_next_states.length + ")");
            nfa_closed_transitions.push(new Transition(state, symbol_next_states, symbol));
        }
    }
    nfa_closed_final_states.sort();
    let start_state_closure = fetch_E_Closure(nfa.startState, nfa.transitions);
    let init_closure_has_final_state = false;
    for (let final_state of nfa.finalStates) {
        if (start_state_closure.includes(final_state)) {
            init_closure_has_final_state = true;
            break;
        }
    }
    if (init_closure_has_final_state) {
        nfa.finalStates.push(nfa.startState);
    }
    nfa = new NFA(nfa.startState, nfa.finalStates, nfa.states, nfa.alphabet, nfa_closed_transitions);
    console.log("--- Epsilon NFA ---");
    console.log(nfa.toDotString());
    console.log("--___--");
    return nfa;
}

function fetch_E_Closure(state, transitions) {
    if (typeof state !== 'string') throw new Error("Expected a single state input as a string");
    if (!Array.isArray(transitions)) throw new Error("Expected transitions parameter to be an array");

    let e_closure = [state];

    for (let t of transitions) {
        if (t.symbol.trim() === '' || t.symbol.trim() === '\u03B5') {
            if (state === t.state) {
                for (let next of t.nextStates) {
                    if (!e_closure.includes(next)) {
                        e_closure.push(next);
                        e_closure.push(...fetch_E_Closure(next, transitions));
                    }
                }
            }
        }
    }
    return e_closure;
}

function generateDFA(nfa) {
    nfa = epsilonClosureNFA(nfa);
    let dfa_states = [];
    let dfa_final_states = [];
    let dfa_transitions = [];
    let stack = [];
    dfa_states.push(nfa.startState);
    stack.push(nfa.startState);
    while (stack.length > 0) {
        let state = stack.pop();
        console.log("Pop'd state: " + state);
        let states;
        if (isMultiState(state)) {
            states = separateStates(state);
        } else {
            states = [];
            states.push(state);
        }
        for (let i = 0; i < nfa.alphabet.length; i++) {
            let next_states_union = [];
            for (let j = 0; j < states.length; j++) {
                let ns = findNextStates(states[j], nfa.alphabet[i], nfa.transitions);
                for (let k = 0; k < ns.length; k++)
                    if (!next_states_union.includes(ns[k]))
                        next_states_union.push(ns[k]);
            }
            let combinedStatesUnion = combineStates(next_states_union);
            if (combinedStatesUnion != null) {
                console.log(state + ", " + nfa.alphabet[i] + " -> " + combinedStatesUnion);
                dfa_transitions.push(new Transition(state, combinedStatesUnion, nfa.alphabet[i]));
                if (!dfa_states.includes(combinedStatesUnion)) {
                    dfa_states.push(combinedStatesUnion);
                    stack.push(combinedStatesUnion);
                }
            } else {
                console.log("END state needed");
                if (!dfa_states.includes("END")) {
                    for (let n = 0; n < nfa.alphabet.length; n++)
                        dfa_transitions.push(new Transition("END", ["END"], nfa.alphabet[n]));
                    dfa_states.push("END");
                }
                dfa_transitions.push(new Transition(state, ["END"], nfa.alphabet[i]));
            }
        }
    }
    console.log("--- NFA Final States ---");
    console.log(nfa.finalStates);
    console.log("-----");
    for (let i = 0; i < dfa_states.length; i++) {
        let dfa_sep_states = separateStates(dfa_states[i]);
        for (let j = 0; j < nfa.finalStates.length; j++) {
            console.log("Does " + dfa_sep_states + " include " + nfa.finalStates[j] + "?");
            if (dfa_sep_states.includes(nfa.finalStates[j])) {
                dfa_final_states.push(nfa.formatDotState(dfa_states[i]));
                break;
            }
        }
    }
    return new NFA(nfa.startState, dfa_final_states, dfa_states, nfa.alphabet, dfa_transitions);
}

function findNextStates(state, symbol, transitions) {
    let next_states = [];
    for (let i = 0; i < transitions.length; i++) {
        let t = transitions[i];
        if (t.state === state && t.symbol === symbol) {
            for (let j = 0; j < t.nextStates.length; j++) {
                if (!next_states.includes(t.nextStates[j])) {
                    next_states.push(t.nextStates[j]);
                }
            }
        }
    }
    return next_states;
}

function isMultiState(state) {
    state = state.toString();
    return state.startsWith("{") && state.endsWith("}");
}

function separateStates(state) {
    if (isMultiState(state)) {
        return state.substring(1, state.length - 1).split(",");
    } else {
        return state;
    }
}

function combineStates(states) {
    if (!Array.isArray(states)) {
        throw new Error("Array expected for combineStates() function");
    }
    states = states.filter(function (e) {
        return e != null;
    });
    if (states.length > 0 && Array.isArray(states[0])) {
        console.warn("Sub-arrays are not expected for combineStates() function");
        states = states[0];
    }
    if (states.length === 0)
        return null;
    states.sort();
    if (states.length === 1)
        return states[0].toString();
    let state = "{";
    for (let i = 0; i < states.length; i++) {
        state += states[i] + ","
    }
    state = state.trim().replace(/,+$/, '');
    state += "}";
    return state;
}

function arraysEqual(a, b) {
    if (a === b) return true;
    if (a == null || b == null) return false;
    if (a.length !== b.length) return false;
    for (let i = 0; i < a.length; i++)
        if (a[i] !== b[i]) return false;
    return true;
}