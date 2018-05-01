from Nfa import Gensym

gensym = Gensym.Gensym()


class Nfa:
    def __init__(self, states, alphabet, transitions, start, ends):
        self.states = states
        self.trans = transitions
        self.al = alphabet
        self.start = start
        self.ends = ends

        if self.start not in self.states:
            raise ValueError("Start state: " + str(self.start) + " not in states: " + str(self.states))

        for end in self.ends:
            if end not in self.states:
                raise ValueError("End state: " + str(end) + " not in states: " + str(self.states))

        for sstate, letters in self.trans.items():

            if sstate not in self.states:
                raise ValueError("Transition start state: " + str(sstate) + " not in states: " + str(self.states))

            for letter, fstates in letters.items():

                if (letter not in self.al) and (letter is not None) and (letter is not ""):
                    raise ValueError("Unknown symbol: '" + str(letter) + "' in transition from state: " + str(sstate))

                for fstate in fstates:
                    if fstate not in self.states:
                        raise ValueError("Unknown transition finish state: " + str(fstate) +
                                         " in the transition starting in state " + str(sstate) +
                                         " with symbol " + str(letter))

    def accepts(self, state, instr):
        if len(instr) == 0:
            return state in self.ends
        return False

    def nextstatesandinputs(self, state, instr):
        if state not in self.states:
            raise ValueError("State " + str(state) + " not in states.")
        ret = []
        if len(instr) > 0:
            if state in self.trans:
                if instr[0] in self.al:
                    if instr[0] in self.trans[state]:
                        for tostate in self.trans[state][instr[0]]:
                            ret.append((tostate, instr[1:]))
                    elif None in self.trans[state]:
                        for tostate in self.trans[state][None]:
                            ret.append((tostate, instr[1:]))
                if "" in self.trans[state]:
                    for tostate in self.trans[state][""]:
                        ret.append((tostate, instr))

        else:
            if "" in self.trans[state]:
                for tostate in self.trans[state][""]:
                    ret.append((tostate, instr))
        return ret

    # Iterative interpretation, so that python doesn't freak out about recursion depth
    def interpret(self, instr, verbose=False):
        q = [(self.start, instr)]
        while len(q) > 0:
            # popping the front of the q is important, since it ensures breadth first search of solutions rather
            # than depth first, since loops could feasibly occur with empty strings
            # (but shouldnt with proper regex reduction).
            currstate, currinput = q.pop(0)
            if self.accepts(currstate, currinput):
                if verbose:
                    print("State: " + str(currstate) + "\t Input: " + currinput + "\t ACCEPT")
                return True
            if verbose:
                print("State: " + str(currstate) + "\t Input: " + currinput + "\t CONTINUE")

            q.extend(self.nextstatesandinputs(currstate, currinput))
        if verbose:
            print("Ran out of states \t REJECT")
        return False

    #copy function, because sometimes we dont want to apply star/con/union to the original NFA
    def copy(self):
        return Nfa(self.states, self.al, self.trans, self.start, self.ends)

    # basic NFA operations (also works for regular expressions)

    def concatenate(self, other):
        start = self.start
        al = self.al + [a for a in other.al if a not in self.al]

        trans = self.trans
        otn = {}
        states = self.states
        for state in other.states:
            if state in self.states:
                c = gensym()
                while c in self.states:
                    c = gensym()
            else:
                c = state
            states.append(c)
            otn[state] = c

        ends = [otn[end] for end in other.ends]

        for state in other.states:
            ns = otn[state]
            if ns not in trans:
                trans[ns] = {}
            if state in other.trans:
                for sym, finstates in other.trans[state].items():
                    if sym not in trans[ns]:
                        trans[ns][sym] = []
                    for finstate in finstates:
                        nfs = otn[finstate]
                        if nfs not in trans[ns][sym]:
                            trans[ns][sym].append(nfs)

        nos = otn[other.start]
        for f in self.ends:
            if f not in trans:
                trans[f] = {}
            if "" not in trans[f]:
                trans[f][""] = []
            if nos not in trans[f][""]:
                trans[f][""].append(nos)

        return Nfa(states, al, trans, start, ends)

    def union(self, other):
        al = self.al + [a for a in other.al if a not in self.al]

        otn = {}
        states = self.states
        for state in other.states:
            if state in self.states:
                c = gensym()
                while c in self.states:
                    c = gensym()
            else:
                c = state
            states.append(c)
            otn[state] = c
        ends = self.ends + [otn[f] for f in other.ends]

        start = 0
        while start in states:
            start += 1

        states.append(start)

        trans = self.trans
        for state in other.states:
            ns = otn[state]
            if ns not in trans:
                trans[ns] = {}
            if state in other.trans:
                for sym, finstates in other.trans[state].items():
                    if sym not in trans[ns]:
                        trans[ns][sym] = []
                    for finstate in finstates:
                        nfs = otn[finstate]
                        if nfs not in trans[ns][sym]:
                            trans[ns][sym].append(nfs)

        trans[start] = {"": [self.start, otn[other.start]]}

        return Nfa(states, al, trans, start, ends)

    def star(self):
        trans = self.trans

        al = self.al
        states = self.states
        start = 0
        while start in states:
            start += 1

        start = gensym()
        while start in self.states:
            start = gensym()

        ends = [start]

        for end in self.ends:
            if end not in trans:
                trans[end] = {}
            if "" not in trans[end]:
                trans[end][""] = []
            if start not in trans[end][""]:
                trans[end][""].append(start)

        trans[start] = {"": [self.start]}

        if start not in states:
            states.append(start)

        if start not in ends:
            ends.append(start)

        return Nfa(states=states, alphabet=al, transitions=trans, start=start, ends=ends)
