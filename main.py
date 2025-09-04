from utils.dictionary import DictionaryBuilder
from utils.board import Board

def extend_word_full(dictionary, board, hand):
    """
    Scan the board and return all valid words formed using hand + board letters.

    Returns:
        List of tuples: (word, used_positions)
        used_positions = [(row, col, letter), ...] for letters from hand
    """
    results = []
    rows, cols = len(board), len(board[0])

    directions = [(0, 1), (1, 0)]  # horizontal, vertical

    # --- Helper: Scan a single line into slots ---
    def scan_slots(line):
        """
        Returns list of slots. Each slot is a list of positions in the line.
        A slot is contiguous letters + empty squares.
        """
        slots = []
        start = None
        for i, cell in enumerate(line):
            if cell != Board.EMPTY or (start is not None):
                if start is None:
                    start = i
            else:
                if start is not None:
                    slots.append(list(range(start, i)))
                    start = None
        if start is not None:
            slots.append(list(range(start, len(line))))
        return slots

    # --- Helper: Generate words recursively along a slot ---
    def generate_words(slot_positions, prefix="", used_positions=None, hand_letters=None):
        if used_positions is None:
            used_positions = []
        if hand_letters is None:
            hand_letters = hand

        # Stop if prefix cannot be extended
        if not dictionary.can_extend(prefix):
            return []

        local_results = []
        if prefix and dictionary.is_word(prefix):
            local_results.append((prefix, used_positions.copy()))

        # Move to next position
        if not slot_positions:
            return local_results

        r, c = slot_positions[0]
        rest_positions = slot_positions[1:]
        cell = board[r][c]

        if cell == Board.EMPTY:
            # Try every letter from hand
            for i, letter in enumerate(hand_letters):
                next_hand = hand_letters[:i] + hand_letters[i+1:]
                next_used = used_positions + [(r, c, letter)]
                local_results += generate_words(rest_positions, prefix + letter, next_used, next_hand)
        else:
            # Use existing board letter
            local_results += generate_words(rest_positions, prefix + cell, used_positions, hand_letters)

        return local_results

    # --- Scan rows ---
    for r in range(rows):
        line = board[r]
        slots = scan_slots(line)
        for slot in slots:
            slot_positions = [(r, c) for c in slot]
            results += generate_words(slot_positions)

    # --- Scan columns ---
    for c in range(cols):
        line = [board[r][c] for r in range(rows)]
        slots = scan_slots(line)
        for slot in slots:
            slot_positions = [(r, c) for r in slot]
            results += generate_words(slot_positions)

    return results

def check_cross_word(dictionary, board, r, c, dr, dc, letter):
    """
    Returns True if the perpendicular word formed by placing `letter` at (r,c) is valid.
    dr, dc: direction of the main word
    """
    rows, cols = len(board), len(board[0])
    if dr == 0:  # horizontal main word -> check vertical cross
        start_r = r
        while start_r > 0 and board[start_r-1][c] != Board.EMPTY:
            start_r -= 1
        end_r = r
        while end_r < rows-1 and board[end_r+1][c] != Board.EMPTY:
            end_r += 1
        # build the cross word
        word = ""
        for row in range(start_r, end_r+1):
            if row == r:
                word += letter
            else:
                word += board[row][c]
        return dictionary.is_word(word)
    elif dc == 0:  # vertical main word -> check horizontal cross
        start_c = c
        while start_c > 0 and board[r][start_c-1] != Board.EMPTY:
            start_c -= 1
        end_c = c
        while end_c < cols-1 and board[r][end_c+1] != Board.EMPTY:
            end_c += 1
        word = ""
        for col in range(start_c, end_c+1):
            if col == c:
                word += letter
            else:
                word += board[r][col]
        return dictionary.is_word(word)
    return True  # single letters with no neighbors are ok





def main():
    dictionary = DictionaryBuilder().get_or_build()
    board = Board(5, 5)

    board.place_word("cat", 1, 0, 0, 1) 
    board.place_word("hey", 4, 1, 0, 1) 


    hand = "chaty"

    r_start, c_start = 0, 1
    dr, dc = 1, 0  # vertical

    if dr != 0:
        print(f"Searching vertically starting at column {c_start}")
    elif dc != 0:
        print(f"Searching horizontally starting at row {r_start}")

    # results = extend_word(dictionary, board.grid, hand, r_start, c_start, dr, dc)
    results = extend_word_full(dictionary, board.grid, hand)

    print("Hand:", hand)
    print("Board:\n", board)
    print(results)

if __name__ == "__main__":
    main()