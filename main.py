from utils.dictionary import DictionaryBuilder
from utils.board import Board

def extend_word_full(dictionary, board, hand):
    """
    Returns list of plays:
      (word, used_positions, main_positions, dr, dc)
    - used_positions: [(r, c, letter), ...] tiles from hand
    - main_positions: full positions of the main word in order
    """
    results = []
    seen = set()
    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (1, 0)]  # horizontal, vertical

    def key_of(word, used_positions, dr, dc):
        # Deduplicate by word text, direction, and exact placed coords+letters
        up = tuple(sorted(used_positions))  # sort to avoid perm duplicates
        return (word, up, dr, dc)

    def generate_words(slot_positions, dr, dc, prefix="", used_positions=None,
                       hand_letters=None, main_positions=None,
                       used_board_in_main=False, made_valid_cross=False):
        if used_positions is None:
            used_positions = []
        if hand_letters is None:
            hand_letters = hand
        if main_positions is None:
            main_positions = []

        # Prune by dictionary prefix
        if not dictionary.can_extend(prefix):
            return []

        local_results = []

        # Accept only if:
        #  - is a word
        #  - at least one tile was placed (no zero-placement words)
        #  - anchored: either used a board tile in the main word OR made at least one valid cross
        if prefix and used_positions and (used_board_in_main or made_valid_cross):
            full_positions = []
            if dr == 0:  # horizontal
                r = slot_positions[0][0] if slot_positions else used_positions[0][0]
                # find start col
                start_c = min(p[1] for p in used_positions + main_positions)
                while start_c > 0 and board[r][start_c - 1] != Board.EMPTY:
                    start_c -= 1
                # find end col
                end_c = max(p[1] for p in used_positions + main_positions)
                while end_c < cols - 1 and board[r][end_c + 1] != Board.EMPTY:
                    end_c += 1
                # build positions
                for c in range(start_c, end_c + 1):
                    if (r, c) in {(rp, cp) for rp, cp, _ in used_positions}:
                        letter = next(l for rr, cc, l in used_positions if rr == r and cc == c)
                    elif (r, c) in {(rp, cp) for rp, cp, l in main_positions}:
                        letter = next(l for rr, cc, l in main_positions if rr == r and cc == c)
                    else:
                        letter = board[r][c]
                    full_positions.append((r, c, letter))
            else:  # vertical
                c = slot_positions[0][1] if slot_positions else used_positions[0][1]
                start_r = min(p[0] for p in used_positions + main_positions)
                while start_r > 0 and board[start_r - 1][c] != Board.EMPTY:
                    start_r -= 1
                end_r = max(p[0] for p in used_positions + main_positions)
                while end_r < rows - 1 and board[end_r + 1][c] != Board.EMPTY:
                    end_r += 1
                for r in range(start_r, end_r + 1):
                    if (r, c) in {(rp, cp) for rp, cp, _ in used_positions}:
                        letter = next(l for rr, cc, l in used_positions if rr == r and cc == c)
                    elif (r, c) in {(rp, cp) for rp, cp, l in main_positions}:
                        letter = next(l for rr, cc, l in main_positions if rr == r and cc == c)
                    else:
                        letter = board[r][c]
                    full_positions.append((r, c, letter))

            full_word = "".join(l for _, _, l in full_positions)
            if dictionary.is_word(full_word):
                k = key_of(full_word, used_positions, dr, dc)
                if k not in seen:
                    seen.add(k)
                    local_results.append((full_word, used_positions.copy(), full_positions.copy(), dr, dc))


        if not slot_positions:
            return local_results

        r, c = slot_positions[0]
        rest_positions = slot_positions[1:]
        cell = board[r][c]

        if cell == Board.EMPTY:
            # Try placing each rack letter, validate perpendicular cross immediately
            for i, letter in enumerate(hand_letters):
                cross = get_cross_word(board, r, c, dr, dc, letter)
                # If cross exists (length > 1), it must be valid; if no cross, it's allowed (anchoring is handled separately)
                if cross:
                    cross_word, _ = cross
                    if not dictionary.is_word(cross_word):
                        continue
                    next_made_valid_cross = True
                else:
                    next_made_valid_cross = made_valid_cross

                next_hand = hand_letters[:i] + hand_letters[i+1:]
                next_used = used_positions + [(r, c, letter)]
                next_main_positions = main_positions + [(r, c, letter)]
                local_results += generate_words(
                    rest_positions, dr, dc, prefix + letter,
                    next_used, next_hand, next_main_positions,
                    used_board_in_main, next_made_valid_cross
                )
        else:
            # Consume existing board letter (anchors the play)
            next_prefix = prefix + cell
            next_main_positions = main_positions + [(r, c, cell)]
            local_results += generate_words(
                rest_positions, dr, dc, next_prefix,
                used_positions, hand_letters, next_main_positions,
                True, made_valid_cross
            )

        return local_results

    # Walk every row/column as a slot, start at each index
    for dr, dc in directions:
        if dr == 0:  # horizontal
            for r in range(rows):
                slot_positions = [(r, c) for c in range(cols)]
                for start_idx in range(len(slot_positions)):
                    results += generate_words(slot_positions[start_idx:], dr, dc)
        else:  # vertical
            for c in range(cols):
                slot_positions = [(r, c) for r in range(rows)]
                for start_idx in range(len(slot_positions)):
                    results += generate_words(slot_positions[start_idx:], dr, dc)

    return results




