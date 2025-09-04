class Board:
    def __init__(self, size=15):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
    
    def place_tile(self, r, c, letter):
        self.grid[r][c] = letter
    
    def get(self, r, c):
        return self.grid[r][c]
    
    def is_empty(self, r, c):
        return self.grid[r][c] == None
    
    def find_anchors(self):
        anchors = []
        for r in range(self.size):
            for c in range(self.size):
                if self.get(r,c) is None:
                    neighbors = [
                        (r-1,c), (r+1,c), (r,c-1), (r,c+1)
                    ]
                    if any(0 <= nr < self.size and 0 <= nc < self.size and self.get(nr,nc)
                        for nr,nc in neighbors):
                        anchors.append((r,c))
        return anchors