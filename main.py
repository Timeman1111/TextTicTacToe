from board import TicTacToe
from board_render import BoardRenderer

import os


class ToeGame:
    def __init__(self, tx: int = 1, ty: int = 1, t_scale: int = 1):

        self.x = tx
        self.y = ty
        self.scale = t_scale
        self.board = TicTacToe()
        self.renderer = BoardRenderer(scale=self.scale)

    def __add_players(self):

        self.board.add_player(1, 'Player 1')
        self.board.add_player(2, 'Player 2')

    def play(self):
        self.__add_players()
        while True:
            clear()
            self.renderer.render_board(x=self.x, y=self.y, board=self.board)

            print("\nPlayer 1 Turn", end="\n")
            X = input("X: ")

            try:
                x = int(X)


            except ValueError:
                print(f"Invalid X: {X}")
                continue



            Y = input("Y: ")

            try:
                y = int(Y)

            except ValueError:
                print(f"Invalid Y: {Y}")
                continue

            self.board.play(1, int(x), int(Y))



def clear():
    print("\033[2J", end="")


if __name__ == '__main__':
    clear()
    game = ToeGame()
    game.play()
