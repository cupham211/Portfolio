# Author: Christine Pham
# Creation Date: 2/29/2020
# Description: A Xiangqi simulation game.


class Piece:
    """a super class containing all piece types. King, Bodyguards, Elephant, Cars, Horses, Cannon, and Soldier inherit
    from it. Contains rules applied to all pieces"""

    def __init__(self, _alive, _color, _loc_x, _loc_y):
        """initialize the color and vitals of a piece"""
        self._alive = True
        self._color = _color
        self._loc_x = _loc_x
        self._loc_y = _loc_y

    def get_vitals(self):
        """returns if the piece is dead or alive"""
        return self._alive

    def get_color(self):
        """returns color of the piece"""
        return self._color

    def get_loc_x(self):
        """returns the x coordinates of the piece"""
        return self._loc_x

    def get_loc_y(self):
        """returns the y coordinates of the piece"""
        return self._loc_y

    def set_vitals(self, status):
        """kills the piece"""
        self._alive = status

    def set_loc_x(self, loc):
        """sets the row location of the piece"""
        self._loc_x = loc

    def set_loc_y(self, loc):
        """set the column location of the piece"""
        self._loc_y = loc


class King(Piece):
    """a class that contains rules applied to the King piece"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='King'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """tests to see if the move attempted can be made by the king."""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._color == 'Red' and self._alive:
            if 0 <= x2 <= 2 and 3 <= y2 <= 5:
                if (abs(x2 - x1) == 1 and y2 - y1 == 0) or (x2 - x1 == 0 and abs(y2 - y1) == 1):
                    result = True
        elif self._color == 'Black' and self._alive:
            if 7 <= x2 <= 9 and 3 <= y2 <= 5:
                if (abs(x2 - x1) == 1 and y2 - y1 == 0) or (x2 - x1 == 0 and abs(y2 - y1) == 1):
                    result = True
        return result


class Bodyguard(Piece):
    """a class that contains rules applied to Bodyguards"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Bodyguard'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """determines validity of move attempted by bodyguards"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._color == 'Red' and self._alive:
            if 0 <= x2 <= 2 and 3 <= y2 <= 5:
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    result = True
        elif self._color == 'Black' and self._alive:
            if 7 <= x2 <= 9 and 3 <= y2 <= 5:
                if abs(x2 - x1) == 1 and abs(y2 - y1) == 1:
                    result = True
        return result


class Elephant(Piece):
    """a class that contains rules applied to Elephants"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Elephant'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """determines if a move for an elephant is valid or not"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._color == 'Red' and self._alive:
            if 0 <= x2 <= 4 and 0 <= y2 <= 8:
                if abs(x2 - x1) != 0 and abs(y2 - y1) != 0 and abs(x2 - x1) == abs(y2 - y1):
                    result = True
        elif self._color == 'Black' and self._alive:
            if 5 <= x2 <= 9 and 0 <= y2 <= 8:
                if abs(x2 - x1) != 0 and abs(y2 - y1) != 0 and abs(x2 - x1) == abs(y2 - y1):
                    result = True
        return result


class Car(Piece):
    """a class containing rules applied to Cars"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Car'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """checks if move can be performed by car"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._alive:
            if (abs(x2 - x1) > 0 and y2 - y1 == 0) or (x2 - x1 == 0 and abs(y2 - y1) > 0):
                result = True
        return result


class Horse(Piece):
    """a class containing rules applied to Horses"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Horse'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """tests if the move attempted for the horse is valid"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._alive:
            if (abs(x2 - x1) == 2 and abs(y2 - y1) == 1) or (abs(x2 - x1) == 1 and abs(y2 - y1) == 2):
                result = True

        return result


class Cannon(Piece):
    """a class containing rules applied to Cannons"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Cannon'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """checks if move can be performed by car"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        if self._alive:
            if (abs(x2 - x1) > 0 and y2 - y1 == 0) or (x2 - x1 == 0 and abs(y2 - y1) > 0):
                result = True
        return result


