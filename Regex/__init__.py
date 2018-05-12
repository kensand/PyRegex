import string

import FA



class Regex:
    # the atomic unit class of a regex, used to represent each expression
    class Section:

        # Enumeration of the different
        CHAR_SECTION = 0
        SET_SECTION = 1
        SEQUENCE_SECTION = 2
        STAR_SECTION = 3
        PLUS_SECTION = 4
        QUESTION_SECTION = 5
        REPEAT_SECTION = 6
        SectionTypes = [CHAR_SECTION, SET_SECTION, SEQUENCE_SECTION, STAR_SECTION, PLUS_SECTION, QUESTION_SECTION,
                        REPEAT_SECTION]

        # Constructor for a section, that takes the section type and the respective content
        # (another section or string, depending on the type)
        def __init__(self, sectype=CHAR_SECTION, content=None):
            if sectype not in self.SectionTypes:
                raise ValueError("Unknown Section type" + str(sectype))
            self.type = sectype
            if content == None:
                self.content = ''
            else:
                self.content = content

        # Converts a Section to a NFA by recursively converting
        # its content and adding an NFA operation to the resulting nfa
        # Character NFAs act as the base case for the recursion

        def tonfa(self):
            def makeCountNFA(count, nfa):
                s = FA.gensym()
                ret = FA.Nfa(states=[s], alphabet=[], transitions={}, start=s, ends=[s])
                for i in range(count):
                    ret = ret.concatenate(nfa)
                return ret

            if self.type == self.CHAR_SECTION:
                return FA.Nfa(states=[0, 1], alphabet=[self.content], start=0, ends=[1],
                              transitions={0: {self.content: [1]}})

            elif self.type == self.SET_SECTION:
                if len(self.content) == 0:
                    raise ValueError("Set Section is given an empty set of regexs")
                else:
                    unionreg = self.content[0].tonfa()
                    for section in self.content[1:]:
                        unionreg = unionreg.union(section.tonfa())
                    return unionreg

            elif self.type == self.SEQUENCE_SECTION:
                if len(self.content) == 0:
                    raise ValueError("Sequence Section is given an empty set of regexs")
                else:
                    concatreg = self.content[0].tonfa()
                    for section in self.content[1:]:
                        concatreg = concatreg.concatenate(section.tonfa())
                    return concatreg

            elif self.type == self.STAR_SECTION:
                if self.content == None:
                    raise ValueError("Star Section has no preceding regex")
                else:
                    return self.content.tonfa().copy().star()

            elif self.type == self.PLUS_SECTION:
                if self.content == None:
                    raise ValueError("Plus Section has no preceding regex")
                else:
                    return self.content.tonfa().concatenate(self.content.tonfa().star())

            elif self.type == self.QUESTION_SECTION:
                if self.content == None:
                    raise ValueError("Plus Section has no preceding regex")
                else:
                    s = FA.gensym()
                    return self.content.tonfa().union(
                        FA.Nfa(states=[s], alphabet=[], transitions={}, start=s, ends=[s]))

            elif self.type == self.REPEAT_SECTION:

                if self.content == None:
                    raise ValueError("Repeat Section has no preceding regex")
                if self.andmore == None:
                    raise ValueError("Repeat Section has no andmore arg")
                if self.start == None:
                    raise ValueError("Repeat Section has no repeat start number")
                if self.start <= 0:
                    raise ValueError("Repeat Section has an invalid repeat start number")
                if self.end is not None and self.end <= 0:
                    raise ValueError("Repeat Section has an invalid repeat start number")

                if self.end == None:  # we only have a start
                    if self.andmore:  # we want more than that number of repetitions
                        cnfa = self.content.tonfa()
                        repnfa = makeCountNFA(self.start, cnfa)
                        return repnfa.concatenate(cnfa.star())
                    else:  # we only want that number of repetitions
                        cnfa = self.content.tonfa()
                        return makeCountNFA(self.start, cnfa)

                else:
                    s = FA.gensym()
                    ret = FA.Nfa(states=[s], alphabet=[], transitions={}, start=s, ends=[s])
                    cnfa = self.content.tonfa()
                    for i in range(self.start, self.end + 1):
                        repeatnfa = makeCountNFA(i, cnfa)
                        ret = ret.union(repeatnfa)
                    return ret

            else:
                raise RuntimeError("Unknown Section type: ", self.type)

    # function to create a new section depending on the the character(s) in the regex
    def nextsection(self, r):

        n = None  # placeholder for next Section
        rest = r  # place holder fot the remaining part of the regex

        if not len(r) == 0:
            # escaped the next character

            if r[0] == '\\':
                if len(r) < 2:
                    raise ValueError("Expected expression following \\")

                elif r[1] == '\\':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '\\'), r[2:]

                elif r[1] == 's':
                    n, rest = self.Section(self.Section.SET_SECTION, [self.Section(self.Section.CHAR_SECTION, c)
                                                                      for c in string.whitespace]), r[2:]

                elif r[1] == 'd':
                    n, rest = self.Section(self.Section.SET_SECTION,
                                           [self.Section(self.Section.CHAR_SECTION, c) for c in string.digits]), r[2:]

                elif r[1] == 'D':
                    n, rest = self.Section(self.Section.SET_SECTION,
                                           [self.Section(self.Section.CHAR_SECTION, c) for c in
                                            string.ascii_letters + string.punctuation + string.whitespace]), r[2:]

                elif r[1] == 'S':
                    n, rest = self.Section(self.Section.SET_SECTION,
                                           [self.Section(self.Section.CHAR_SECTION, c) for c in
                                            string.ascii_letters + string.punctuation + string.digits]), r[2:]

                elif r[1] == '(':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '('), r[2:]

                elif r[1] == ')':
                    n, rest = self.Section(self.Section.CHAR_SECTION, ')'), r[2:]

                elif r[1] == '[':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '['), r[2:]

                elif r[1] == ']':
                    n, rest = self.Section(self.Section.CHAR_SECTION, ']'), r[2:]

                elif r[1] == '*':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '*'), r[2:]

                elif r[1] == '.':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '.'), r[2:]

                elif r[1] == '?':
                    n, rest = self.Section(self.Section.CHAR_SECTION, '?'), r[2:]

                elif r[1] == 'n':
                    # not really sure how this would work out with line splitting...
                    n, rest = self.Section(self.Section.CHAR_SECTION, '\n'), r[2:]

                else:
                    raise ValueError("Unknown expression following \\")

            elif r[0] == '*':
                n, rest = self.Section(sectype=self.Section.STAR_SECTION, content=None), r[1:]

            elif r[0] == '+':
                n, rest = self.Section(sectype=self.Section.PLUS_SECTION, content=None), r[1:]

            elif r[0] == '?':
                n, rest = self.Section(sectype=self.Section.QUESTION_SECTION, content=None), r[1:]

            # find a matching parenthesis starting at the end and working forwards
            elif r[0] == '(':
                i = 1
                count = 0
                while i < len(r):
                    if r[i] == ')' and not r[i - 1] == '\\':
                        if count == 0:
                            break
                        elif count > 0:
                            count -= 1
                        else:
                            raise ValueError("Mismatched parenthesis. Use a backslash ('\\') to escape parenthesis.")

                    if r[i] == '(' and not r[i - 1] == '\\':
                        count += 1

                    i += 1

                if i == len(r):
                    raise ValueError("Mismatched parenthesis. Use a backslash ('\\') to escape parenthesis.")
                else:
                    n, rest = self.Section(sectype=self.Section.SEQUENCE_SECTION, content=self.getsections(r[1:i])), r[
                                                                                                                     i + 1:]

            elif r[0] == '{':
                i = 1
                while i < len(r) and r[i] != '}':
                    i += 1
                if i >= len(r):
                    raise ValueError("Regex repeat clause missing closing '}'. Did you forget to escape a '{' ?")
                inside = r[1:i]
                n, rest = self.Section(sectype=self.Section.REPEAT_SECTION, content=None), r[i + 1:]
                n.start = None
                n.end = None

                if ',' in inside:
                    splist = [x for x in inside.split(',') if len(x) > 0]
                    n.andmore = True
                    if len(splist) > 2:
                        raise ValueError("Regex repeat clause arguments are invalid")
                    if len(splist) == 2:
                        try:
                            n.start = int(splist[0])
                        except Exception as e:
                            raise ValueError("Regex repeat clause start argument is invalid: " + splist[0])

                        if n.start < 0:
                            raise ValueError("Regex repeat clause start argument is invalid: " + splist[0])

                        try:
                            n.end = int(splist[1])
                        except Exception as e:
                            raise ValueError("Regex repeat clause end argument is invalid: " + splist[1])

                    if len(splist) == 1:
                        try:
                            n.start = int(splist[0])
                        except Exception as e:
                            raise ValueError("Regex repeat clause start argument is invalid: " + splist[0])

                else:
                    try:
                        n.start = int(inside)
                    except Exception as e:
                        raise ValueError("Regex repeat clause start argument is invalid: " + inside)

                    if n.start < 0:
                        raise ValueError("Regex repeat clause start argument is invalid: " + inside)

                    n.end = None
                    n.andmore = False

            # Set of options
            elif r[0] == '[':
                i = 1
                count = 0
                while i < len(r):
                    if r[i] == ']' and not r[i - 1] == '\\':
                        if count == 0:
                            break
                        elif count > 0:
                            count -= 1
                        else:
                            raise ValueError("Mismatched parenthesis. Use a backslash ('\\') to escape parenthesis.")

                    if r[i] == '[' and not r[i - 1] == '\\':
                        count += 1

                    i += 1

                if i == len(r):
                    raise ValueError("Mismatched Square Brackets. Use a backslash ('\\') to escape Square Brackets.")
                else:
                    n, rest = self.Section(sectype=self.Section.SET_SECTION, content=self.getsections(r[1:i])), r[
                                                                                                                i + 1:]

            elif r[0] == '.':
                n, rest = self.Section(self.Section.SET_SECTION,
                                       [self.Section(self.Section.CHAR_SECTION, c) for c in string.printable]), r[1:]

            else:
                n, rest = self.Section(self.Section.CHAR_SECTION, r[0]), r[1:]

        return n, rest

    # function that splits all the sections in the regex, then applies the required stacking of sections that modify
    # others, such as star and question mark
    def getsections(self, regex):
        sections = []
        r = regex
        while len(r) > 0:
            s, r = self.nextsection(r)
            sections.append(s)

        i = 0
        while i < len(sections):
            if sections[i].type == self.Section.STAR_SECTION:
                if i == 0:
                    raise ValueError("Star Section has no preceeding Section to apply to")
                else:
                    sections[i].content = sections[i - 1]
                    sections.pop(i - 1)

            elif sections[i].type == self.Section.PLUS_SECTION:
                if i == 0:
                    raise ValueError("Star Section has no preceeding Section to apply to")
                else:
                    sections[i].content = sections[i - 1]
                    sections.pop(i - 1)

            elif sections[i].type == self.Section.QUESTION_SECTION:
                if i == 0:
                    raise ValueError("Question Section has no preceeding Section to apply to")
                else:
                    sections[i].content = sections[i - 1]
                    sections.pop(i - 1)

            elif sections[i].type == self.Section.REPEAT_SECTION:
                if i == 0:
                    raise ValueError("Repeat Section has no preceeding Section to apply to")
                else:
                    sections[i].content = sections[i - 1]
                    sections.pop(i - 1)
            i += 1

        # print(sections)
        return sections

    def __init__(self, r, verbose=False):
        self.r = r
        self.verbose = verbose
        sect = self.Section(self.Section.SEQUENCE_SECTION, self.getsections(r))
        self.n = sect.tonfa()
        # self.d = self.n.toDFA()

    # interprets a given string, returning true if the Regex accepts, and false if the Regex rejects.
    def interpret(self, s, verbose=None):
        if verbose == None:
            verbose = self.verbose

        return self.n.interpret(s, verbose=verbose)
