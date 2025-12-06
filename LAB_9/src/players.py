import random

def smart_player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]


def random_player(game, state):
    """A game player who  uses random choice to do a next move"""
    return random.choice(list(game.actions(state)))

def human_player(game, state):
    print("Humans Turn!")
    print(f"Current State:\n {state}")
    move = int(input("Enter Move: "))
    while True:
        if move in game.actions(state):
            return move
        else:
            print("Move must be: ", {game.actions(state)})
    