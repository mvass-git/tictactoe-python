from models import GameLobby
commands = {}

lobbies = []
clients = []

def command(func):
    def wrapper(cmd_name):
        commands[cmd_name] = func
        return func
    return wrapper

@command("create_or_join")
def create_or_join(id):
    for l in lobbies:
        if l.is_full():
            continue
        l.add_player(id)
        return {"type":"start_game"}
    l = GameLobby()
    l.add_player(id)
    lobbies.append(l)
    return {"type":"wait_for_game"}

@command("make_turn")
def make_turn(id):
    pass

@command("leave_lobby")
def leave_lobby(id):
    pass