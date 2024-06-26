def objectNFA(s,l,tm,ss,fs):
    return {
        'states': s,
        'letters': l,
        'transition_matrix': tm,
        'start_states': ss,
        'final_states':fs
    }


def unitLenRegexToNFA(alphabet):
    s = ["Q0","Q1"]
    a = [alphabet]
    tm = [
        ["Q0",alphabet,"Q1"],
    ]
    ss = ["Q0"]
    fs = ["Q1"]
    return objectNFA(s, a, tm, ss, fs)


def concatenationNFA(NFA1, NFA2):
    # Making `a` array
    a = [ alphabet for alphabet in NFA1['letters']]
    for l in NFA2['letters']:
        if l not in a:
            a.append(l)

    # Making `s, ss and fs` array
    s = []
    ss = []
    fs = []
    tm = []
    for i in range(len(NFA1['states'])):
        current_state = NFA1['states'][i]
        s.append(current_state)
        if current_state in NFA1['start_states']:
            ss.append(current_state)

    for i in range(len(NFA2['states'])):
        current_state = NFA2['states'][i]
        effective_state = "Q"+str(i+len(NFA1['states']))
        s.append(effective_state)
        if current_state in NFA2['final_states']:
            fs.append(effective_state)
        
        if current_state in NFA2['start_states']:
            for nfa1_final_state in NFA1['final_states']:
                tm.append([nfa1_final_state,'ε',effective_state])

    # Making `tm` array
    for arc in NFA1['transition_matrix']:
        tm.append(arc)
    
    for arc in NFA2['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(int(os[1:])+len(NFA1['states']))
        n_ns = 'Q'+ str(int(ns[1:])+len(NFA1['states']))
        tm.append([n_os, il, n_ns ])
    
    return objectNFA(s, a,tm, ss, fs)


def unionNFA(NFA1, NFA2):
    # Making `a` array
    a = [ alphabet for alphabet in NFA1['letters']]
    for l in NFA2['letters']:
        if l not in a:
            a.append(l)

    # Making `s, ss and fs` array
    s = ["Q0"]
    ss = ["Q0"]
    fs = []
    tm = []

    for i in range(len(NFA1['states'])):

        current_state = NFA1['states'][i]
        effective_state = 'Q'+str(i+1)
        s.append(effective_state)

        if current_state in NFA1['final_states']:
            fs.append(effective_state)
        if current_state in NFA1['start_states']:
            tm.append(['Q0','ε',effective_state])


    for i in range(len(NFA2['states'])):

        current_state = NFA2['states'][i]
        effective_state = "Q"+str(i+1+len(NFA1['states']))
        s.append(effective_state)

        if current_state in NFA2['final_states']:
            fs.append(effective_state)
        if current_state in NFA2['start_states']:
            tm.append(['Q0','ε',effective_state])
    
    # Making `tm` array
    for arc in NFA1['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:]))
        n_ns = 'Q'+ str(1+int(ns[1:]))
        tm.append([n_os, il, n_ns ])
    
    for arc in NFA2['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:])+len(NFA1['states']))
        n_ns = 'Q'+ str(1+int(ns[1:])+len(NFA1['states']))
        tm.append([n_os, il, n_ns ])
    
    return objectNFA(s, a, tm, ss, fs)


def starNFA(NFA):
    s = ['Q0']
    for i in range(len(NFA['states'])):
        effective_state = 'Q'+str(i+1)
        s.append(effective_state)
    
    index = 1+len(NFA['states'])
    only_final_state = 'Q'+str(index)
    s.append(only_final_state)

    l = [ letter for letter in NFA['letters'] ]
    ss = ['Q0']
    fs = [only_final_state]

    tm = []
    for arc in NFA['transition_matrix']:
        [os, il, ns] = arc
        n_os = 'Q'+ str(1+int(os[1:]))
        n_ns = 'Q'+ str(1+int(ns[1:]))
        tm.append([n_os, il, n_ns ])
    
    for st_state in NFA['start_states']:
        tm.append(['Q0','ε','Q'+ str(1+int(st_state[1:]))])
    tm.append(['Q0','ε',only_final_state])

    for fn_state in NFA['final_states']:
        tm.append(['Q'+ str(1+int(fn_state[1:])),'ε',only_final_state])
        for st_state in NFA['start_states']:
            tm.append(['Q'+ str(1+int(fn_state[1:])),'ε','Q'+ str(1+int(st_state[1:]))])
    
    return objectNFA(s, l, tm, ss, fs)


def isAlphabet(character):
    flag = False
    if (character>='a')and(character<='z'):
        flag = True
    elif (character>='0')and(character<='9'):
        flag = True
    return flag


def add_dot(regex):
    indices = []
    new_regex = regex[:]
    for i in range(len(regex)-1):
        cc = regex[i]
        cn = regex[i+1]
        if isAlphabet(cc) or (cc==')') or (cc=='*'):
            if isAlphabet(cn) or cn=='(':
                indices.append(i)
    
    for i in range(len(indices)):
        index = indices[i]
        new_regex = new_regex[:index+i+1]+"."+new_regex[index+i+1:]
    return new_regex


def infixToPostfix(regex):
    precedence ={
        '*': 3,
        '.': 2,
        '+': 1,
    }

    stack = []
    postfixRegex = ""
    for char in regex:
        if isAlphabet(char) or (char=='*'):
            postfixRegex += char
        elif char=='(':
            stack.append(char)
        elif char==')':
            while( (len(stack)!=0) and (stack[-1]!='(') ):
                postfixRegex += stack.pop()
            stack.pop()
        else:
            while( (len(stack)!=0) and 
            (stack[-1]=='*' or stack[-1]=='.') and 
            (precedence[char]<=precedence[stack[-1]]) 
            ):
                postfixRegex += stack.pop()
            stack.append(char)
    while len(stack)!=0:
        postfixRegex += stack.pop()
    return postfixRegex


def makeNFA(postfixRegex):
    nfaStack = []
    for char in postfixRegex:
        if isAlphabet(char):
            nfaStack.append(unitLenRegexToNFA(char))
        elif char=="*":
            nfaStack.append(starNFA(nfaStack.pop()))
        elif char=="+" or char=="|":
            NFA2 = nfaStack.pop()
            NFA1 = nfaStack.pop()
            nfaStack.append(unionNFA(NFA1,NFA2))
        elif char==".":
            NFA2 = nfaStack.pop()
            NFA1 = nfaStack.pop()
            nfaStack.append(concatenationNFA(NFA1,NFA2))
        else:
            print("Literally, an Edge case is there!")
    return nfaStack.pop()


def convertToNFA(regular_expression):
    if regular_expression=="":
        return unitLenRegexToNFA('ε')
    
    regular_expression = add_dot(regular_expression)
    regular_expression = infixToPostfix(regular_expression)
    return makeNFA(regular_expression)

def remove_slashes(string):
    # Menghapus '/' di awal dan di akhir string
    if string.startswith('/'):
        string = string[1:]
    if string.endswith('/'):
        string = string[:-1]
    return string