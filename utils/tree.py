class Node:
    def __init__(self):
        self.children = {}
        self.is_word = False

    def next(self, char: str) -> 'Node':
        return self.children.get(char)

    def __str__(self):
        return str(self.children)

class Tree:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.children.setdefault(char, Node())
        node.is_word = True

    def start(self, letter: str) -> Node:
        return self.root.children.get(letter)
    
    def is_word(self, word: str) -> bool:
        node = self.root
        for char in word:
            node, is_word = self.next(node, char)
            if not node:
                return False
        return is_word
    
    def can_extend(tree, prefix):
        node = tree.root
        for ch in prefix:
            node, is_word = tree.next(node, ch)
            if not node:
                return False
        return True
    
    def __str__(self):
        return str(self.root)