class GameLobby:
    def __init__(self):
        self.pX = None
        self.pO = None

        self.current_p = "X"

        self.board = [[None, None, None] for i in range(3)]
        self.is_finished = False

    def add_player(self, player):
        if not self.pX:
            self.pX = player
            return
        if not self.pO:
            self.pO = player
            return
        return
    
    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] and row[1] == row[2] and row[0]:
                return row[0]
        for i in range(len(self.board)):
            if (self.board[0][i] == self.board[1][i] and 
                self.board[1][i] == self.board[2][i] 
                and self.board[0][i]):
                return self.board[0][i]
        
        if ((self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]) or
            (self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]) and self.board[1][1]):
            return self.board[1][1]
    
    def get_symbol(self, player_id):
        if self.pX == player_id:
            return "X"
        elif self.pO == player_id:
            return "O"
        else:
            return

    def make_turn(self, player_id, pos):
        row, col = pos
        if self.board[row][col]:
            return
        if self.current_p != self.get_symbol(player_id):
            return
        
        if self.is_finished:
            return
        
        self.board[row][col] = self.get_symbol(player_id)

        if self.check_winner():
            return
        self.current_p = "X" if self.current_p == "O" else "O"
        
        

