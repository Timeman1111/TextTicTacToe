from board import TicTacToe

class BoardRenderer:
    def __init__(self, scale: int =1,):
        self.scale = scale

    def render_board(self, board: TicTacToe, offset_x: int = 0, offset_y: int = 0):


