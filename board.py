import numpy as np
import math

class Board:
    """
    A class used to represent the board we are playing on
    Attributes
    ----------
    columns int : Number of columns used
    rows int : Number of rows used
    board nparray : The playable slots of the board
    
    Methods
    -------
    playPiece : move a piece onto the board
    getNextValidPosition : for a column, get next free position (=0)
    getFreeColumns : get all columns where there's a free position (=0)
    calculScore : score a hypothetical board for minimax algorithm
    countConnect4 : check if winner onto the hypothetical board for minimax algorithm
    isTerminalNode : check if winner of board full
    minimax : Implementation of minimax algorithm
    verifKeepPlaying : check if winner on actual board. Used in isTerminalNode

    """
    def __init__(self, columns, rows):
        """ Create an empty board to play with
        """

        self.columns = columns
        self.rows = rows
        self.board = np.zeros((rows,columns), dtype=int)
    
    def playPiece(self, row, column, color):
        """ Change the value of a slot as the player or the AI just played
            Parameters
                board : The board we are playing with
                row : The row the player or AI decided to play on
                column : The column the player or AI decided to play on
                color : Define the player or AI. 1 for player, 2 for AI """
        self.board[row][column] = color

    def getNextValidPosition(self, column):
        """ According to the column passed in, get the next row with value = 0
            Parameters
                board : The board we are playing with
                column : The column the player or AI would like to play on
            Returns
                Int : The next row with value = 0
                None : If there is no next row at 0 """   
        if column != None and self.board[self.rows - 1][column] == 0:
            return np.where(self.board[0:, column] == 0)[0][0]
        else:
            return None

    def getFreeColumns(self):
        """ Search for columns where there is a next valid position = 0 to play on
            Parameters
                board : The board we are playing with
            Returns
                List : Ids of columns where player of IA can play on """  
        validMoves = []
        for col in range(self.columns):
            if self.getNextValidPosition(col) != None:
                validMoves.append(col)
        return validMoves

    def calculScore(self):
        """ Assign a general score to the board passed in.
            The goal is to foresee the best possible board case scenario for the IA to play
            Parameters
                board : The board we are playing with
            Returns
                Int : The score of the board  """
        score = 0

        # The more you play the center column, the more u have chances to win
        centerColumnCount = list(self.board[:, 3]).count(2)
        score += centerColumnCount * 3
        # Check Horizontal lines
        for r in range(self.rows):
            rowsTab = list(self.board[r,:])
            for c in range(self.columns-3):
                line = rowsTab[c:c+4] # +4 because a line of 4 required to win
                score += self.countConnect4(line)
        
        # Check Vertical lines
        for c in range(self.columns):
            colsTab = list(self.board[:,c])
            for r in range(self.rows-3):
                line = colsTab[r:r+4]
                score += self.countConnect4(line)
        # Check diagonals
        for r in range(self.rows-3):
            for c in range(self.columns-3):
                line = [self.board[r+i][c+i] for i in range(4)]
                score += self.countConnect4(line)
        #Check diagonals the other way
        for r in range(self.rows-3):
            for c in range(self.columns-3):
                line = [self.board[r+3-i][c+i] for i in range(4)]
                score += self.countConnect4(line)
        return score

    def countConnect4(self, line):
        """ Assign a score value to a line of 4 slots passed in.
            The more there is AI color, the higher the score
            The more there is Player color, the lesser the score
            Parameters
                board : The board we are playing with
            Returns
                Int : The score of the board  """
        score = 0 # Score the more AI color (2) we count on the line
        if line.count(2) == 4:
            score += 100
        elif line.count(2) == 3 and line.count(0) == 1:
            score += 5
        elif line.count(2) == 2 and line.count(0) == 2:
            score += 2

        if line.count(1) == 3 and line.count(0) == 1: # Score the more Player color (1) we count on the line
            score -= 4
        return score

    def isTerminalNode(self):
        return not self.verifKeepPlaying(1) or not self.verifKeepPlaying(2) or len(self.getFreeColumns()) == 0

    def minimax(self, depth, player):
        """ Implementation of the minmax algorithm, minimizing the player loss of the IA while maximizing the player's score
        https://fr.wikipedia.org/wiki/Algorithme_minimax

        Parameters
                board : The board we are playing with
                depth : size of the tree we use to foresee and score the possible boards. The more the depth, the slower the algorithm. 4 is good, 5 begins to be too slow.
                player : variable used to switch from minimizing IA loss and maximizing player's score
        Returns
            Tuple(int column,int value)
                value is the highest score when maximizing, the lowest score when minimizing
                column is the column where we hypothetically make the next move (copy of the board)
        """
        valid_locations = self.getFreeColumns()
        is_terminal = self.isTerminalNode()
        if depth == 0 or is_terminal:
            if is_terminal:
                if not self.verifKeepPlaying(2):
                    return (None, 1000000)
                elif not self.verifKeepPlaying(1):
                    return (None, -1000000)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.calculScore())
        if player == 2: # Maximizing IA
            value = -math.inf
            column = ''
            for col in valid_locations:
                row = self.getNextValidPosition(col)
                board2 = Board(self.columns, self.rows)
                board2.board = self.board.copy()
                board2.playPiece(row, col, 2)
                score = board2.minimax( depth-1, 1)[1]
                if score > value:
                    value = score
                    column = col

        else: # Minimizing IA
            value = math.inf
            column = ''
            for col in valid_locations:
                row = self.getNextValidPosition(col)
                board2 = Board(self.columns, self.rows)
                board2.board = self.board.copy()
                board2.playPiece(row, col, 1)
                score = board2.minimax(depth-1, 2)[1]
                if score < value:
                    value = score
                    column = col
        return column, value

    def verifKeepPlaying(self, color):
        """ Check if the game can go on or not, by checking if somebody won horizontally, vertically and diagonally
            Parameters
                board : The board we are playing with
                color : The player we want to verify (1 for player, 2 for AI)
            Returns
                Bool : True if the game can go on, False if not  """
        # Check connect 4 horizontally
        for c in range(self.columns-3):
            for r in range(self.rows):
                if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] == color:
                    return False

        # Check connect 4 vertically
        for c in range(self.columns):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] == color:
                    return False

        # Check diagonals bottom left to top right
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] == color:
                    return False

        # Check diagonals top left to bottom right
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] == color:
                    return False
        return True