from .game import Game
import copy
import math

class PlayAI:
    def __init__(self):
        self.game = Game()
    
    def computerTurn(self, depth=4):
        value, bestPit = self.MinimaxAlphaBetaPruning(self.game, 'COMPUTER1', depth, -math.inf, math.inf)
        print(f"Computer chooses pit: {bestPit}")
        extra_turn = self.game.state.doMove(self.game.playerSide['COMPUTER1'], bestPit)
        return extra_turn
    

    def computer2Turn(self, depth=4):
        value, bestPit = self.MinimaxAlphaBetaPruning(self.game, 'COMPUTER2', depth, -math.inf, math.inf)
        print(f"Computer 2 chooses pit: {bestPit}")
        extra_turn = self.game.state.doMove(self.game.playerSide['COMPUTER2'], bestPit)
        return extra_turn


    
    @staticmethod
    def MinimaxAlphaBetaPruning(game, player, depth, alpha, beta):
        if game.gameOver() or depth == 0:
            if player == 'COMPUTER1':
                bestValue = game.evaluate()
            elif player == 'COMPUTER2':
                bestValue = game.evaluate2()
            return bestValue, None

        if player == 'COMPUTER1':
            bestValue = -math.inf
            bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                next_player = player if extra_turn else 'COMPUTER2'
                value, _ = PlayAI.MinimaxAlphaBetaPruning(child_game, next_player, depth-1, alpha, beta)
                if value > bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue >= beta:
                    break
                if bestValue > alpha:
                    alpha = bestValue
            return bestValue, bestPit
        else:
            player = 'COMPUTER2'
            bestValue = math.inf
            bestPit = None
            for pit in game.state.possibleMoves(game.playerSide[player]):
                child_game = copy.deepcopy(game)
                extra_turn = child_game.state.doMove(game.playerSide[player], pit)
                next_player = player if extra_turn else 'COMPUTER1'
                value, _ = PlayAI.MinimaxAlphaBetaPruning(child_game, next_player, depth-1, alpha, beta)
                if value < bestValue:
                    bestValue = value
                    bestPit = pit
                if bestValue <= alpha:
                    break
                if bestValue < beta:
                    beta = bestValue
            return bestValue, bestPit