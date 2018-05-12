import sys                                                                                                                                                                                                        
sys.path.append('../') 
from Regex import Regex


def testrgx(r, t, e, verbose=False):
    reg = Regex(r, verbose=verbose)
    res = reg.interpret(t, verbose=verbose)
    trs = ""
    if res == e:
        trs = "CORRECT::  "
    else:
        trs = "ERROR::    "
    print(trs + "Regex: '" + str(r) + "'\t Test: '" + str(t) + "'\t Expected: '" + str(e) + "'\t Actual: '" + str(
        res) + "'")


def tests():
    testrgx("ab+c", "abc", True)
    testrgx("ab+c", "ac", False)
    testrgx("ab+c", "abbc", True)
    testrgx("ab+c", "abbbbbbbbbbbbbbc", True)

    testrgx("a[bc]d", "ad", False)
    testrgx("a[bc]d", "abd", True)
    testrgx("a[bc]d", "acd", True)
    testrgx("a[bc]d", "azd", False)

    testrgx("a[bc]+d", "ad", False)
    testrgx("a[bc]+d", "abd", True)
    testrgx("a[bc]+d", "acd", True)
    testrgx("a[bc]+d", "abcbcccbd", True)
    testrgx("a[bc]+d", "abcbcccbzd", False)

    testrgx("a([bc]+z)*d", "ad", True)
    testrgx("a([bc]+z)*d", "abzd", True)
    testrgx("a([bc]+z)*d", "aczd", True)
    testrgx("a([bc]+z)*d", "abzczbzczczczbzd", True)
    testrgx("a([bc]+z)*d", "abzczbzczccbd", False)
    testrgx("(..........)*",
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            True, verbose=False)

    testrgx("ab{5}a", "abbbbba", True)
    testrgx("ab{5}a", "abbbba", False)
    testrgx("ab{5}a", "abbbbbba", False)
    testrgx("ab{3,5}a", "abbbbbba", False)
    testrgx("ab{3,5}a", "abbbbba", True)
    testrgx("ab{3,5}a", "abbbba", True)
    testrgx("ab{3,5}a", "abbba", True)
    testrgx("ab{3,5}a", "abba", False)
    testrgx("ab{3,}a", "abbbbba", True)
    testrgx("ab{3,}a", "abbbba", True)
    testrgx("ab{3,}a", "abbba", True)
    testrgx("ab{3,}a", "abba", False)


if __name__ == "__main__":
    tests()
