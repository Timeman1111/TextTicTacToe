

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

        if current_item != 0:
            if current_item == player_id:
                print("You already claimed that box")
            else:
                print("You cannot go there")
            return

        self.board[y][x] = player_id

    def who_won(self) -> list:
        # Optimized to scan board once
        winners = []
        size = len(self.board)
        
        # Check rows
        for row in self.board:
            first = row[0]
            if first != 0 and all(cell == first for cell in row):
                if first not in winners: winners.append(first)
                
        # Check columns
        for x in range(size):
            first = self.board[0][x]
            if first != 0 and all(self.board[y][x] == first for y in range(size)):
                if first not in winners: winners.append(first)
                
        # Check diagonals
        first_main = self.board[0][0]
        if first_main != 0 and all(self.board[i][i] == first_main for i in range(size)):
            if first_main not in winners: winners.append(first_main)
            
        first_anti = self.board[0][size - 1]
        if first_anti != 0 and all(self.board[i][size - 1 - i] == first_anti for i in range(size)):
            if first_anti not in winners: winners.append(first_anti)

        return winners

    def did_win(self, player) -> bool:
        size = len(self.board)
        # Check rows
        if any(all(cell == player for cell in row) for row in self.board):
            return True
        # Check columns
        if any(all(self.board[y][x] == player for y in range(size)) for x in range(size)):
            return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(size)):
            return True
        if all(self.board[i][size - 1 - i] == player for i in range(size)):
            return True

        return False







    def __repr__(self):
        return "\n".join(str(row) for row in self.board)

    def __str__(self):
        return self.__repr__()


    def log(self, msg:str, end: str = "\n"):
        if self.debug:
            print(msg, end=end)