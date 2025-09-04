class Board:
    def __init__(self, rows=15, cols=15):
        # Initialize an empty board
        self.grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    def __getitem__(self, idx):
        return self.grid[idx]
    
    def __setitem__(self, idx, value):
        self.grid[idx] = value

    def place_word(self, word, r, c, dr, dc):
        """
        Place a word on the board at a given starting position and direction.

        Args:
            word (str): The word to place on the board.
            r (int): The starting row index (0-based).
            c (int): The starting column index (0-based).
            dr (int): Row direction increment. Use 0 for horizontal, 1 for vertical.
            dc (int): Column direction increment. Use 1 for horizontal, 0 for vertical.

        Example:
            board.place_word("cat", 2, 0, 0, 1)  # places "cat" horizontally starting at row 2, column 0
            board.place_word("dog", 0, 3, 1, 0)  # places "dog" vertically starting at row 0, column 3
        """
        for ch in word:
            self.grid[r][c] = ch
            r += dr
            c += dc


    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)

    
    # def scan_line(self, line):
    #     segments = []
    #     i = 0
    #     while i < len(line):
    #         if line[i] != ' ':  # start of a filled segment
    #             start = i
    #             while i < len(line) and line[i] != ' ':
    #                 i += 1
    #             end = i
    #             segments.append(line[start:end])
    #         else:
    #             i += 1
    #     return segments


    
    # def is_empty(self, r, c):
    #     return self.grid[r][c] == None
    
    # def find_anchors(self):
    #     anchors = []
    #     for r in range(self.size):
    #         for c in range(self.size):
    #             if self.get(r,c) is None:
    #                 neighbors = [
    #                     (r-1,c), (r+1,c), (r,c-1), (r,c+1)
    #                 ]
    #                 if any(0 <= nr < self.size and 0 <= nc < self.size and self.get(nr,nc)
    #                     for nr,nc in neighbors):
    #                     anchors.append((r,c))
    #     return anchors

if __name__ == "__main__":
    board = Board()
    line = [' ', ' ', 'a', 'b', ' ', ' ', 'a', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    segments = board.scan_line(line)
    print(segments)