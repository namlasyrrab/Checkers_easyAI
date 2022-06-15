# ********************************************************************************************
#
# Group Members:Salman Ahmed Barry, Greydi Lora
# Coded by: Salman Ahmed Barry
# Course: INTRO To Artificial Inteligence (CAP4630 001) Professor: Oge Marques
# Due Date:6/17/2022	Due Time: 11:59 pm
# Total Points: 100             Module 03
#
# *********************************************************************************************

# --------TEACHERS Note--------
# i have added comments in the areas new content is added

# -----------------------------Library------------------------------------

from easyAI import TwoPlayerGame, AI_Player, Negamax
# REMOVED "Human_Player" import
# due to lack of use to make code more efficient
# the code relies on two AI players instead for testing purposes
from easyAI import solve_with_iterative_deepening
import numpy as np

# --------------------Glabal Values Declaration---------------------------

even = [0,2,4,6]
odd = [1,3,5,7]
even_row = [(i,j) for i in even for j in odd]
odd_row = [(i,j) for i in odd for j in even]
black_squares = even_row + odd_row

# ----------------------------------------------CLASS (CHECKER GAME)------------------------------------------------

class Checker(TwoPlayerGame):


    # -------------Initialization-------------------
    # intializes the board, the white peices and black peices
    # are initializes as array objects and identifies the black
    # and white territory for victory conditions
    # ----------------------------------------------
    def __init__(self, players):

        self.players = players
        self.blank_board = np.zeros((8,8), dtype=object)
        self.board = self.blank_board.copy()
        self.black_pieces = [
            (0,1), (0,3), (0,5), (0,7),
            (1,0), (1,2), (1,4), (1,6)
        ]
        self.white_pieces = [
            (6,1), (6,3), (6,5), (6,7),
            (7,0), (7,2), (7,4), (7,6)
        ]
        for i,j in self.black_pieces:
            self.board[i,j] = "B"
        for i,j in self.white_pieces:
            self.board[i,j] = "W"
        self.white_territory = [(7,0), (7,2), (7,4), (7,6)]
        self.black_territory = [(0,1), (0,3), (0,5), (0,7)]
        self.players[0].pos = self.white_pieces
        self.players[1].pos = self.black_pieces
        self.current_player = 1 # player 1 starts.

    # --------Possibles moves for black/whte--------
    # returns the possible moves for the white pieces
    # Due to the way the AI works I couldnt teach it to prioritize chain killing thus victory Due to kills does not occur
    #(tested on sample of thousand mathces)
    # ----------------------------------------------
    def possible_moves_on_white_turn(self):
        table_pos = []
        old_new_piece_pos = []
        board = self.blank_board.copy() # board position before move
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        for v in self.players[self.current_player-1].pos:
        # get legal move of each pieces. (old piece location, new piece location)
        # get position of each move (list of all table position)
            old_piece_pos = v
            step_pos = [(v[0]-1, v[1]-1), (v[0]-1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            # print(old_piece_pos,j)
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))
        for i,j in old_new_piece_pos:
        # board position after  move
            b = board.copy()
            b[i[0], i[1]] = 0 # old position
            b[j[0], j[1]] = "W"# new position
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_white_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"
        self.board = board
        return table_pos

    def possible_moves_on_black_turn(self):
        #returns the possible moves for the black pieces
        table_pos = []
        old_new_piece_pos = []
        board = self.blank_board.copy()
        # board position before move
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        for v in self.players[self.current_player-1].pos:
            # get legal move of each pieces. (old piece location, new piece location)
            # get position of each move (list of all table position)
            old_piece_pos = v
            step_pos = [(v[0]+1, v[1]-1), (v[0]+1, v[1]+1)]
            # if no piece at step_pos, step
            # otherwise jump until no piece at next step_pos
            for n in step_pos:
                if (n[0] >= 0 and n[0] <= 7) and (n[1] >= 0 and n[1] <= 7) and (n in black_squares):
                    if board[n[0], n[1]] in ["B","W"]:
                        y = ((n[0] - old_piece_pos[0]) * 2) + old_piece_pos[0]
                        x = ((n[1] - old_piece_pos[1]) * 2) + old_piece_pos[1]
                        j = (y,x)
                        is_inside_board = (j[0] >= 0 and j[0] <= 7) and (j[1] >= 0 and j[1] <= 7)
                        if (j[0] <= 7) and (j[1] <=7):
                            is_position_empty = (board[j[0], j[1]] == 0)
                        else:
                            is_position_empty = False
                        if is_inside_board and (j in black_squares) and is_position_empty:
                            old_new_piece_pos.append((old_piece_pos,j))
                    else:
                        old_new_piece_pos.append((old_piece_pos,n))
        # board position after  move
        for i,j in old_new_piece_pos:
            b = board.copy()
            b[i[0], i[1]] = 0
            b[j[0], j[1]] = "B"
            table_pos.append(b)
            assert len(np.where(b != 0)[0]) == 16, f"In possible_moves_on_black_turn(), there are {len(np.where(b != 0)[0])} pieces on the board  \n {b}"
        self.board = board
        return table_pos

    # --------Possibles moves for current Player--------
    #checks the current player and returns a function
    #that returns the possible moves for that player
    # -------------------------------------------------
    def possible_moves(self):

        if self.current_player == 2:
            return self.possible_moves_on_black_turn()
        else:
            return self.possible_moves_on_white_turn()

    # --------Piece Reset-------------------------------
    #returns the current positions of the pieces on the board before each turn
    # -------------------------------------------------
    def get_piece_pos_from_table(self, table_pos):
        if self.current_player-1 == 0:
            x = np.where(table_pos == "W")
        elif self.current_player-1 == 1:
            x = np.where(table_pos == "B")
        else:
            raise ValueError("There can be at most 2 players.")
        assert len(np.where(table_pos != 0)[0]) == 16, f"In get_piece_pos_from_table(), there are {len(np.where(table_pos != 0)[0])} pieces on the board  \n {table_pos}"
        return [(i,j) for i,j in zip(x[0], x[1])]

    # --------Possibles moves for current Player--------
    #assigning the new positions of the pieces as the current positions
    # -------------------------------------------------
    def make_move(self, pos):
    # ---------------------------------Added content--------------------------
        newpos_1 = [] #list that will hold the new positions for P1
        newpos_2 = [] #list that will hold the new positions for P2
        for i in range(8):
            for j in range(8):
                if pos[i,j] == "B": #Looking for B peices in the checker board array
                    current_pos=(i,j)
                    newpos_2.append(current_pos) #appending list with new positions
                if pos[i,j] == "W": #Looking for W peices in the checker board array
                    current_pos=(i,j)
                    newpos_1.append(current_pos)#appending list with new positions
        self.players[0].pos = newpos_1 #new player positions for player 1 to return to possible moves
        self.players[1].pos = newpos_2 #new player positions for player 2 to return to possible moves
    # ----------------------------------------------------------

    # --------Instant Lose condition--------
    #returns the instant lose condition for a player making it to the other side
    # -------------------------------------------------
    def lose(self):
        # ---------------------------------Added content--------------------------
        for i in range(8):
            if self.board[7,i] == "B": #if Black squares are in white territory
                return 1
        for i in range(8):
            if self.board[0,i] == "W": #if white squares are in black territory
                return 1
        # -----------------------------------------------------------

    # --------No moves Lose condition--------
    #returns true if playr runs out of possible moves due to no viable position or out of peices
    # -------------------------------------------------
    def is_over(self):
        # --------------------------------Added content--------------------------

        return (self.possible_moves() == []) or self.lose() #checks if there are no possible moves or one of the players lose
        # -----------------------------------------------------------

    def show(self):
        # board position before move
        board = self.blank_board.copy()
        print(f"player 1 positions = {self.players[0].pos}")
        print(f"player 2 positions = {self.players[1].pos}")
        for (p,l) in zip(self.players, ["W", "B"]):
            for x,y in p.pos:
                board[x,y] = l
        print('\n')
        print(board)

    def scoring(self):
       """
       win = 0
       lose = -100
       """
       # ---------------------------------Added content--------------------------
       return -100 if self.lose() else 0
       # -----------------------------------------------------------

# -------------------------------------------MAIN---------------------------------------------------

if __name__ == "__main__":
    aiplayer1 = Negamax(2) #the ai will think 2 movies ahead
    aiplayer2 = Negamax(3) #the ai will think 3 movies ahead
    game = Checker([AI_Player(aiplayer1), AI_Player(aiplayer2)])
    history = game.play()
    if game.lose(): #congratulate player on win
            print("A Player wins!!")
    else: #draw #if both players are out of moves
        print("Looks like we have a draw.")
