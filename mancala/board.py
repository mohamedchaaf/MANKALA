class MancalaBoard:
    def __init__(self):
        self.board = {
            'A': 4, 'B': 4, 'C': 4, 'D': 4, 'E': 4, 'F': 4,
            'G': 4, 'H': 4, 'I': 4, 'J': 4, 'K': 4, 'L': 4,
            1: 0, 2: 0
        }
        self.player1_pits = ('A','B','C','D','E','F')
        self.player2_pits = ('G','H','I','J','K','L')

        self.opposite = {
            'A':'L','B':'K','C':'J','D':'I','E':'H','F':'G',
            'G':'F','H':'E','I':'D','J':'C','K':'B','L':'A'
        }

        self.next_pit = {
            'A':'B','B':'C','C':'D','D':'E','E':'F','F':1,
            1:'G','G':'H','H':'I','I':'J','J':'K','K':'L','L':2,
            2:'A'
        }
    def possibleMoves(self, player):
        pits = self.player1_pits if player == 1 else self.player2_pits
        return [p for p in pits if self.board[p]> 0 ] 
    
    def doMove(self,player,pit):

        # ndo pits mn place li 5yrha 
        seeds = self.board[pit]
        self.board[pit] = 0
        current = pit

        # hna nsrbiw seeds f bits
        while seeds > 0 : 
            current = self.next_pit[current]
            if (player == 1 and current == 2) or (player == 2 and current == 1):
                continue
            self.board[current] += 1
            seeds -= 1

        player_pits = self.player1_pits if player == 1 else self.player2_pits
        player_store = 1 if player == 1 else 2


        # capture 

        if current in player_pits and self.board[current] == 1:
            opposite_pit = self.opposite[current]
            captured = self.board[opposite_pit]

            if captured > 0:
                self.board[player_store] += captured + 1
                self.board[current] = 0
                self.board[opposite_pit] = 0

        # check for extra turn
        extra_turn = current == player_store
        return extra_turn   


        

