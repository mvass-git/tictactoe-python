from models import GameLobby
commands = {}

lobbies = []
clients = []

def get_lobby_by_player_id(id):
    for l in lobbies:
        if l.pO == id or l.pX == id:
            return l

def command(cmd_name):
    def wrapper(func):
        commands[cmd_name] = func
        return func
    return wrapper

@command("create_or_join")
def create_or_join(id, **kwargs):
    for l in lobbies:
        if l.is_full():
            continue
        l.add_player(id)
        l.start_game()
        return {"status":"ok"}
    l = GameLobby()
    l.add_player(id)
    lobbies.append(l)
    return {"type":"wait_for_game"}

@command("make_turn")
def make_turn(id, **kwargs):
    pos = kwargs.get("pos")
    if not pos:
        return
    print("POSITION GOT: ", pos)
    l = get_lobby_by_player_id(id)
    if l.make_turn(id, pos):
        return {"status":"OK"}
    else:
        return {"status":"Fail"}

    

@command("leave_lobby")
def leave_lobby(id, **kwargs):
    pass
    