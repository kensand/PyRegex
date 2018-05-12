import os
import io
import string
import argparse
import sys
import json

#The DFA class, emulates a dfa given the required info
class Dfa:
    #dfa constructor
    def __init__(self, states, alphabet, transitions, start, ends):
        self.verifyDFA(start, ends, states, alphabet, transitions)
        self.t = transitions
        self.st = states
        self.a = alphabet
        self.s = start
        self.f = ends

    #the interpreter function, takes a string
    def interp(self, s, verbose=False):
        r = self.s
        #print(s)
        for i in range(len(s)):
            if s[i] not in self.a:
                raise(Exception("Invalid character: '" + s[i] + "' in string: '" + s + "', Rest of line was ignored."))
            if s[i] in self.t[r]:

                if verbose:
                    print("Current State: '", r, "' \t Symbol: '", s[i], "'->\t Result State: '", self.t[r][s[i]], "'")
                r = self.t[r][s[i]]
            else:
                if verbose:
                    print("Current State: '", r, "' \t Symbol: '", s[i], "'->\t No transition, False")
                return False
        if r in self.f:
            return True
        else:
            return False

    #function to verify a dfa
    def verifyDFA(self, start, ends, states, al, trans):
        if start not in states:
            raise Exception("Start state: ", start, " not found in State set: ", states)
        for end in ends:
            if end not in states:
                raise Exception("End state: ", end, " not found in State set: ", states)

        for tran in trans:
            if tran[0] not in states:
                raise Exception("transition start state: " +str(tran[0])+ " not found in State set: " +str(states))

            if tran[1] not in al:
                raise Exception("transition symbol: '" +str(tran[1])+ "' not found in alphabet: " +str(al))

            if tran[2] not in states:
                raise Exception("transition end state: " +str( tran[2]) + " not found in State set: " + str(states))
def dfa():
    #arg parse definitions
    parser = argparse.ArgumentParser(usage="python dfa.py -d <dfafile> [-v]", description="Read in a DFA file and process each line of STDIN using that DFA, printing the results to STDOUT.")
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-d', action='store', dest='file', default=None, help="The input DFA file, in JSON format.", required=True)
    parser.add_argument('-v', action='store_true', dest='verbose', help="Print both the DFA JSON and each transition as it occurs.")
    args = parser.parse_args()


    #load the json file
    d = None
    try:
        with open(args.file) as f:
            d = json.load(f)
    except Exception as e:
        print("Error reading file:", e)
        exit(1)

    if d is None:
        print("Empty file, exiting")
        exit(2)


    #transform the json to the format the dfa class requires
    a = []
    t = {}
    for tran in d["transition"]:
        if tran["current_state"] not in t:
            t[tran["current_state"]] = {}

        if tran["next_symbol"] not in a:
            a.append(tran["next_symbol"])
        if tran["next_symbol"] not in t[tran["current_state"]]:
            t[tran["current_state"]][tran["next_symbol"]] = tran["new_state"]
        else:
            print ("Multiple transitions for state: "+ str( tran["current_state"]) +" with symbol " + str(tran["next_symbol"]))
            raise Exception("Multiple transitions for state: "+ str( tran["current_state"]) +" with symbol " + str(tran["next_symbol"]))
    #print(d)
    #print(t)

    #create the dfa
    dfa = DFA(alphabet=a, states=d['states'], start=d['start_state'], ends=d['final_states'], transitions=t)

    #print the dfa if verbose mode is on
    if args.verbose:
        print("---BEGIN DFA definition---")
        print(json.dumps(d, indent=4))
        print("---END DFA definition---")

    #read each line from stdin, strip and interpret the string, print the result.
    for line in sys.stdin:
        l = line.strip()
        try:
            res = dfa.interp(l, verbose=args.verbose)
            out = None
            if res:
                out = "NOT ACCEPT"
            else:
                out = "ACCEPT"
            print(l, "-->", out)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    dfa()