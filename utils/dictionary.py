import pickle
from pathlib import Path
from utils.tree import Tree

class DictionaryBuilder:
    def __init__(self, min_length=3):
        self._min_length = min_length
    
    def _build(self, dict_path: Path):
        with open(dict_path, 'r') as f:
            words = f.read().splitlines()

        tree = Tree()
        for word in words:
            if len(word) < self._min_length:
                continue
            tree.insert(word)
        return tree
    
    def get_or_build(self, dict_path: Path=Path("sowpods.txt"), rebuild=False):
        tree = None
        pkl_path = Path("tree.pkl")
        if rebuild or not pkl_path.exists():
            tree = self._build(dict_path)
            with open(pkl_path, 'wb') as f:
                pickle.dump(tree, f)
        else:
            with open(pkl_path, 'rb') as f:
                tree = pickle.load(f)
        return tree
    
    @property
    def min_length(self):
        return self._min_length
    
    @min_length.setter
    def min_length(self, value):
        raise AttributeError("min_length is immutable")
        
        

if __name__ == "__main__":
    builder = DictionaryBuilder()
    dict_path = Path("words_alpha.txt")
    tree = builder.get_or_build(dict_path)

    print(tree.is_word("cat"))

    node = tree.root
    word = ""
    for ch in "cats":
        node, is_word = tree.next(node, ch)
        if node is None:
            print(f"Prefix {word+ch} is invalid")
            break
        word += ch
        if is_word:
            print(f"Found word: {word}")