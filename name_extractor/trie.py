from collections import deque
import heapq


class Trie(object):
    def __init__(self):
        self.children = {}
        self.word_count = 0
        self.type = None

    def insert(self, word, word_count, type=None):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()

            node = node.children[char]
        node.word_count += word_count
        if node.type is None:
            node.type = type

    def contains(self, word):
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]

        return node.word_count > 0

    def autocomplete(self, prefix, name_type=None):
        node = self
        # move the pointer to the ending for prefix in trie
        for char in prefix:
            if char not in node.children:
                return set()
            node = node.children[char]

        result = node.bfs_search_suffix(prefix, name_type)
        # return top 10 frequent naming from the heap
        return heapq.nlargest(10, result, key=lambda word_freq: word_freq[1])

    def bfs_search_suffix(self, prefix, name_type=None):
        queue = deque()
        queue.append((self, prefix))
        result = set()
        while queue:
            node, prefix = queue.popleft()
            if node.word_count > 0:
                if name_type is None or name_type == node.type:
                    result.add((prefix,node.word_count, node.type))
            for char in node.children:
                next_node = node.children[char]
                queue.append((next_node, prefix + char))

        return list(result)


def test():
    word_freq_list = [('apple', 5), ('app', 100)]
    suggest_trie = Trie()
    for w, freq in word_freq_list:
        suggest_trie.insert(w, freq)

    print suggest_trie.autocomplete('app')


if __name__ == "__main__":
    test()