def check_cross_word(dictionary, board, r, c, dr, dc, letter):
    """
    Returns True if placing `letter` at (r,c) in the main word direction (dr,dc)
    creates a valid perpendicular word.
    """
    rows, cols = len(board), len(board[0])
    if dr == 0:  # horizontal main word -> check vertical cross
        start_r = r
        while start_r > 0 and board[start_r - 1][c] != Board.EMPTY:
            start_r -= 1
        end_r = r
        while end_r < rows - 1 and board[end_r + 1][c] != Board.EMPTY:
            end_r += 1

        # if no perpendicular neighbor, it's fine
        if start_r == end_r:
            return True

        # build the vertical word
        word = ""
        for row in range(start_r, end_r + 1):
            if row == r:
                word += letter
            else:
                word += board[row][c]
        return dictionary.is_word(word)

    elif dc == 0:  # main word is vertical → check horizontal cross
        start_c = c
        while start_c > 0 and board[r][start_c - 1] != Board.EMPTY:
            start_c -= 1
        end_c = c
        while end_c < cols - 1 and board[r][end_c + 1] != Board.EMPTY:
            end_c += 1

        if start_c == end_c:
            return True

        word = ""
        for col in range(start_c, end_c + 1):
            if col == c:
                word += letter
            else:
                word += board[r][col]
        return dictionary.is_word(word)

    return True

LETTER_SCORES = {
    **dict.fromkeys(list("AEILNORSTU"), 1),
    **dict.fromkeys(list("DG"), 2),
    **dict.fromkeys(list("BCMP"), 3),
    **dict.fromkeys(list("FHVWY"), 4),
    "K": 5,
    **dict.fromkeys(list("JX"), 8),
    **dict.fromkeys(list("QZ"), 10),
}

def get_cross_word(board, r, c, dr, dc, letter):
    rows, cols = len(board), len(board[0])
    if dr == 0:  # main word horizontal → perpendicular vertical
        start_r = r
        while start_r > 0 and board[start_r - 1][c] != Board.EMPTY:
            start_r -= 1
        end_r = r
        while end_r < rows - 1 and board[end_r + 1][c] != Board.EMPTY:
            end_r += 1
        if start_r == end_r:  # no perpendicular neighbors
            return None
        positions = []
        word = ""
        for row in range(start_r, end_r + 1):
            if row == r:
                word += letter
                positions.append((row, c, letter))
            else:
                word += board[row][c]
                positions.append((row, c, board[row][c]))
        return word, positions

    elif dc == 0:  # main word vertical → perpendicular horizontal
        start_c = c
        while start_c > 0 and board[r][start_c - 1] != Board.EMPTY:
            start_c -= 1
        end_c = c
        while end_c < cols - 1 and board[r][end_c + 1] != Board.EMPTY:
            end_c += 1
        if start_c == end_c:
            return None
        positions = []
        word = ""
        for col in range(start_c, end_c + 1):
            if col == c:
                word += letter
                positions.append((r, col, letter))
            else:
                word += board[r][col]
                positions.append((r, col, board[r][col]))
        return word, positions
    return None



def score_word(word, positions):
    score = 0
    for (_, _, letter) in positions:
        score += LETTER_SCORES.get(letter.upper(), 0)
    return score



def score_play(dictionary, board, word, main_positions, used_positions, dr, dc):
    total = score_word(word, main_positions)

    # Perpendicular words from each placed tile
    for (r, c, letter) in used_positions:
        cross = get_cross_word(board, r, c, dr, dc, letter)
        if not cross:
            continue
        cross_word, cross_positions = cross
        if len(cross_word) > 1 and dictionary.is_word(cross_word):
            total += score_word(cross_word, cross_positions)

    return total


def rank_plays(dictionary, board, plays):
    ranked = []
    for word, used_positions, main_positions, dr, dc in plays:
        score = score_play(dictionary, board, word, main_positions, used_positions, dr, dc)
        ranked.append((word, used_positions, main_positions, dr, dc, score))
    ranked.sort(key=lambda x: x[5], reverse=True)
    return ranked



def main():
    dictionary = DictionaryBuilder().get_or_build()
    board = Board(5, 5)
    board.place_word("cat", 1, 0, 0, 1)
    board.place_word("hey", 4, 1, 0, 1)

    hand = "catcy"

    plays = extend_word_full(dictionary, board.grid, hand)
    ranked = rank_plays(dictionary, board.grid, plays)

    print("Hand:", hand)
    print("Board:\n", board)
    for word, used_positions, main_positions, dr, dc, score in ranked:
        dir_str = "H" if dr == 0 else "V"
        print(f"{word:10} {dir_str} score={score} used={used_positions}")


if __name__ == "__main__":
    main()