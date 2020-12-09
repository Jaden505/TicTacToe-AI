from random import randrange
import copy

from Evaluations import row_win, col_win, diag_win, evaluate

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

    def __init__(self, board):
        self.board = board
        self.player = 2
        self.score_O = 0    # Needs to get as high as possible 2
        self.turn = True

    def checkWin(self, m_bord):
        if any([col_win(m_bord, self.player),
                row_win(m_bord, self.player),
                diag_win(m_bord, self.player)]):
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

    def minimax(self, empty_cells, depth):
        all_cell_values = {}
        all_possibilities = []
        all_wins = []

        for c in empty_cells:
            m_bord = copy.deepcopy(self.board)

            m_bord[c[0]][c[1]] = self.player

            if self.checkWin(m_bord):
                all_wins.append(m_bord)
                if evaluate(m_bord) == 'O':
                    self.score_O += 1
                else:
                    self.score_O -= 1
            else:
                all_possibilities.append(m_bord)

            self.player = 2 if self.player == 1 else 1

            for i in range(depth):
                vals = [b for b in all_possibilities if [item for sublist in b for item in sublist].count(0) == depth-i]
                for b in vals:
                    ec, d = self.emptyCells(b)

                    for cell in ec:
                        b_copy = copy.deepcopy(b)

                        b_copy[cell[0]][cell[1]] = self.player

                        if self.checkWin(b_copy):
                            all_wins.append(b_copy)
                            if evaluate(m_bord) == 'O':
                                self.score_O += 1
                            else:
                                self.score_O -= 1
                        else:
                            all_possibilities.append(b_copy)

                    self.player = 2 if self.player == 1 else 1

            all_cell_values[c[0], c[1]] = self.score_O

            all_possibilities = []
            all_wins = []
            self.score_O = 0

        # print(all_cell_values)
        max_points_move = max(all_cell_values.values())
        best_move = list(all_cell_values.keys())[list(all_cell_values.values()).index(max_points_move)]

        print(best_move)

        return best_move

        # if self.board[best_move[0]][best_move[1]] == 0:
        #     print(best_move)
        #
        #     return best_move
        # else:
        #     for i in range(len(all_cell_values.values())):
        #         max_points_move = sorted(all_cell_values.values())[-i]
        #         best_move = list(all_cell_values.keys())[list(all_cell_values.values()).index(max_points_move)]
        #
        #         if self.board[best_move[0], best_move[1]] == 0:
        #             print(best_move)
        #
        #             return best_move

if __name__ == '__main__':
    board = randBoard()
    bot = AI(board)
    print(board)
    empty_cells, depth = bot.emptyCells(board)
    bot.minimax(empty_cells, depth)
