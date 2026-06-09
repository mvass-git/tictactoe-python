from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

import json
import threading
import socket

import traceback

from kivy.lang import Builder
Builder.load_file("ui.kv")

class Connector:
    HOST, PORT = " 192.168.50.40", 320

    def __init__(self, handler):
        self.handler = handler
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.HOST, self.PORT))

        threading.Thread(target=self.receiever, daemon= True).start()
    
    def receiever(self):
        while True:
            package = self.sock.recv(1024)

            if not package:
                break
            try:
                msg = json.loads(package.decode())
                mtype = msg.get("type")
                self.handler(mtype, msg)
            except:
                print(traceback.format_exc())
    
    def send(self, msg):
        self.sock.sendall(json.dumps(msg).encode())

class BoardCell(Button):
    def __init__(self, row, col, **kwargs):
        self.cell_pos = (row, col)
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.text = f"{self.cell_pos}"
    
    def on_press(self):
        msg = {
            "type":"make_turn",
            "pos":self.cell_pos
        }
        self.app.conn.send(msg)
        return super().on_press()

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
    
    def start_game_query(self):
        msg = {
            "type":"create_or_join",
        }
        self.app.conn.send(msg)
    
    def update_status(self, new_status):
        self.ids.lbl_status.text = new_status
    
    def go_to_game(self):
        self.manager.current = "game"

class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        board = self.ids.grid_board
        board.cols = 3
        board.rows = 3
        for i in range(board.rows):
            for j in range(board.cols):
                board.add_widget(
                    BoardCell(i, j)
                )
    def finish_game(self, winner):
        app = App.get_running_app()
        app.menu.update_status(f"Winner: {winner}")
        self.manager.current = "menu"
        self.leave()

    def leave(self):
        app = App.get_running_app()
        leave_cmd = {
            "type":"leave"
        }
        app.conn.send(leave_cmd)
    
    def prepare_game(self, symbol):
        self.ids.lbl_you.text = "you " +symbol
    
    def update_board(self, board):
        for i in range(len(self.ids.grid_board.children)):
            #self.ids.grid_board.children[i] = board[len(self.ids.grid_board.children)//len(board)][i%len(board)]
            cell = self.ids.grid_board.children[i]
            value = board[cell.cell_pos[0]][cell.cell_pos[1]]
            cell.text = value if value else ""

class TicTacToeApp(App):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.conn = Connector(self.response_handler)


    def build(self):
        self.sm = ScreenManager()
        
        self.game = GameScreen(name = "game")
        self.menu = MenuScreen(name = "menu")
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.game)
        return self.sm
    
    def response_handler(self, mtype, msg):
        if mtype == "wait_for_game":
            Clock.schedule_once(lambda dt: self.menu.update_status("Wait for an opponent."))
        if mtype == "start_game":
            Clock.schedule_once(lambda dt: self.menu.go_to_game())
            Clock.schedule_once(lambda dt: self.game.prepare_game(msg.get("symbol")))
        if mtype == "state":
            Clock.schedule_once(lambda dt: self.game.update_board(msg.get("board")))
        if mtype == "finish_game":
            Clock.schedule_once(lambda dt: self.game.finish_game(msg.get("winner")))
TicTacToeApp().run()