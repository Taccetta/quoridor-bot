import numpy as np
from itertools import product as iteration
from pawns import MyPawn
from wall import MyWall


class BotQuoridor():


    def __init__(self):
        self.board = None
        self.side = None
        self.opp_side = None
        self.from_row = 0
        self.from_col = 0
        self.to_row = 0
        self.to_col = 0
        self.remaining_walls = 1
        self.my_pawn_coordinates = []
        self.opp_pawn = []
        self.walls = []
        self.created_pawns = []
        self.possible_moves = []
        self.final_choice = []
        self.im_going_to_move = "."
        self.wall_place = 0
        self.wall_placing_coordinates = []


    def board_state_creator(self):
        self.board = [char for char in self.board]
        self.board = np.array(self.board).reshape(17,17)


    def opponent_side_set(self):
        if self.side == 'N':
            self.opp_side = 'S'
        else:
            self.opp_side = 'N'


    def check_pawns_and_walls_position(self):
        for row, col in iteration(range(0, 17, 1), range(0, 17, 1)):
            if self.board[row][col] == self.side:
                self.my_pawn_coordinates.append((row, col))
            elif self.board[row][col] == self.opp_side:
                self.opp_pawn.append((row, col))
            elif self.board[row][col] == '-' or self.board[row][col] == '|':
                self.walls.append((row, col))


    def pawn_call(self):
        for pawn in self.my_pawn_coordinates:
            self.created_pawns.append(MyPawn(pawn[0], pawn[1], self.side, 
                                        self.walls, self.my_pawn_coordinates, 
                                        self.opp_pawn
                                    ))
        for pawn in self.created_pawns:
            for moves in pawn.my_movements:
                self.possible_moves.append(moves)


    def decide_move(self):
        best_score = -1000
        for move in self.possible_moves:
            if move[2] >= best_score:
                best_score = move[2]
                self.final_choice = move[0:2]
        print("Side: ", self.side)

        if self.final_choice == [] or best_score < -3 and self.remaining_walls > 5:
            self.wall_place = MyWall(self.side, self.walls, 
                            self.my_pawn_coordinates, self.opp_pawn)
            if self.wall_place.final_wall_choice == []:
                self.im_going_to_move = "pawn"
            else:
                self.im_going_to_move = "wall"
            self.wall_placing_coordinates.append((self.wall_place.final_wall_choice[0] - self.created_pawns[0].direction, 
                                                self.wall_place.final_wall_choice[1]))
            print(self.im_going_to_move)

        else:
            self.im_going_to_move = "pawn"
            print(self.im_going_to_move)
        print("choice", self.final_choice)


    def bot_play(self):
        self.board_state_creator()
        self.opponent_side_set()
        self.check_pawns_and_walls_position()
        print("\n\n\n  0   1   2   3   4   5   6   7   8")
        print(str(self.board).replace("'", "").replace("[[", " |").replace("[", "|").replace("]]", "|").replace("]", "|"))
        self.pawn_call()
        self.decide_move()
