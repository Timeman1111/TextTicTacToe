from board import TicTacToe
from board_render import BoardRenderer

import os






def clear():
    print("\033[2J", end="\033[0;0H")


if __name__ == '__main__':
    clear()
    term_size = os.get_terminal_size()
    scale = 1
    lines, columns = term_size.lines, term_size.columns

    x = columns // 2 - 1
    y = lines // 2 - 1


    clear()
    b = TicTacToe(True)
    render = BoardRenderer(scale = scale)

    # Add players
    b.add_player(1, 'Player 1')
    b.add_player(2, 'Player 2')


    b.play(1, x=0, y=0)
    b.play(1, x=1, y=1)
    b.play(1, x=2, y=2)
    render.render_board(board=b, x=x, y=y)

