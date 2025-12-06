from src.gameClass import Game
from src.boardClass import Board

class State:
    def __init__(self, to_move: str, global_total: int):
        self.global_total = global_total
        self.to_move = to_move
        
    def __repr__(self):
        return f"TO MOVE: {self.to_move} | CURRENT TOTAL: {self.global_total}"

class MiseryGame(Game):

    def __init__(self, players, terminal_test = 5):
        self.players = players
        self.terminal = terminal_test
        self.initial = State(players[0], 0)

    def actions(self, state):
        """Legal moves are 1,2,3 at most combined"""
        return [1,2,3]

    def result(self, state: State, move):
        next_player = None
        if state.to_move == self.players[0]:
            next_player = self.players[1]
        else:
            next_player = self.players[0]
        return State(
            next_player, (state.global_total + move)
        )

    def utility(self, state: State, player: str):
        """Return the value to player; 1 for win, -1 for loss"""
        if self.is_terminal(state):
            if state.to_move == player:
                return 1
            return -1

    def is_terminal(self, state: State):
        return state.global_total >= self.terminal

    def display(self, board): print(board)     
