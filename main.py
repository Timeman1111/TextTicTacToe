from board import TicTacToe
from board_render import BoardRenderer

def clear():
    print("\033[2J", end="\033[0;0H")


if __name__ == '__main__':
    clear()
    b = TicTacToe(True)
    render = BoardRenderer()

    # Add players
    b.add_player(1, 'Player 1')
    b.add_player(2, 'Player 2')


    b.play(1, x=2, y=0)
    b.play(1, x=1, y=1)
    b.play(1, x=0, y=2)
    render.render_board(board=b, x=1, y=5)