class Soldier(Piece):
    """a class containing rules applied to Soldiers"""

    def __init__(self, _alive, _color, _loc_x, _loc_y, _rank='Soldier'):
        """1 class specific parameter along with parent class parameters"""
        super().__init__(_alive, _color, _loc_x, _loc_y)
        self._rank = _rank

    def get_rank(self):
        """returns the name of the piece"""
        return self._rank

    def valid_moves(self, start, dest):
        """valid moves allowed by a soldier"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]
        if self._color == 'Red' and self._alive:
            # if the red soldier is across the river
            if 5 <= x1 < x2:  # if not moving backwards
                if (abs(y2 - y1) == 1 and x2 - x1 == 0) or (x2 - x1 == 1 and y2 - y1 == 0):
                    result = True
            elif 5 > x1 and y1 == y2:
                if x2 - x1 == 1:
                    result = True
        elif self._color == 'Black' and self._alive:
            # if the black soldier is across the river
            if 4 >= x1 > x2:
                if (abs(y2 - y1) == 1 and x2 - x1 == 0) or (x2 - x1 == -1 and y2 - y1 == 0):
                    result = True
            elif x1 > 4 and y1 == y2:
                if x2 - x1 == -1:
                    result = True
        return result


class XiangqiGame:
    """a class representing the Xiangqi board"""

    def __init__(self):
        """initialize pieces and locations"""

        self._col = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        self._row = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9}

        columns = 9
        width = 10
        self._board = [[None for _ in range(columns)] for _ in range(width)]  # row-major order
        self.reset_board()
        self._turn = 'Red'
        self._game_state = 'UNFINISHED'
        self._checkmate = False

    def reset_board(self):

        # initialize red pieces on board
        self._board[self._row['1']][self._col['a']] = Car(True, 'Red', 0, 0)
        self._board[self._row['1']][self._col['i']] = Car(True, 'Red', 0, 8)
        self._board[self._row['1']][self._col['b']] = Horse(True, 'Red', 0, 1)
        self._board[self._row['1']][self._col['h']] = Horse(True, 'Red', 0, 7)
        self._board[self._row['1']][self._col['c']] = Elephant(True, 'Red', 0, 2)
        self._board[self._row['1']][self._col['g']] = Elephant(True, 'Red', 0, 6)
        self._board[self._row['1']][self._col['d']] = Bodyguard(True, 'Red', 0, 3)
        self._board[self._row['1']][self._col['f']] = Bodyguard(True, 'Red', 0, 5)
        self._board[self._row['1']][self._col['e']] = King(True, 'Red', 0, 4)
        self._board[self._row['3']][self._col['b']] = Cannon(True, 'Red', 2, 1)
        self._board[self._row['3']][self._col['h']] = Cannon(True, 'Red', 2, 7)
        self._board[self._row['4']][self._col['a']] = Soldier(True, 'Red', 3, 0)
        self._board[self._row['4']][self._col['c']] = Soldier(True, 'Red', 3, 2)
        self._board[self._row['4']][self._col['e']] = Soldier(True, 'Red', 3, 4)
        self._board[self._row['4']][self._col['g']] = Soldier(True, 'Red', 3, 6)
        self._board[self._row['4']][self._col['i']] = Soldier(True, 'Red', 3, 8)

        # initialize black pieces on board
        self._board[self._row['10']][self._col['a']] = Car(True, 'Black', 9, 0)
        self._board[self._row['10']][self._col['i']] = Car(True, 'Black', 9, 8)
        self._board[self._row['10']][self._col['b']] = Horse(True, 'Black', 9, 1)
        self._board[self._row['10']][self._col['h']] = Horse(True, 'Black', 9, 7)
        self._board[self._row['10']][self._col['c']] = Elephant(True, 'Black', 9, 2)
        self._board[self._row['10']][self._col['g']] = Elephant(True, 'Black', 9, 6)
        self._board[self._row['10']][self._col['d']] = Bodyguard(True, 'Black', 9, 3)
        self._board[self._row['10']][self._col['f']] = Bodyguard(True, 'Black', 9, 5)
        self._board[self._row['10']][self._col['e']] = King(True, 'Black', 9, 4)
        self._board[self._row['8']][self._col['b']] = Cannon(True, 'Black', 7, 1)
        self._board[self._row['8']][self._col['h']] = Cannon(True, 'Black', 7, 7)
        self._board[self._row['7']][self._col['a']] = Soldier(True, 'Black', 6, 0)
        self._board[self._row['7']][self._col['c']] = Soldier(True, 'Black', 6, 2)
        self._board[self._row['7']][self._col['e']] = Soldier(True, 'Black', 6, 4)
        self._board[self._row['7']][self._col['g']] = Soldier(True, 'Black', 6, 6)
        self._board[self._row['7']][self._col['i']] = Soldier(True, 'Black', 6, 8)

    def get_piece(self, xycoord):
        """returns the object at the xy coordinate location specified"""
        return self._board[xycoord[0]][xycoord[1]]

    def find_location(self, rank, color):
        """returns a list of xy coord of the specified piece parameters. Returns empty list if none found."""
        squares = []

        for row in self._board:
            for obj in row:
                if obj is not None:  # if piece on square matches and isn't dead
                    if obj.get_rank() == rank and obj.get_color() == color and obj.get_vitals() is True:
                        # group the xy coord into a list and send inside a list
                        setxy = [obj.get_loc_x(), obj.get_loc_y()]
                        squares.append(setxy)

        return squares

    def check_on_board(self, coord):
        """checks if the coordinate is within board boundaries"""
        coord = list(coord)

        if coord[0] not in self._col or coord[1] not in self._row:  # checks if letter within bounds
            return False
        return True

    def convert_to_xy(self, strcoord):
        """converts and returns the string coord to a [x, y]"""
        strcoord = list(strcoord)
        if len(strcoord) == 2:
            xy = [self._row[strcoord[1]], self._col[strcoord[0]]]
        else:
            xy = [self._row['10'], self._col[strcoord[0]]]
        return xy

    def set_whose_turn(self, player):
        """sets the turn of the player"""
        self._turn = player

    def get_whose_turn(self):
        """returns whose turn it is for the round"""
        return self._turn

    def get_game_state(self):
        """returns either UNFINISHED, BLACK_WON, or RED_WON"""
        return self._game_state

    def check_coast_clear_ver(self, start, dest):
        """checks if there are pieces in the way from the starting point to the ending point vertically.
        param: int coords, returns a boolean result: True if no pieces blocking"""
        result = True
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]
        if y1 == y2 and x1 < x2:
            for i in range(x1 + 1, x2):
                if self._board[i][y1] is not None:
                    result = False
        if y1 == y2 and x1 > x2:
            for i in range(x2 + 1, x1):
                if self._board[i][y1] is not None:
                    result = False
        return result

    def check_coast_clear_hor(self, start, dest):
        """checks if there are pieces in the way from the starting point to the ending point horizontally.
        param: int coords, returns a boolean result: True if no pieces blocking"""
        result = True
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]
        if x1 == x2 and y1 < y2:
            for i in range(y1 + 1, y2):
                if self._board[x1][i] is not None:
                    result = False
        if x1 == x2 and y1 > y2:
            for i in range(y2 + 1, y1):
                if self._board[x1][i] is not None:
                    result = False
        return result

    def check_coast_clear_dia(self, start, dest):
        """checks if there are pieces in the way from the starting point to one square in every dir diagonally.
            param: int coords, returns a boolean result: True if no pieces blocking"""
        result = True
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]
        if x2 > x1 and y2 > y1:
            if self._board[x1 + 1][y1 + 1] is not None:  # lower right
                result = False
        elif x2 < x1 and y2 > y1:
            if self._board[x1 - 1][y1 + 1] is not None:  # lower left
                result = False
        elif x2 > x1 and y2 < y1:
            if self._board[x1 + 1][y1 - 1] is not None:  # upper right
                result = False
        elif x2 < x1 and y2 < y1:
            if self._board[x1 - 1][y1 - 1] is not None:  # upper left
                result = False
        return result

    def check_coast_clear_horse(self, start, dest):
        """checks if the space in front of the horse is clear for movement"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]

        xbtw = int(abs(x1 + x2) / 2)
        ybtw = int(abs(y2 + y1) / 2)

        if abs(x2 - x1) == 2 and abs(y2 - y1) == 1:
            if self._board[xbtw][y1] is None:
                result = True
        elif abs(x2 - x1) == 1 and abs(y2 - y1) == 2:
            if self._board[x1][ybtw] is None:
                result = True
        return result

    def check_kings_sight(self, start):
        """a method that determines if the kings will face each other if a move is executed.
        Para: int location of piece about to move. Returns True if kings will face each other"""

        bking = self.find_location('King', 'Black')
        rking = self.find_location('King', 'Red')

        if bking[0][1] == rking[0][1] == start[1]:
            # store object to be moved in temp var
            temp = self._board[start[0]][start[1]]
            # set its location to None and check if column is clear between kings
            self._board[start[0]][start[1]] = None
            result = self.check_coast_clear_ver(bking[0], rking[0])
            # restore object to original location
            self._board[start[0]][start[1]] = temp
        else:
            result = False

        return result

    def cannon_valid_kill_move(self, start, dest):
        """determines if move performed by cannon is to kill a piece. returns True if kill move is valid"""
        result = False
        x1, x2, y1, y2 = start[0], dest[0], start[1], dest[1]
        xbtw = int(abs(x1 + x2) / 2)
        ybtw = int(abs(y2 + y1) / 2)
        cannon = self._board[x1][y1]
        target = self._board[xbtw][ybtw]

        if target is not None:
            if cannon.get_color() != target.get_color() and (abs(x2 - x1) == 2 and y2 - y1 == 0) \
                    or (abs(y2 - y1) == 2 and x2 - x1 == 0):
                result = True

        return result

    def is_in_check(self, color):
        """determines whether the king is in check or not"""
        result = False
        color = color.capitalize()
        coord = self.find_location('King', color)  # gets the location of the king in (x,y)
        coord = coord[0]    # strips outer brackets
        upOne, downOne, leftOne, rightOne = False, False, False, False

        stationary = self.check_tester(coord)    # result of when king hasn't moved yet

        if stationary:
            move = [coord[0]+1, coord[1]]
            if (0 <= move[0] <= 2 or 7 <= move[0] <= 9) and 3 <= move[1] <= 5 and self._board[move[0]][move[1]] is None:
                coord, move = move, coord
                # if switching positions isn't illegal from king's sight, check if space above is dangerous
                if self.check_kings_sight(move) is False:
                    upOne = self.check_tester(move)
                coord, move = move, coord
            # if space next to king isn't empty he's considered trapped so checkmate at this spot is True
            else:
                upOne = True

            move = [coord[0]-1, coord[1]]
            if (0 <= move[0] <= 2 or 7 <= move[0] <= 9) and 3 <= move[1] <= 5 and self._board[move[0]][move[1]] is None:
                coord, move = move, coord
                # check if space below is dangerous
                if self.check_kings_sight(move) is False:
                    downOne = self.check_tester(move)
                coord, move = move, coord
            else:
                downOne = True

            move = [coord[0], coord[1]+1]
            if (0 <= move[0] <= 2 or 7 <= move[0] <= 9) and 3 <= move[1] <= 5 and self._board[move[0]][move[1]] is None:
                coord, move = move, coord
                if self.check_kings_sight(move) is False:
                    rightOne = self.check_tester(move)
                coord, move = move, coord
            else:
                rightOne = True

            move = [coord[0], coord[1]-1]
            if (0 <= move[0] <= 2 or 7 <= move[0] <= 9) and 3 <= move[1] <= 5 and self._board[move[0]][move[1]] is None:
                coord, move = move, coord
                if self.check_kings_sight(move) is False:
                    leftOne = self.check_tester(move)
            else:
                leftOne = True

        # if all 5 possible positions can kill the king, king is in checkmate
            if upOne and downOne and leftOne and rightOne:
                result = True
                if color == 'Black':
                    self._game_state = 'RED_WON'
                else:
                    self._game_state = 'BLACK_WON'

        return result

    def check_tester(self, king_xy):
        """a helper function to test danger sites threatening the king. Takes the color of the king as param.
        Returns True if at least one piece can kill."""
        result = False
        kingobj = self._board[king_xy[0]][king_xy[1]]
        horse = {(2, -1), (2, 1), (-2, -1), (-2, 1), (1, -2), (-1, -2), (1, 2), (-1, 2)}
        soldier = {(-1, 0), (1, 0), (0, 1), (0, -1)}
        cannon = {(0, -1, 0, 1), (-1, 0, 1, 0), (0, 1, 0, -1), (1, 0, -1, 0)}

        x2, y2 = king_xy[0], king_xy[1]

        for location in horse:
            # orient the coordinate pair to be relative to king's location
            x1, y1 = x2-location[0], y2-location[1]
            # make sure space is within bounds and has a piece on it
            if 0 <= x1 <= 9 and 0 <= y1 <= 8 and self._board[x1][y1] is not None:
                obj = self._board[x1][y1]
                start = [x1, y1]
                # if piece is a horse and the move towards the King is valid
                if obj.get_rank() == 'Horse' and obj.valid_moves(start, king_xy):
                    # check for obstructions in path and if the colors are different
                    if self.check_coast_clear_horse(start, king_xy) and obj.get_color() != kingobj.get_color():
                        result = True
            else:
                continue

        for location in soldier:
            x1, y1 = x2-location[0], y2-location[1]
            if 0 <= x1 <= 9 and 0 <= y1 <= 8 and self._board[x1][y1] is not None:
                obj = self._board[x1][y1]
                start = [x1, y1]
                if obj.get_rank() == 'Soldier' and obj.valid_moves(start, king_xy):
                    if obj.get_color() != kingobj.get_color():
                        result = True
            else:
                continue

        for location in cannon:
            # cannon jumps to kill so get location of endpoints
            x1, y1, endx, endy = x2-location[0], y2-location[1], x2-location[2], y2-location[3]
            # check borders and if object exists on space
            if 0 <= x1 <= 9 and 0 <= y1 <= 8 and self._board[x1][y1] is not None \
                    and 0 <= endx <= 9 and 0 <= endy <= 8 and self._board[endx][endy] is None:
                obj = self._board[x1][y1]
                start = [x1, y1]
                dest = [endx, endy]
                # verify legal move of Cannon
                if obj.get_rank() == 'Cannon' and self.cannon_valid_kill_move(start, dest)  \
                        and obj.get_color() != kingobj.get_color():
                    result = True
            else:
                continue

        # get king's color to get opposite color of car
        if kingobj.get_color() == 'Black':
            color = 'Red'
        else:
            color = 'Black'
        cars = self.find_location('Car', color)
        # test all cars to see if they can get to the King
        for car in cars:
            carobj = self._board[car[0]][car[1]]

            if carobj.valid_moves(car, king_xy):
                if self.check_coast_clear_hor(car, king_xy) or self.check_coast_clear_ver(car, king_xy):
                    result = True
                else:
                    continue

        return result

    def make_move(self, start, dest):
        """a method that moves pieces on a xiangqi board. Takes two string parameters and converts them to coordinates
        the program can use. Then updates the board according to the piece moved and where it moved to/who it killed.
        Returns False if a move could not be executed"""
        move_complete = False
        move_ok = False

        # start position and end position can't be the same -- that would be like skipping a turn
        if start == dest:
            return False

        # if move is on the board boundaries and the game is still unfinished
        if self.check_on_board(start) and self.check_on_board(dest) and self.get_game_state() == 'UNFINISHED':
            startxy, destxy = self.convert_to_xy(start), self.convert_to_xy(dest)
            startpiece, endpiece = self.get_piece(startxy), self.get_piece(destxy)

            # if a piece is located on the start & the color at the starting piece matches the color of the same player
            if startpiece is not None and startpiece.get_color() == self.get_whose_turn():
                start_rank = startpiece.get_rank()

                if startpiece.valid_moves(startxy, destxy) and self.check_kings_sight(startxy) is False:
                    # check if the piece is a cannon
                    if start_rank == 'Cannon' and self.cannon_valid_kill_move(startxy, destxy):
                        kill_piecex = int(abs(destxy[0] + startxy[0])/2)
                        kill_piecey = int(abs(destxy[1] + startxy[1])/2)

                        # set captured piece vitals to False and remove from board
                        obj = self._board[kill_piecex][kill_piecey]
                        obj.set_vitals(False)
                        # if capture piece is the king, then set game_state to the winner
                        if obj.get_rank() == 'King':
                            self._game_state = self._turn.upper() + '_WON'
                        self._board[kill_piecex][kill_piecey] = None
                        move_ok = True

                    elif start_rank == 'Cannon' and self.cannon_valid_kill_move(startxy, destxy) is False \
                            and endpiece is None:
                        if self.check_coast_clear_ver(startxy, destxy) \
                                                    or self.check_coast_clear_hor(startxy, destxy):
                            move_ok = True

                    # if a non-cannon is trying to capture a piece
                    elif endpiece is not None and endpiece.get_color() != startpiece.get_color():
                        if start_rank == 'Car' and (self.check_coast_clear_ver(startxy, destxy)
                                                    or self.check_coast_clear_hor(startxy, destxy)):
                            endpiece.set_vitals(False)
                            if endpiece.get_rank() == 'King':
                                self._game_state = self._turn.upper() + '_WON'
                            move_ok = True
                        elif start_rank == 'Elephant' and self.check_coast_clear_dia(startxy, destxy):
                            endpiece.set_vitals(False)
                            if endpiece.get_rank() == 'King':
                                self._game_state = self._turn.upper() + '_WON'
                            move_ok = True
                        elif start_rank == 'Horse' and self.check_coast_clear_horse(startxy, destxy):
                            endpiece.set_vitals(False)
                            if endpiece.get_rank() == 'King':
                                self._game_state = self._turn.upper() + '_WON'
                            move_ok = True
                        elif start_rank == 'Soldier' or start_rank == 'Bodyguard' or start_rank == 'King':
                            endpiece.set_vitals(False)
                            if endpiece.get_rank() == 'King':
                                self._game_state = self._turn.upper() + '_WON'
                            move_ok = True

                    # if the start piece is just moving
                    elif endpiece is None:
                        if start_rank == 'Car' and (self.check_coast_clear_ver(startxy, destxy)
                                                    or self.check_coast_clear_hor(startxy, destxy)):
                            move_ok = True
                        elif start_rank == 'Elephant' and self.check_coast_clear_dia(startxy, destxy):
                            move_ok = True
                        elif start_rank == 'Horse' and self.check_coast_clear_horse(startxy, destxy):
                            move_ok = True
                        elif start_rank == 'Soldier' or start_rank == 'Bodyguard' or start_rank == 'King':
                            move_ok = True

                if move_ok:
                    # update starting piece position to end destination
                    self._board[destxy[0]][destxy[1]] = startpiece
                    startpiece.set_loc_x(destxy[0])
                    startpiece.set_loc_y(destxy[1])
                    # change starting spot on board to None
                    self._board[startxy[0]][startxy[1]] = None
                    move_complete = True

                if move_complete:
                    # update game_status and turn
                    if self._turn == 'Red':
                        self.set_whose_turn('Black')
                    elif self._turn == 'Black':
                        self.set_whose_turn('Red')

                    # check for checkmate
                    self._checkmate = self.is_in_check('Black')
                    if self._checkmate:
                        self._game_state = 'RED_WON'

                    self._checkmate = self.is_in_check('Red')
                    if self._checkmate:
                        self._game_state = 'BLACK_WON'

        return move_complete


# board = XiangqiGame()
# print(board.convert_to_xy('a3'))
# board.find_location('King', 'Black')
# board._board[7][7].cannon_valid_kill_move([7,7],[5,6])
# print(board.make_move('a1', 'a2'))
# print(board.make_move('g10', 'c6'))
# board.check_tester([9,4])
