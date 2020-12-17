from random import randrange
from math import inf as infinity

from Evaluations import row_win, col_win, diag_win, evaluate, player_score

HUMAN = +1  # On board == 1 MAXIMIZER
COMP = -1   # On board == 2 MINIMIZER

scores = []

def randBoard():
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    turn = 1  # X starts

    for i in range(randrange(4)):
        for j in range(randrange(4)):
            if board[i][j] == 0:
                board[i][j] = turn
                turn = 2 if turn == 1 else 1

    return board

def gameOver(board, depth):
    if evaluate(board) != -1 or depth == 0:
        return True
    else:
        return False

def emptyCells(board):
    cells = []

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    depth = len(cells)

    return cells, depth

def minimax(board, depth, player):
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if gameOver(board, depth):
        score = player_score(board)
        return [-1, -1, score]

    for cell in emptyCells(board)[0]:
        x, y = cell[0], cell[1]
        if player == COMP:
            board[x][y] = 2
        else:
            board[x][y] = 1
        score = minimax(board, depth-1, -player)
        # print(score)
        board[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    scores.append(best)

    return best

if __name__ == '__main__':
    brd = randBoard()
    player = COMP
    # brd = [[0, 2, 0], [1, 2, 0], [1, 0, 0]]
    print(brd)
    # bot = AI()
    ecs, d = emptyCells(brd)
    b = minimax(brd, d, player)
    print(b)
