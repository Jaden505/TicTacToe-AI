from random import randrange
from math import inf as infinity

from Evaluations import row_win, col_win, diag_win, evaluate, player_score

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

class AI:
    def __init__(self):
        self.player = 2

    def gameOver(self, m_bord, depth):
        if any([col_win(m_bord, self.player),
                row_win(m_bord, self.player),
                diag_win(m_bord, self.player)]) or depth == 0:
            return True
        else:
            return False

    def emptyCells(self, board):
        cells = []

        for x, row in enumerate(board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        depth = len(cells)

        return cells, depth

    def minimax(self, board, empty_cells, depth):
        if self.player == 2:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if self.gameOver(board, depth):
            score = player_score(board)
            return [-1, -1, score]

        for cell in self.emptyCells(board)[0]:
            x, y = cell[0], cell[1]
            board[x][y] = self.player
            self.player = 2 if self.player == 1 else 1
            score = self.minimax(board, empty_cells, depth-1)
            board[x][y] = 0
            score[0], score[1] = x, y

            if self.player == 2:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

if __name__ == '__main__':
    brd = randBoard()
    # brd = [[0, 0, 0], [1, 2, 0], [1, 2, 0]]
    print(brd)
    bot = AI()
    ecs, d = bot.emptyCells(brd)
    b = bot.minimax(brd, ecs, d)
    print(b)

