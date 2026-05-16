commands = {}

def command(func):
    def wrapper(cmd_name):
        commands[cmd_name] = func
        return func
    return wrapper

@command("create_or_join")
def create_or_join():
    pass

@command("make_turn")
def make_turn():
    pass

@command("leave_lobby")
def leave_lobby():
    pass