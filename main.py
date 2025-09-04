from utils.dictionary import DictionaryBuilder
from utils.board import Board

def extend_word(dictionary, board, hand, r, c, dr, dc, prefix="", used_positions=None):
    """
    dictionary: your dictionary tree
    board: 2D board
    hand: letters available
    r, c: starting coordinates
    dr, dc: direction delta (1,0)=down, (0,1)=right
    prefix: current word being formed
    used_positions: track which tiles we placed from hand
    """
    if used_positions is None:
        used_positions = []

    if not dictionary.can_extend(prefix):
        # print(f"Prefix {prefix} is invalid")
        return []

    results = []
    if dictionary.is_word(prefix):
        results.append((prefix, used_positions.copy()))
    
    r_next, c_next = r + dr, c + dc
    if 0 <= r_next < len(board) and 0 <= c_next < len(board[0]):
        if board[r_next][c_next] == Board.EMPTY:
            for i, letter in enumerate(hand):
                hand_next = hand[:i] + hand[i+1:]
                used_positions_next = used_positions + [(r_next, c_next, letter)]
                # print(f"Trying letter '{letter}' at ({r_next}, {c_next}), prefix so far: '{prefix}'")
                results += extend_word(dictionary, board, hand_next, r_next, c_next, dr, dc, prefix + letter, used_positions_next)
        else:
            # print(f"Using board letter '{board[r_next][c_next]}' at ({r_next}, {c_next}), prefix so far: '{prefix}'")
            results += extend_word(dictionary, board, hand, r_next, c_next, dr, dc, prefix + board[r_next][c_next], used_positions)
    return results


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

    results = extend_word(dictionary, board.grid, hand, r_start, c_start, dr, dc)

    print("Hand:", hand)
    print("Board:\n", board)
    print(results)

if __name__ == "__main__":
    main()