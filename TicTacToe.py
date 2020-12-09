import sys
from PyQt5.QtWidgets import *
from functools import partial

from Evaluations import row_win, col_win, diag_win, evaluate
from TicTacToeAI import AI

class TTT:

    def __init__(self, app):
        self.app = app
        self.moves = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    def screen(self):
        self.win = QWidget()
        self.win.setGeometry(200,200,300,300)
        self.win.setWindowTitle('Tic tac toe')
        self.turn = 'X'

        self.win.show()

    def board(self):
        self.layout = QGridLayout()

        for i in range(3):
            for j in range(3):
                btn = QPushButton('')
                self.layout.addWidget(btn, i, j)
                btn.clicked.connect(partial(self.click, btn))
                btn.setMinimumSize(100,100)

        self.win.setLayout(self.layout)

    def click(self, btn):
        btn.setText(self.turn)
        btn.clicked.disconnect()

        idx = self.layout.indexOf(btn)
        loc = self.layout.getItemPosition(idx)[:2]

        self.moves[loc[0]][loc[1]] = 1

        check = self.check()

        if not check:
            self.turn = 'O' if self.turn == 'X' else 'X'

            self.bot()

    def check(self):
        player = 1 if self.turn == 'X' else 2

        if any([col_win(self.moves, player),
        row_win(self.moves, player),
        diag_win(self.moves, player)])\
        or sum(self.moves, []).count(0) == 0:

            # Disable buttons
            for i in reversed(range(self.layout.count())):
                try: self.layout.itemAt(i).widget().disconnect()
                except Exception: pass
            # Show winner
            if sum(self.moves, []).count(0) == 0:
                self.label_winner = QLabel("It's a tie.")
            else:
                self.label_winner = QLabel(f'The winner is {evaluate(self.moves)}', self.win)
            self.label_winner.move(300, 150)
            self.layout.addWidget(self.label_winner)
            # Rest button
            self.reset = QPushButton('Reset')
            self.reset.clicked.connect(self.restart)
            self.layout.addWidget(self.reset)

            return True
        return False

    def bot(self):
        bot = AI(self.moves)
        empty_cells, depth = bot.emptyCells(self.moves)
        move = bot.minimax(empty_cells, depth)
        ind = ((move[0] * 3) + (move[1] + 1))-1

        btn = self.layout.itemAt(ind).widget()
        btn.setText(self.turn)
        self.moves[move[0]][move[1]] = 2

        self.check()

        self.turn = 'O' if self.turn == 'X' else 'X'

    def restart(self):
        self.turn = 'X'
        self.moves = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        # Remove winner and reset button
        self.layout.removeWidget(self.label_winner)
        self.layout.removeWidget(self.reset)
        self.label_winner.setVisible(False)
        self.reset.setVisible(False)

        for i in reversed(range(self.layout.count())):
            btn = self.layout.itemAt(i).widget()
            btn.clicked.connect(partial(self.click, btn))
            btn.setText('')

if __name__ == '__main__':
    app = QApplication(sys.argv) # Start
    game = TTT(app)
    game.screen()
    game.board()
    sys.exit(app.exec()) # Loop
