import sys
import tokenize
from token import *
import keyword
import __builtin__
from collections import Counter

from peek_generator import PeekGenerator

DEFINE = "def"
CLASS = "class"
preserved_word = keyword.kwlist + dir(__builtin__)


def analyze_code(filename):
    fp = open(filename)
    tokengen = tokenize.generate_tokens(fp.readline)
    tokengen = PeekGenerator(tokengen)
    last_token = None
    name_freq = Counter()
    class_set = set()
    method_set = set()
    for token in tokengen:
        token_type, tok_str, _, _, context = token
        if token_type == NAME and tok_str not in preserved_word:
            # look_head_token = tokengen.peek
            name_freq[tok_str] += 1
            if last_token and last_token[1] == CLASS:
                class_set.add(tok_str)

            if last_token and last_token[1] == DEFINE:
                method_set.add(tok_str)

        last_token = token

    name_set = set(name_freq.keys())
    variable_set = name_set - class_set - method_set

    fp.close()

    return variable_set, class_set, method_set, name_freq


def dump_to_stdout(variable_set, class_set, method_set, name_freq):
    for v in variable_set:
        print "v, %s, %d" % (v, name_freq[v])
    for c in class_set:
        print "c, %s, %d" % (c, name_freq[c])
    for m in method_set:
        print "m, %s, %d" % (m, name_freq[m])


if __name__ == "__main__":
    assert len(sys.argv) >= 2
    filename = sys.argv[1]
    variable_set, class_set, method_set, name_freq = analyze_code(filename)
    dump_to_stdout(variable_set, class_set, method_set, name_freq)
