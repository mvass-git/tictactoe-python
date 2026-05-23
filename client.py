from kivy.app import App

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

import json
import threading
import socket

import traceback

from kivy.lang import Builder
Builder.load_file("ui.kv")

class Connector:
    HOST, PORT = "127.0.0.1", 320

    def __init__(self):
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
            except:
                print(traceback.format_exc)

class BoardCell(Button):
    pass

class MenuScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        board = self.ids.grid_board
        board.cols = 3
        board.rows = 3
        for i in range(9):
            board.add_widget(
                BoardCell()
            )

class TicTacToeApp(App):
    def __init__(self, **kw):
        super().__init__(**kw)

    def build(self):
        self.sm = ScreenManager()
        
        self.game = GameScreen()
        self.sm.add_widget(self.game)
        return self.sm
TicTacToeApp().run()