class UserInput {
    constructor(startState, finalStates, states, alphabet, transitions) {
        this.startState = startState;
        this.finalStates = finalStates;
        this.states = states;
        this.alphabet = alphabet;
        this.transitions = transitions;
    }
}

$(document).ready(() => {
    $("#new-transition").click(() => {
        $("#nfa-transitions .production-row").last().clone(true).appendTo("#nfa-transitions");
    });

    $("#resetBtn").click(() => {
        $("#startStateInput, #finalStatesInput").val('');
        $("#nfa-transitions .production-row:not(:first-child)").remove(); // Hapus semua baris form transisi kecuali satu
        $("#nfa-transitions input").val('');
        $("#current-nfa, #current-dfa, #current-dfa-minimized").empty();
    });
    

    $(document).on('keypress', '.production-row input', function (e) {
        if (e.which === 13) $("#new-transition").click();
    });

    $(document).on('keyup', '.production-row input', function (e) {
        if (e.which !== 13) $("#verify-update-debug").click();
    });

    $(document).on('keyup', '#startStateInput, #finalStatesInput', function (e) {
        $("#verify-update-debug").click();
    });

    $("#verify-update-debug").click(() => {
        let user_input = fetchUserInput();
        if (!user_input) return;
        let dotStr = "digraph fsm {\n";
        dotStr += "rankdir=LR;\n";
        dotStr += "size=\"8,5\";\n";
        dotStr += "node [shape = doublecircle]; " + user_input.finalStates + ";\n";
        dotStr += "node [shape = point]; START_STATE\n";
        dotStr += "node [shape = circle];\n";
        dotStr += "START_STATE -> " + user_input.startState + ";\n";
        for (let transition of user_input.transitions)
            dotStr += `${transition.state} -> ${transition.nextStates} [label="${transition.symbol}"];\n`;
        dotStr += "}";
        console.log(dotStr);
        d3.select("#current-nfa").graphviz().zoom(false).renderDot(dotStr);
        let dfa = generateDFA(new NFA(user_input.startState, user_input.finalStates, user_input.states, user_input.alphabet, user_input.transitions));

        dotStr = dfa.toDotString();
        console.log(dotStr);
        d3.select("#current-dfa").graphviz().zoom(false).renderDot(dotStr);
        dfa = minimizeDFA(dfa);
        dotStr = dfa.toDotString();
        console.log(dotStr);
        $("#current-dfa-minimized").show();
        d3.select("#current-dfa-minimized").graphviz().zoom(false).renderDot(dotStr);
    });
    });

    function fetchUserInput() {
        let startState = $("#startStateInput").val().trim();
        let finalStates = $("#finalStatesInput").val().trim();
        let states = [];
        let alphabet = [];
        let transitions = [];
        if (startState.includes('{') || finalStates.includes('{')) {
            alert('State names cannot contain the "{" character!');
            return null;
        }

        $(".production-row").each(function () {
            let currentState = $(this).find(".current-state-input").val().trim();
            let inputSymbol = $(this).find(".input-symbol").val().trim();
            if (inputSymbol === '') {
                inputSymbol = '\u03B5'; 
            }
            let nextState = $(this).find(".next-states").val().trim();
            if (currentState.includes('{') || nextState.includes('{')) {
                alert('State names cannot contain the "{" character!');
                return;
            }
            transitions.push(new Transition(currentState, nextState, inputSymbol));
            if (inputSymbol !== '\u03B5' && !alphabet.includes(inputSymbol)) {
                alphabet.push(inputSymbol);
            }
            if (!states.includes(currentState)) {
                states.push(currentState);
            }
            if (!states.includes(nextState)) {
               states.push(nextState);
            }
        });
        if (finalStates.includes(",")) {
            finalStates = finalStates.split(",");
        }
        return new UserInput(startState, finalStates, states, alphabet, transitions);
    }
