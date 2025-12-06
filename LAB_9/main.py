from src.algorithms import minimax_search
from src.gameClass import play_game
from src.FiveMiseryGameClass import MiseryGame
from src.players import smart_player,random_player,human_player


# human_player() is defined inside the players.py file
# game logic is defined in FiveMiseryGameClass.py 

def main():
    
    print("RANDOM VS SMART AGENT PLAYING...\n")
    game1 = MiseryGame(["SmartPlayer", "RandomPlayer"], 5)
    strategies = {
        "SmartPlayer": smart_player(minimax_search),
        "RandomPlayer": random_player,
    }
    terminal1 = play_game(game1, strategies, True)
    print("END STATE: ", terminal1)
    print("WINNER: ", terminal1.to_move)

    print("\n\nHUMAN VS SMART AGENT PLAYING...\n")
    game2 = MiseryGame(["SmartPlayer", "HumanPlayer"], 5)
    strategies = {
        "SmartPlayer": smart_player(minimax_search),
        "HumanPlayer": human_player
    }
    terminal2 = play_game(game2, strategies, True)
    print("END STATE: ", terminal2)
    print("WINNER: ", terminal2.to_move)

main()