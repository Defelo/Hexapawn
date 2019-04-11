from typing import List, Tuple

BOARD = List[List[int]]
MOVE = Tuple[Tuple[int, int], Tuple[int, int]]


def possible_player_moves(state: BOARD) -> List[MOVE]:
    out: List[MOVE] = []
    for i in range(2, 0, -1):
        for j in range(3):
            if not 0 < state[i][j] < 7:
                continue
            if 0 < j and state[i - 1][j - 1] == 7:
                out.append(((i, j), (i - 1, j - 1)))
            if state[i - 1][j] == 0:
                out.append(((i, j), (i - 1, j)))
            if j < 2 and state[i - 1][j + 1] == 7:
                out.append(((i, j), (i - 1, j + 1)))
    return out


def possible_computer_moves(state: BOARD) -> List[MOVE]:
    out: List[MOVE] = []
    for i in range(2):
        for j in range(3):
            if state[i][j] != 7:
                continue
            if 0 < j and 0 < state[i + 1][j - 1] < 7:
                out.append(((i, j), (i + 1, j - 1)))
            if state[i + 1][j] == 0:
                out.append(((i, j), (i + 1, j)))
            if j < 2 and 0 < state[i + 1][j + 1] < 7:
                out.append(((i, j), (i + 1, j + 1)))
    return out


def apply_move(state: BOARD, move: MOVE):
    (i, j), (p, q) = move
    state[p][q] = state[i][j]
    state[i][j] = 0


def check_win(state: BOARD, computers_turn: bool) -> int:
    if any(x in state[0] for x in (1, 2, 3)):
        return 1
    if 7 in state[2]:
        return 2
    if not any(7 in l for l in state):
        return 1
    if not any(x in l for l in state for x in (1, 2, 3)):
        return 2
    if computers_turn and not possible_computer_moves(state):
        return 1
    if not computers_turn and not possible_player_moves(state):
        return 2
    return 0


def stringify_board(state: BOARD) -> List[str]:
    return [" ".join(str(c) for c in row) for row in state]


def print_board(state: BOARD):
    for row in stringify_board(state):
        print(row)


def show_possible_moves(state: BOARD) -> List[MOVE]:
    moves: List[str] = stringify_board(state)
    width: int = max(map(len, moves))
    height: int = len(moves)
    moves[height // 2] = moves[height // 2].ljust(width) + "  ->  "
    for i in range(height):
        moves[i] = moves[i].ljust(width + 6)

    possible_moves: List[MOVE] = possible_player_moves(state)
    for i, move in enumerate(possible_moves):
        s: BOARD = [[*l] for l in state]
        apply_move(s, move)
        for j, row in enumerate(stringify_board(s)):
            moves[j] += ["   ", f"{i + 1}) "][j == 0] + row.ljust(width + 4)

    for row in moves:
        print(row)

    return possible_moves


def game():
    board = [
        [7, 7, 7],
        [0, 0, 0],
        [1, 2, 3]
    ]
    while True:
        moves: List[MOVE] = show_possible_moves(board)
        move: str = input(">> ")
        if move.lower() in ["q", "exit", "quit"]:
            exit()
        if not move.isnumeric():
            continue
        move: int = int(move) - 1
        if not 0 <= move <= 2:
            continue
        apply_move(board, moves[move])
        winner: int = check_win(board, True)
        if winner:
            print_board(board)
            print(["Player", "Computer"][winner - 1], " wins the game!")
            break


if __name__ == '__main__':
    game()
