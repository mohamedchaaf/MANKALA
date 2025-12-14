from .board import MancalaBoard

class Game:
    def __init__(self, playerSide={'HUMAN': 1, 'COMPUTER': 2}):

        self.state = MancalaBoard()
        self.playerSide = playerSide

    def gameOver(self):
        player1_empty = all(self.state.board[p] == 0 for p in self.state.player1_pits)
        player2_empty = all(self.state.board[p] == 0 for p in self.state.player2_pits)

        if player1_empty or player2_empty:

            self.state.board[self.playerSide['HUMAN']] += sum(self.state.board[p] for p in self.state.player1_pits)
            self.state.board[self.playerSide['COMPUTER']] += sum(self.state.board[p] for p in self.state.player2_pits)
   
            # nfrgho ge3 les pits 
            for p in self.state.player1_pits:
                self.state.board[p] = 0
            for p in self.state.player2_pits:
                self.state.board[p] = 0
            return True
        return False
    
    def findWinner(self):

        human_store = self.state.board[self.playerSide['HUMAN']]
        computer_store = self.state.board[self.playerSide['COMPUTER']]

        if human_store > computer_store:
            return 'HUMAN', human_store
        elif computer_store > human_store:
            return 'COMPUTER', computer_store
        else:
            return 'DRAW', human_store
        
    def evaluate(self):
        return self.state.board[self.playerSide['COMPUTER']] - self.state.board[self.playerSide['HUMAN']]



# class Game:
#     def __init__(self, playerSide={'COMPUTER1': 1, 'COMPUTER2': 2}):

#         self.state = MancalaBoard()
#         self.playerSide = playerSide

#     def gameOver(self):
#         player1_empty = all(self.state.board[p] == 0 for p in self.state.player1_pits)
#         player2_empty = all(self.state.board[p] == 0 for p in self.state.player2_pits)

#         if player1_empty or player2_empty:

#             self.state.board[self.playerSide['COMPUTER1']] += sum(self.state.board[p] for p in self.state.player1_pits)
#             self.state.board[self.playerSide['COMPUTER2']] += sum(self.state.board[p] for p in self.state.player2_pits)
   
#             # nfrgho ge3 les pits 
#             for p in self.state.player1_pits:
#                 self.state.board[p] = 0
#             for p in self.state.player2_pits:
#                 self.state.board[p] = 0
#             return True
#         return False
    
#     def findWinner(self):

#         human_store = self.state.board[self.playerSide['COMPUTER1']]
#         computer_store = self.state.board[self.playerSide['COMPUTER2']]

#         if human_store > computer_store:
#             return 'COMPUTER1', human_store
#         elif computer_store > human_store:
#             return 'COMPUTER2', computer_store
#         else:
#             return 'DRAW', human_store
        
#     def evaluate(self):
#         return self.state.board[self.playerSide['COMPUTER2']] - self.state.board[self.playerSide['COMPUTER1']]


#     def evaluate2(self):
#         board = self.state.board


#         my_store = board[self.playerSide['COMPUTER2']]
#         opp_store = board[self.playerSide['COMPUTER1']]

#         my_pits = self.state.player2_pits
#         opp_pits = self.state.player1_pits

#         my_non_empty = sum(1 for p in my_pits if board[p] > 0)
#         opp_non_empty = sum(1 for p in opp_pits if board[p] > 0)

#         return (my_store + my_non_empty) - (opp_store + opp_non_empty)


    