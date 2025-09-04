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

    # --- Helper: Recursively generate words along a slot ---
    def generate_words(slot_positions, prefix="", used_positions=None, hand_letters=None):
        if used_positions is None:
            used_positions = []
        if hand_letters is None:
            hand_letters = hand

        if not dictionary.can_extend(prefix):
            return []

        local_results = []
        if prefix and dictionary.is_word(prefix):
            local_results.append((prefix, used_positions.copy()))

        if not slot_positions:
            return local_results

        r, c = slot_positions[0]
        rest_positions = slot_positions[1:]
        cell = board[r][c]

        if cell == Board.EMPTY:
            for i, letter in enumerate(hand_letters):
                next_hand = hand_letters[:i] + hand_letters[i+1:]
                next_used = used_positions + [(r, c, letter)]
                local_results += generate_words(rest_positions, prefix + letter, next_used, next_hand)
        else:
            local_results += generate_words(rest_positions, prefix + cell, used_positions, hand_letters)

        return local_results

    # --- Scan rows and columns ---
    for dr, dc in directions:
        if dr == 0:  # horizontal
            for r in range(rows):
                slot_positions = [(r, c) for c in range(cols)]
                # Start recursion at each position in the slot
                for start_idx in range(len(slot_positions)):
                    results += generate_words(slot_positions[start_idx:])
        else:  # vertical
            for c in range(cols):
                slot_positions = [(r, c) for r in range(rows)]
                for start_idx in range(len(slot_positions)):
                    results += generate_words(slot_positions[start_idx:])

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