import random
from typing import List, Tuple

BOARD = List[List[int]]
MOVE = Tuple[Tuple[int, int], Tuple[int, int]]


def copy_board(state: BOARD) -> BOARD:
    return [[*row] for row in state]


def possible_player_moves(state: BOARD) -> List[MOVE]:
    out: List[MOVE] = []
    for i in range(2, 0, -1):
        for j in range(3):
            if state[i][j] != 1:
                continue
            if 0 < j and state[i - 1][j - 1] == 2:
                out.append(((i, j), (i - 1, j - 1)))
            if state[i - 1][j] == 0:
                out.append(((i, j), (i - 1, j)))
            if j < 2 and state[i - 1][j + 1] == 2:
                out.append(((i, j), (i - 1, j + 1)))
    return out


def possible_computer_moves(state: BOARD) -> List[MOVE]:
    out: List[MOVE] = []
    for i in range(2):
        for j in range(3):
            if state[i][j] != 2:
                continue
            if 0 < j and state[i + 1][j - 1] == 1:
                out.append(((i, j), (i + 1, j - 1)))
            if state[i + 1][j] == 0:
                out.append(((i, j), (i + 1, j)))
            if j < 2 and state[i + 1][j + 1] == 1:
                out.append(((i, j), (i + 1, j + 1)))
    return out


def apply_move(state: BOARD, move: MOVE):
    (i, j), (p, q) = move
    state[p][q] = state[i][j]
    state[i][j] = 0


def check_win(state: BOARD, computers_turn: bool) -> int:
    if 1 in state[0]:
        return 1
    if 2 in state[2]:
        return 2
    if not any(2 in l for l in state):
        return 1
    if not any(1 in l for l in state):
        return 2
    if computers_turn and not possible_computer_moves(state):
        return 1
    if not computers_turn and not possible_player_moves(state):
        return 2
    return 0


def stringify_board(state: BOARD) -> List[str]:
    header = ["+" + "-" * 5 + "+"]
    return header + ["|" + " ".join(" +#"[c] for c in row) + "|" for row in state] + header


def print_board(state: BOARD):
    for row in stringify_board(state):
        print("    " + row)


def show_possible_moves(state: BOARD, possible_moves: List[MOVE], numbers: bool, text: str):
    moves: List[str] = stringify_board(state)
    width: int = max(map(len, moves))
    height: int = len(moves)
    moves[height // 2] = moves[height // 2].ljust(width) + "  ->  "
    for i in range(height):
        moves[i] = moves[i].ljust(width + 6)

    for i, move in enumerate(possible_moves):
        s: BOARD = copy_board(state)
        apply_move(s, move)
        for j, row in enumerate(stringify_board(s)):
            if numbers:
                moves[j] += ["   ", f"{i + 1}) "][j == 0]
            moves[j] += row.ljust(width + 4)

    for i, row in enumerate(moves):
        print([" " * len(text), text][i == 0] + row)


memory = {}


def get_computers_move(state: BOARD) -> MOVE:
    board = tuple(i for row in state for i in row)
    if board not in memory:
        memory[board] = possible_computer_moves(state)
    return random.choice(memory[board])


def game() -> bool:
    board = [
        [2, 2, 2],
        [0, 0, 0],
        [1, 1, 1]
    ]
    computer_history: List[Tuple[BOARD, MOVE]] = []
    while True:
        moves: List[MOVE] = possible_player_moves(board)
        show_possible_moves(board, moves, True, "")
        move: str = input(">> ")
        if move.lower() in ["q", "exit", "quit"]:
            exit()
        if not move.isnumeric():
            continue
        move: int = int(move) - 1
        if not 0 <= move < len(moves):
            continue
        apply_move(board, moves[move])
        winner: int = check_win(board, True)
        if winner:
            assert winner == 1
            for i in range(len(computer_history))[::-1]:
                last_state, last_computer_move = computer_history[i]
                stored_moves: List[MOVE] = memory[tuple(j for row in last_state for j in row)]
                stored_moves.remove(last_computer_move)
                if stored_moves:
                    break
            print_board(board)
            print(["Player", "Computer"][winner - 1], "wins the game!")
            return winner == 1

        move: MOVE = get_computers_move(board)
        board_copy: BOARD = copy_board(board)
        show_possible_moves(board, [move], False, "Computer:    ")
        apply_move(board, move)
        winner: int = check_win(board, False)
        if winner:
            assert winner == 2
            memory[tuple(i for row in board_copy for i in row)] = [move]
            print_board(board)
            print(["Player", "Computer"][winner - 1], "wins the game!")
            return winner == 1
        computer_history.append((board_copy, move))


if __name__ == '__main__':
    history: str = ""
    gamenum: int = 1
    while True:
        print("=" * 30, f"Game #{gamenum}", "=" * 30)
        history += "CP"[game()]
        print("History: ", history)
        print("Player:  ", history.count("P"))
        print("Computer:", history.count("C"))
        gamenum += 1
