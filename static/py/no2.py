from graphviz import Digraph

class Type:
    SYMBOL = 1
    CONCAT = 2
    UNION = 3
    KLEENE = 4

class ExpressionTree:
    def __init__(self, _type, value=None):
        self._type = _type
        self.value = value
        self.left = None
        self.right = None

def constructTree(regexp):
    stack = []
    for c in regexp:
        if c.isalnum():  # Alphanumeric characters are treated as symbols
            stack.append(ExpressionTree(Type.SYMBOL, c))
        else:
            z = None
            if c == "+":
                z = ExpressionTree(Type.CONCAT)
                z.right = ExpressionTree(Type.KLEENE)
                z.right.left = stack.pop()
                z.left = stack.pop()
            elif c == ".":
                z = ExpressionTree(Type.CONCAT)
                z.right = stack.pop()
                z.left = stack.pop()
            elif c == "*":
                z = ExpressionTree(Type.KLEENE)
                z.left = stack.pop()
            elif c == "|":
                z = ExpressionTree(Type.UNION)
                z.right = stack.pop()
                z.left = stack.pop()
            stack.append(z)

    return stack[0]

def postfix(regexp):
    temp = []
    for i in range(len(regexp)):
        if i != 0 and (regexp[i-1].isalnum() or regexp[i-1] == ")" or regexp[i-1] == "*") and (regexp[i].isalnum() or regexp[i] == "("):
            temp.append(".")
        temp.append(regexp[i])
    regexp = temp

    stack = []
    output = ""

    for c in regexp:
        if c.isalnum():  # Accept alphanumeric characters (a-z, A-Z, 0-9)
            output = output + c
            continue

        if c == ")":
            while len(stack) != 0 and stack[-1] != "(":
                output = output + stack.pop()
            stack.pop()
        elif c == "(":
            stack.append(c)
        elif c == "*":
            output = output + c
        elif len(stack) == 0 or stack[-1] == "(" or higherPrecedence(c, stack[-1]):
            stack.append(c)
        else:
            while len(stack) != 0 and stack[-1] != "(" and not higherPrecedence(c, stack[-1]):
                output = output + stack.pop()
            stack.append(c)

    while len(stack) != 0:
        output = output + stack.pop()

    return output

def higherPrecedence(a, b):
    p = ["+", ".", "*"]
    return p.index(a) > p.index(b) if a in p and b in p else False

class NFAState:
    state_count = 0

    def __init__(self):
        self.state_id = NFAState.state_count
        NFAState.state_count += 1
        self.next_states = {}

    @staticmethod
    def reset_state_count():
        NFAState.state_count = 0


class NFA:
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = accept_states

    def test(self, string):
        current_states = [self.start_state]
        for symbol in string:
            next_states = []
            for state in current_states:
                next_states.extend(state.next_states.get(symbol, []))
                next_states.extend(state.next_states.get('ε', []))
            current_states = next_states
        return any(state in self.accept_states for state in current_states)

def evalRegexSymbol(et):
    start_state = NFAState()
    end_state = NFAState()
    start_state.next_states[et.value] = [end_state]
    return start_state, end_state

def evalRegexConcat(et):
    left_nfa = evalRegex(et.left)
    right_nfa = evalRegex(et.right)
    left_nfa[1].next_states['ε'] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]

def evalRegexUnion(et):
    start_state = NFAState()
    end_state = NFAState()
    up_nfa = evalRegex(et.left)
    down_nfa = evalRegex(et.right)
    start_state.next_states['ε'] = [up_nfa[0], down_nfa[0]]
    up_nfa[1].next_states['ε'] = [end_state]
    down_nfa[1].next_states['ε'] = [end_state]
    return start_state, end_state

def evalRegexKleene(et):
    start_state = NFAState()
    end_state = NFAState()
    sub_nfa = evalRegex(et.left)
    start_state.next_states['ε'] = [sub_nfa[0], end_state]
    sub_nfa[1].next_states['ε'] = [sub_nfa[0], end_state]
    start_state.next_states['ε'] = [end_state, sub_nfa[0]]
    return start_state, end_state

def evalRegex(et):
    if et._type == Type.SYMBOL:
        return evalRegexSymbol(et)
    elif et._type == Type.CONCAT:
        return evalRegexConcat(et)
    elif et._type == Type.UNION:
        return evalRegexUnion(et)
    elif et._type == Type.KLEENE:
        return evalRegexKleene(et)

def regexToNFA(regex):
    postfix_regex = postfix(regex)
    expression_tree = constructTree(postfix_regex)
    NFAState.reset_state_count()
    nfa_start, nfa_end = evalRegex(expression_tree)
    return NFA(nfa_start, [nfa_end])

def printTransitionTable(nfa):
    transition_table = []
    visited = set()

    def visit_state(state):
        if state in visited:
            return
        visited.add(state)
        for symbol, next_states in state.next_states.items():
            for next_state in next_states:
                transition_table.append((f"q{state.state_id}", symbol, f"q{next_state.state_id}"))
                visit_state(next_state)

    visit_state(nfa.start_state)
    return transition_table

def visualizeNFA(nfa, filename='nfa'):
    dot = Digraph(filename=filename, format='png')
    dot.attr(rankdir='LR')
    visited = set()

    def add_states(state):
        if state in visited:
            return
        visited.add(state)
        if state in nfa.accept_states:
            dot.node(f'q{state.state_id}', shape='doublecircle')
        else:
            dot.node(f'q{state.state_id}')
        
        if state == nfa.start_state:
            dot.node('start', shape='none')
            dot.edge('start', f'q{state.state_id}')
        
        for symbol, next_states in state.next_states.items():
            for next_state in next_states:
                if symbol == 'ε':
                    dot.edge(f'q{state.state_id}', f'q{next_state.state_id}', label='ε')
                else:
                    dot.edge(f'q{state.state_id}', f'q{next_state.state_id}', label=symbol)
                add_states(next_state)

    add_states(nfa.start_state)
    filename_with_extension = f'{filename}.gv'
    dot.render(filename_with_extension, directory='static', cleanup=True) 
    return f'{filename}.gv.png'
