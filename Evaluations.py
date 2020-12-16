import numpy as np

def row_win(board, player):
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[x][y] != player:
                win = False
                continue

        if win == True:
            return (win)
    return (win)

def col_win(board, player):
    for x in range(len(board)):
        win = True

        for y in range(len(board)):
            if board[y][x] != player:
                win = False
                continue

        if win == True:
            return (win)
    return (win)

def diag_win(board, player):
    win = True
    y = 0
    for x in range(len(board)):
        if board[x][x] != player:
            win = False
    if win:
        return win
    win = True
    if win:
        for x in range(len(board)):
            y = len(board) - 1 - x
            if board[x][y] != player:
                win = False
    return win

def evaluate(board):
    winner = 0

    for player in [1, 2]:
        if (row_win(board, player) or
                col_win(board, player) or
                diag_win(board, player)):
            winner = player

    winner_player = 'X' if winner == 1 else 'O'

    if np.all(board != 0) and winner == 0:
        winner_player = -1

    return winner_player

def player_score(state):
    if evaluate(state) == 'O':
        score = +1
    elif evaluate(state) == 'X':
        score = -1
    else:
        score = 0

    return score

