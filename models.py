class GameLobby:
    def __init__(self):
        self.pX = None
        self.pO = None

        self.current_p = "X"

        self.board = [[None, None, None] for i in range(3)]
        self.is_finished = False
    
    def is_full(self):
        return self.pX and self.pO
    
    def broadcast(self, msg, excluded_player=None):
        from routing import send_by_id

        if self.pX != excluded_player:
            send_by_id(self.pX, msg)
        if self.pO != excluded_player:
            send_by_id(self.pO, msg)
    
    def start_game(self):
        from routing import send_by_id

        msgX = {
            "type":"start_game",
            "symbol":"X"
        }

        msgO = {
            "type":"start_game",
            "symbol":"O"
        }
        send_by_id(self.pX, msgX)
        send_by_id(self.pO, msgO)

    def add_player(self, player):
        if self.pX == player or self.pO == player:
            return

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
                self.is_finished = True
                return row[0]
        for i in range(len(self.board)):
            if (self.board[0][i] == self.board[1][i] and 
                self.board[1][i] == self.board[2][i] 
                and self.board[0][i]):
                self.is_finished = True
                return self.board[0][i]
        
        if (((self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]) or
            (self.board[0][2] == self.board[1][1] and self.board[1][1] == self.board[2][0]))
            and self.board[1][1]):
            self.is_finished = True
            return self.board[1][1]

    def is_draw(self):
        for row in self.board:
            for cell in row:
                if not cell:
                    return
        self.is_finished = True
        return 1
    
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
        winner = self.check_winner()
        if winner:
            self.broadcast(self.get_state())
            self.broadcast({
                "type":"finish_game",
                "winner":winner
            })
            return 1
        if self.is_draw():
            self.broadcast(self.get_state())
            self.broadcast({
                "type":"finish_game",
                "winner":"Draw"
            })
            return 1
        self.current_p = "X" if self.current_p == "O" else "O"

        self.broadcast(self.get_state())
        return 1
    
    def get_state(self):
        return {
            "type":"state",
            "board":self.board,
            "current_turn":self.current_p
        }
        
        

