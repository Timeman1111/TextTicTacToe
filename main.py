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

        self.running = False

    def __add_players(self):

        self.board.add_player(1, 'Player 1')
        self.board.add_player(2, 'Player 2')

    def player_turn(self, player_id: int):



        if player_id not in self.board.players:
            print(f"Player with id {player_id} not in registry")
            return

        name = self.board.players[player_id]


        print(f"\n\n{name}'s Turn", end="\n")


        x, y = self.get_player_input()



        self.board.play(player_id, x, y)


    def get_player_input(self):



        def get_int(prompt: str):
            while True:
                try:
                    return int(input(prompt))
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

        mx = len(self.board.board)
        x: int = get_int(f"Enter Column (1 - {mx}): ") - 1
        y: int = get_int(f"Enter Height (1 - {mx}): ") - 1

        return x, y

    def round(self, player_id: int):
        clear()
        self.show_board()
        self.player_turn(player_id=player_id)

        if self.board.did_win(player_id):
            print(f"Player {player_id} won!")
            return True


    def play(self):
        self.__add_players()
        self.running = True
        while self.running:
            p1 = self.round(player_id=1)

            if p1:
                break


            p2 = self.round(player_id=2)

            if p2:
                break




    def show_board(self):
        self.renderer.render_board(x=self.x, y=self.y, board=self.board)



def clear():
    print("\033[2J", end="")


if __name__ == '__main__':
    clear()
    game = ToeGame()
    game.play()
