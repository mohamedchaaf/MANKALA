from .game import Game
import copy
import math

class Play:
    def __init__(self):
        self.game = Game()

    def humanTurn(self):
        moves = self.game.state.possibleMoves(self.game.playerSide['HUMAN'])
        print("Your possible moves:", moves)

        move = input("Enter your move (pit letter): ").upper()

        while move not in moves:
            move = input("Invalid move! Choose again: ").upper()

        extra_turn = self.game.state.doMove(self.game.playerSide['HUMAN'], move)
        return extra_turn
    
    def computerTurn(self, depth=4):
        value, bestPit = self.MinimaxAlphaBetaPruning(self.game, 'COMPUTER', depth, -math.inf, math.inf)
        print(f"Computer chooses pit: {bestPit}")
        extra_turn = self.game.state.doMove(self.game.playerSide['COMPUTER'], bestPit)
        return extra_turn

    
    @staticmethod
    def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta):
        if game.gameOver() or depth == 0:
            bestValue = game.evaluate()
            return bestValue, None

        if player == 'COMPUTER':
            bestValue = -math.inf
            bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                next_player = player if extra_turn else 'HUMAN'
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, next_player, depth-1, alpha, beta)
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue >= beta:
                    break
                if bestValue > alpha:
                    alpha = bestValue
            return bestValue, bestPit
        else:
            bestValue = math.inf
            bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                next_player = player if extra_turn else 'COMPUTER'
                value, _ = Play.MinimaxAlphaBetaPruning(child_game, next_player, depth-1, alpha, beta)
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue <= alpha:
                    break
                if bestValue < beta:
                    beta = bestValue
            return bestValue, bestPit