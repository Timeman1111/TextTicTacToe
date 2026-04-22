

class TicTacToe:
    def __init__(self, debug: bool = False):

        self.players: dict[int, str] = {}
        self.board = [[0,0,0],
                      [0,0,0],
                      [0,0,0]]

        self.debug = debug


    def add_player(self, player_id: int, name: str):
        self.players[player_id] = name
        return player_id

    def delete_player(self, player_id: int):
        if player_id in self.players:
            del self.players[player_id]
        else:
            print("Player not in registry")





    def play(self, player_id, x: int, y: int):

        current_item = self.board[y][x]

        if current_item == player_id:
            print("You already claimed that box")

        elif current_item == 0:
            self.board[y][x] = player_id

        else:
            print("You cannot go there")

    def who_won(self) -> list:
        winners = []
        for player in self.players:
            if self.did_win(player):
                winners.append(player)

        return winners

    def did_win(self, player) -> bool:


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
        for y in range(len(self.board)):

            if self.board[y][y] != player_id and self.board[y][len(self.board)-1-y] != player_id:
                return False

        return True

    def __row_check(self,player_id, y: int):

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