"""Entry point for the text-based TicTacToe game."""
from board import TicTacToe
from board_render import BoardRenderer
from term_utils import init_terminal


class ToeGame:
    """Manages a single TicTacToe game session, including player turns and rendering."""

    def __init__(self, size: int = 3, tx: int = 1, ty: int = 1, t_scale: int = 1):
        """Initialize the game with board size and terminal render position/scale."""
        self.x = tx
        self.y = ty
        self.scale = t_scale
        self.board = TicTacToe(size)
        self.renderer = BoardRenderer(scale=self.scale)

        self.running = False

    def __add_players(self):
        self.board.add_player(1, 'Player 1')
        self.board.add_player(2, 'Player 2')

    def player_turn(self, player_id: int):
        """Execute one turn for the given player, handling invalid input."""
        if player_id not in self.board.players:
            print(f"Player with id {player_id} not in registry")
            return

        name = self.board.players[player_id]

        print(f"\n\n{name}'s Turn", end="\n")

        x, y = self.get_player_input()

        if self.board.is_occupied(x, y):
            print("That spot is already taken")
            self.player_turn(player_id)
            return

        self.board.play(player_id, x, y)

    def get_player_input(self):
        """Prompt the current player to enter valid board coordinates."""

        def get_int(prompt: str):
            while True:
                try:
                    return int(input(prompt))
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

        def is_within(value: int, mx: int, mn: int):
            return mn <= value <= mx

        x: int = get_int(f"Enter Column (1 - {self.board.size}): ")
        y: int = get_int(f"Enter Height (1 - {self.board.size}): ")

        if not is_within(x, self.board.size, 1) or not is_within(y, self.board.size, 1):
            print(f"Invalid input. Please enter a value between 1 and {self.board.size}.")
            # Could cause a recursion error if player keeps entering invalid input
            return self.get_player_input()

        return x - 1, y - 1

    def round(self, player_id: int) -> bool | None:
        """Play one round for the given player; return True if the game is over."""
        clear()
        self.show_board()
        self.player_turn(player_id=player_id)

        if self.board.did_win(player_id) or self.board.is_draw:
            return True

        return None

    def play(self):
        """Run the main game loop until a player wins or the board is full."""
        self.__add_players()
        self.running = True
        while self.running:
            p1 = self.round(player_id=1)

            if p1:
                break

            p2 = self.round(player_id=2)

            if p2:
                break

            if self.board.all_full:
                break

        clear()
        self.show_board()
        print("\n\nGame Over!")

        if self.board.is_draw:
            print("It's a draw!")

        else:

            players = self.board.who_won()

            print(f"{self.board.players[players[0]]} won!")

    def show_board(self):
        """Render the current board state to the terminal."""
        self.renderer.render_board(x=self.x, y=self.y, board=self.board)


def clear():
    """Clear the terminal screen."""
    print("\033[2J", end="")


def run_game():
    """Initialize the terminal and start a new game."""
    init_terminal()
    clear()
    game = ToeGame()
    game.play()


if __name__ == '__main__':

    while True:
        run_game()
        print("Press Enter to play again or Ctrl+C to exit.")
        try:
            input()
        except KeyboardInterrupt:
            print("Exiting...")

            break
