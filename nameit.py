import subprocess
import argparse
import os
import glob
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
from os import listdir

from name_extractor.trie import Trie
from name_extractor.scan_repo import scan_repo, CACHE_FILE

XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'nameit')

def enable_cache():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def interactive_suggestion(suggest_trie):
    while True:
        query = raw_input('Enter query: ')
        if query == 'exit':
            break
        else:
            print suggest_trie.autocomplete(query)


def load_trie():
    """
    Load trie from the repositories downloaded to local temp dir [REPO_DIR]
    """
    repo_paths = [os.path.join(REPO_DIR, f) for f in listdir(REPO_DIR)]
    suggest_trie = Trie()
    for path in repo_paths:
        variable_set, class_set, method_set, name_freq = scan_repo(path)
        for name in variable_set:
                suggest_trie.insert(name, name_freq[name], "variable")
        for name in class_set:
            suggest_trie.insert(name, name_freq[name], "class")
        for name in method_set:
            suggest_trie.insert(name, name_freq[name], "method")

    return suggest_trie


def format_code(code):

    return highlight(code,
                     PythonLexer(),
                     TerminalFormatter(bg='dark'))


def format_names(names):
    output = []
    for name in names:
        output.append("{0:<20}{1:<25}{2:<30}\n".format(*name))
    return "".join(output)


def grep_code_snippet_with_name(name, filepath=REPO_DIR):
    args = ['grep', '-r', name, '-m 5', '-A 3', '-B 3', filepath]
    # -m num: Stop reading the file after num matches.
    # --context num: Print num lines of leading and trailing context.
    res = subprocess.check_output(args, stderr=subprocess.STDOUT)
    return res


def get_parser():
    parser = argparse.ArgumentParser(description='instant python naming suggestion via the command line')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='naming prefix query')
    parser.add_argument('-t', '--type', help='specify naming type 0:variable, 1: class,  2: method', default=3, type=int)
    parser.add_argument('-c', '--context', help='display the code context', type=str)
    parser.add_argument('-l', '--load', help='load repository', type=str)
    parser.add_argument('-i', '--interactive', help='interactive mode', action='store_true')
    parser.add_argument('-C', '--clear-cache', help='clear the cache', action='store_true')

    return parser


def command_line_runner():
    parser = get_parser()
    args = parser.parse_args()
    if args.clear_cache:
        for cache in glob.glob('{0}*'.format(CACHE_FILE)):
            os.remove(cache)
        print "successfully clean cache"
        return
        
    if args.load:
        filename = args.load
        # TODO: download the file
        # currently use script instead
        print "not implemented yet!"
        return

    if args.context:
        res = grep_code_snippet_with_name(args.context)
        print format_code(res)
        return

    name_type = None

    suggest_trie = load_trie()
    if args.interactive:
        interactive_suggestion(suggest_trie)
        return

    if args.type:
        all_name_type = ['variable', 'class', 'method', None]
        name_type = all_name_type[args.type]

    if not args.query:
        parser.print_help()
        return
    else:
        for q in args.query:
            names = suggest_trie.autocomplete(q, name_type)
            print format_names(names)
        return


if __name__ == "__main__":
    command_line_runner()
