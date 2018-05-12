import collections
from FA.Dfa import Dfa

# This was my original implementation of NFA, which uses recursion. Obviously this is not a good choice, as python is
# depth limited and the implementation adds a recursion for every char added,
# so this will not work well for large inputs.

# I stopped working on this once I created IterNFA, so sorry if it is messy,
# but it is just here for example of what not to do.
class RecursiveNfa:

    # transitions is a dictionary of dictionaries
    # the None transition is the default transition
    def __init__(self, states=None, alphabet=None, transitions=None, start=None, ends=None):

        # default setup
        if states is None:
            self.states = ["q1"]
        else:
            self.states = states

        if alphabet is None:
            self.alphabet = {}
        else:
            self.alphabet = alphabet

        if transitions is None:
            self.transitions = {"q1": {None: ["q1"]}}
        else:
            self.transitions = transitions

        if start is None:
            self.start = "q1"
        else:
            self.start = start

        if ends is None:
            self.ends = []
        else:
            self.ends = ends

        if self.start not in self.states:
            raise ValueError("Start state: " + str(self.start) + " not in states: " + str(self.states))

        for end in self.ends:
            if end not in self.states:
                raise ValueError("End state: " + str(end) + " not in states: " + str(self.states))

        for sstate, letters in self.transitions.items():

            if sstate not in self.states:
                raise ValueError("Transition start state: " + str(sstate) + " not in states: " + str(self.states))

            for letter, fstates in letters.items():

                if (letter not in self.alphabet) and (letter is not None) and (letter is not ""):
                    raise ValueError("Unknown symbol: '" + str(letter) + "' in transition from state: " + str(sstate))

                for fstate in fstates:
                    if fstate not in self.states:
                        raise ValueError("Unknown transition finish state: " + str(fstate) +
                                         " in the transition starting in state " + str(sstate) +
                                         " with symbol " + str(letter))

    def interpretRecurse(self, input, state, depth, maxdepth, verbose):
        if depth == maxdepth:
            return False

        nextstates = []

        # if the length is zero, we have an empty string.
        if len(input) == 0:

            tin = input
            if not isinstance(input, collections.Hashable):
                tin = ""

            # if the current state is accept, then we accept
            if state in self.ends:
                if verbose:
                    print("Input is empty and in end state, accepting")
                return True

            # if the empty string has a specific transition
            elif tin in self.transitions[state]:
                if verbose:
                    print("Input is empty, not in accept state, and have specified transition to states: " +
                          str(self.transitions[state][tin]) + " for empty string, recursing to those states.")
                for nextstate in self.transitions[state][tin]:
                    if self.interpretRecurse(input, nextstate, depth + 1, maxdepth, verbose):
                        return True

            # otherwise if the current state has a default transition
            elif None in self.transitions[state]:
                if verbose:
                    print("Input is empty, not in accept state, and no specified transition to states, going" +
                          " to default transition to states: " + str(self.transitions[state][None]) +
                          " for empty string, recur sing to those states.")

                for nextstate in self.transitions[state][None]:
                    if self.interpretRecurse(input, nextstate, depth + 1, maxdepth, verbose):
                        return True
            # then there are no states to go to and we will end false
            return False

        # theres at least one symbol in the input

        nextstates = []
        sym = input[0]

        if state not in self.transitions:
            if verbose:
                print("No transition for given symbol " + str(sym) + " in state: " + str(state) + " returning.")
            return state in self.ends

        if sym in self.transitions[state]:
            if verbose:
                print("Transition for given symbol " + str(sym) + " in state: " + str(state) + " to states: " +
                      str(self.transitions[state][sym]))
            nextstates = self.transitions[state][sym]

        elif None in self.transitions[state]:
            if verbose:
                print("Made default transition for given symbol " + str(sym) + " in state: " + str(
                    state) + " to states: " +
                      str(self.transitions[state][None]))
            nextstates = self.transitions[state][None]

        # otherwise nextstates is empty

        for nextstate in nextstates:
            if self.interpretRecurse(input[1:], nextstate, depth + 1, maxdepth, verbose):
                return True

        if "" in self.transitions[state]:
            for nextstate in self.transitions[state][""]:
                if self.interpretRecurse(input, nextstate, depth + 1, maxdepth, verbose):
                    return True

        if verbose:
            print("No transition made (no next states) for given symbol " + str(sym) + " in state: " + str(state))
        return False

    def toDFA(self):
        import itertools
        def powerset(iterable):
            s = list(iterable)
            return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

        def eclosure(state, states, trans):
            if state not in states:
                raise ValueError("State not in states - ECLOSURE")
            l = [state]
            reached = [state]
            while len(l) > 0:
                s = l[0]
                if s not in reached:
                    reached.append(s)
                if s in trans and "" in trans[s]:
                    for f in trans[s][""]:
                        if f not in reached:
                            l.append(f)
                            reached.append(f)

            return reached

        def possibleStates(states, start, trans):
            1

        trans = {}
        start = eclosure(self.start, self.states, self.transitions)
        states = possibleStates(self.states, self.start, self.transitions)
        for state in self.states:
            for stateset in states:
                if stateset not in trans:
                    trans[stateset] = {}

                if state in stateset and state in self.transitions:
                    for sym, fss in self.transitions[state].items():
                        if sym not in trans[stateset]:
                            trans[stateset][sym] = []
                        for fs in fss:
                            if fs not in trans[stateset][sym]:
                                trans[stateset][sym].append(fs)

        ends = []
        for end in self.ends:
            for state in states:
                if end in state and state not in ends:
                    ends.append(state)

        return (states, self.alphabet, trans, start, ends)

    def copy(self):
        return RecursiveNfa(self.states, self.alphabet, self.transitions, self.start, self.ends)

    # interpret call
    def interpret(self, input, maxdepth=None, verbose=False):
        if maxdepth == None:
            maxdepth = len(input) * 100
        return self.interpretRecurse(input=input, state=self.start, depth=0, maxdepth=maxdepth, verbose=verbose)

    def concatenate(self, other):
        start = self.start
        al = self.alphabet + [a for a in other.alphabet if a not in self.alphabet]

        otn = {}
        trans = self.transitions
        otn = {}
        states = self.states
        for state in other.states:
            c = 0
            if state in self.states:
                while c in states:
                    c += 1
            else:
                c = state
            states.append(c)
            otn[state] = c

        ends = [otn[end] for end in other.ends]

        for state in other.states:
            ns = otn[state]
            if ns not in trans:
                trans[ns] = {}
            if state in other.transitions:
                for sym, finstates in other.transitions[state].items():
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

        return RecursiveNfa(states, al, trans, start, ends)

    def union(self, other):
        al = self.alphabet + [a for a in other.alphabet if a not in self.alphabet]

        otn = {}
        states = self.states
        for state in other.states:
            c = 0
            if state in self.states:
                while c in states:
                    c += 1
            else:
                c = state
            states.append(c)
            otn[state] = c
        ends = self.ends + [otn[f] for f in other.ends]

        start = 0
        while start in states:
            start += 1

        states.append(start)

        trans = self.transitions
        for state in other.states:
            ns = otn[state]
            if ns not in trans:
                trans[ns] = {}
            if state in other.transitions:
                for sym, finstates in other.transitions[state].items():
                    if sym not in trans[ns]:
                        trans[ns][sym] = []
                    for finstate in finstates:
                        nfs = otn[finstate]
                        if nfs not in trans[ns][sym]:
                            trans[ns][sym].append(nfs)

        trans[start] = {"": [self.start, otn[other.start]]}

        return RecursiveNfa(states, al, trans, start, ends)

    def star(self):
        trans = self.transitions

        al = self.alphabet
        states = self.states
        start = 0
        while start in states:
            start += 1

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

        return RecursiveNfa(states=states, alphabet=al, transitions=trans, start=start, ends=ends)


if __name__ == "__main__":
    n = RecursiveNfa()
    print(n.interpret("abc"))

    # accepts odd number of symbols
    n = RecursiveNfa(states=['q1', 'q2'], alphabet={}, transitions={'q1': {None: ['q2'], "": ['q1']},
                                                                    'q2': {None: ['q1'], "": ['q2']}},
                     start='q1', ends=['q2'])

    print(n.interpret("abc"))
    print(n.interpret("ab"))

    # try it with a list of symbols?
    print(n.interpret(["a", "b", "\\n", -2, -5]))
    print(n.interpret(["a", "b", "\\n", -5]))
