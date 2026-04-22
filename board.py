

class TicTacToe:
    def __init__(self, debug: bool = False):
        """
        Initializes the class with optional debugging mode, prepares the game board,
        and sets up the player tracking.

        :param debug: Indicates whether debugging mode is enabled.
        :type debug: bool
        """
        self.players: dict[int, str] = {}
        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]

        self.debug = debug


    def add_player(self, player_id: int, name: str):
        """
        Adds a new player to the system.

        This method adds a player to the tracking system with the given player ID and name.
        It stores the player in the `players` dictionary and returns the player ID if successfully added.

        :param player_id: The unique identifier for the player.
        :type player_id: int
        :param name: The name of the player to be added.
        :type name: str
        :return: The player ID of the newly added player.
        :rtype: int
        """

        self.players[player_id] = name
        return player_id

    def delete_player(self, player_id: int):
        """
        Deletes a player from the registry by their unique identifier.

        This method checks if the player ID exists in the current players registry
        and removes it if found. If the player ID does not exist, it outputs
        a message indicating that the player is not part of the registry.

        :param player_id: Unique identifier of the player to remove
        :type player_id: int
        :return: None
        """
        if player_id in self.players:
            del self.players[player_id]
        else:
            print("Player not in registry")





    def play(self, player_id, x: int, y: int):
        """
        Updates the game board based on the player's move. This method determines if a player
        can make a move at the specified position and updates the board accordingly. If the position
        has already been claimed by the same player, the action is ignored with a corresponding
        message. If the position is empty, the move is allowed, and the board is updated. If the
        position is occupied by another player, the action is disallowed with a corresponding message.

        :param player_id: The unique identifier of the player making the move.
        :param x: The column index on the game board where the player wants to make a move.
        :param y: The row index on the game board where the player wants to make a move.
        :return: None
        """
        current_item = self.board[y][x]

        if current_item == player_id:
            print("You already claimed that box")

        elif current_item == 0:
            self.board[y][x] = player_id

        else:
            print("You cannot go there")

    def who_won(self) -> list:
        """
        Determines which players have won based on the game's win condition.

        The function iterates through the list of players and checks each player
        against the game's win condition using the `did_win` method. If a player
        has met the win condition, they are added to a list of winners. The function
        then returns this list of winning players.

        :return: A list of players who have won based on the game's win condition.
        :rtype: list
        """
        winners = []
        for player in self.players:
            if self.did_win(player):
                winners.append(player)

        return winners

    def did_win(self, player) -> bool:
        """
        Evaluates whether the given player has won the game by checking all possible
        win conditions (rows, columns, and diagonals) on the board.

        :param player: The player identifier being checked for a win.
        :type player: Any
        :return: A boolean value indicating whether the player has won the game.
        :rtype: bool
        """
        for y in range(len(self.board)):
            if self.__row_check(player, y):
                return True

        for x in range(len(self.board[0])):
            if self.__column_check(player, x):
                return True

        if self.__diagonal_check(player):
            return True

        else:
            return False



    def __diagonal_check(self, player_id):
        """
        Checks if there is a diagonal win condition for the given player in the current
        state of the game board.

        This function evaluates both the main diagonal (top-left to bottom-right) and
        the anti-diagonal (top-right to bottom-left) of the board to determine if all
        positions in either diagonal are occupied by the specified player's identifier.

        :param player_id: The identifier of the player to check for a diagonal win.
        :type player_id: Any
        :return: True if all positions in one of the diagonals are occupied by the
            specified player's identifier, otherwise False.
        :rtype: bool
        """

        for y in range(len(self.board)):

            if self.board[y][y] != player_id and self.board[y][len(self.board)-1-y] != player_id:
                return False

        return True

    def __row_check(self,player_id, y: int):
        """
        Checks if all entries in a specified row are occupied by the given player.

        This method verifies if every element in the row index `y` of the game
        board matches the provided `player_id`. If any entry is empty or belongs
        to a different player, the method will return ``False``.

        :param player_id: The identifier of the player to check for.
        :type player_id: int
        :param y: The index of the row to check.
        :return: ``True`` if all elements in the row belong to the given player,
            otherwise ``False``.
        :rtype: bool
        """

        row = self.board[y]

        for item in row:
            if item == 0 or item != player_id:
                return False


        return True

    def __column_check(self, player_id, x: int):




        for y in range(len(self.board)):
            current_value = self.board[y][x]

            if current_value == 0 or current_value != player_id:
                return False

        return True




    def __repr__(self):
        f_str = ""
        for row in self.board:
            f_str += str(row) + "\n"

        return f_str

    def __str__(self):
        return self.__repr__()


    def log(self, msg:str, end: str = "\n"):
        if self.debug:
            print(msg, end=end)