import sys
from name_extractor.tokenize_code import analyze_code
from name_extractor.trie import Trie
from name_extractor.scan_repo import scan_dir


def main():
    print sys.argv
    assert len(sys.argv) >= 2, "usage: python main.py [filename.py]"
    file_list = sys.argv[1:]
    suggest_trie = Trie()
    for filename in file_list:
        variable_set, class_set, method_set, name_freq = analyze_code(filename)
        for name in variable_set:
            suggest_trie.insert(name, name_freq[name])

    interactive_suggestion(suggest_trie)


def interactive_suggestion(suggest_trie):
    while True:
        query = raw_input('Enter query: ')
        if query == 'exit':
            break
        else:
            print suggest_trie.autocomplete(query)

if __name__ == "__main__":

    name_freq = scan_dir('/tmp/exp_dir', analyze_code)
    suggest_trie = Trie()
    for name in name_freq:
        suggest_trie.insert(name, name_freq[name])

    interactive_suggestion(suggest_trie)
