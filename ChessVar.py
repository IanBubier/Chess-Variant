# Author: Ian Bubier
# GitHub username: IanBubier
# Date: 12/07/2023
# Description: A variant chess game in which the objective is to capture all of an opponent's pieces of a single type.
#     For example, the game could be won by capturing the queen, or all pawns, or both rooks, etc. There is no check,
#     checkmate, castling, en passant, or pawn promotion. Includes class ChessVar for the game and board and class Piece
#     and inheriting classes for the pieces, along with required methods for each.

class ChessVar:
    """Represents a variant chess game. Monitors game state, turns, active player, pieces in play, and occupied squares.
    Includes a get method for game state, a get method for game turn, a method for players to make moves and a method to
    print the board. Communicates with different Pieces to assess legality of moves."""

    def __init__(self):
        self._game_state = 'UNFINISHED'  # 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON'
        self._turn = 0  # Increments at game start and end of every 'black' player phase.
        self._active_player = 'white'  # 'white' or 'black'
        self._white_pieces = {'king': 1, 'queen': 1, 'bishop': 2, 'knight': 2, 'rook': 2, 'pawn': 8}
        self._black_pieces = {'king': 1, 'queen': 1, 'bishop': 2, 'knight': 2, 'rook': 2, 'pawn': 8}
        self._occupied_squares = {'e1': King('white'), 'd1': Queen('white'), 'c1': Bishop('white'),
                                  'f1': Bishop('white'), 'b1': Knight('white'), 'g1': Knight('white'),
                                  'a1': Rook('white'), 'h1': Rook('white'), 'a2': Pawn('a2', 'white'),
                                  'b2': Pawn('b2', 'white'), 'c2': Pawn('c2', 'white'), 'd2': Pawn('d2', 'white'),
                                  'e2': Pawn('e2', 'white'), 'f2': Pawn('f2', 'white'), 'g2': Pawn('g2', 'white'),
                                  'h2': Pawn('h2', 'white'), 'e8': King('black'), 'd8': Queen('black'),
                                  'c8': Bishop('black'), 'f8': Bishop('black'), 'b8': Knight('black'),
                                  'g8': Knight('black'), 'a8': Rook('black'), 'h8': Rook('black'),
                                  'a7': Pawn('a7', 'black'), 'b7': Pawn('b7', 'black'), 'c7': Pawn('c7', 'black'),
                                  'd7': Pawn('d7', 'black'), 'e7': Pawn('e7', 'black'), 'f7': Pawn('f7', 'black'),
                                  'g7': Pawn('g7', 'black'), 'h7': Pawn('h7', 'black')}  # {'square': class(Piece)}
        # self.print_board()  # Uncomment to print board at game start.
        self._turn += 1

    def get_game_state(self):
        """Returns 'UNFINISHED', 'WHITE_WON', or 'BLACK_WON' depending on game state."""
        return self._game_state

    def get_turn(self):
        """Returns turn number."""
        return self._turn

    # The only method a player should need to use.
    def make_move(self, move_from, move_to):  # Strings, case sensitive. e.g. 'd4', 'f6'
        """Attempts to move a piece from one square to another. If the game is over, the wrong player is moving, the
        starting square is empty, or the move is illegal for any reason, returns False. Otherwise, moves the piece,
        removes any captured piece, updates the game state, updates the turn, and returns True."""
        if self._game_state == 'UNFINISHED' and move_from in self._occupied_squares and \
                self._occupied_squares[move_from].get_color() == self._active_player and move_to in \
                self._occupied_squares[move_from].move_range(move_from, self._occupied_squares):
            if move_to in self._occupied_squares:
                if self._active_player == 'white':
                    self._black_pieces[self._occupied_squares[move_to].get_name()] -= 1
                    if self._black_pieces[self._occupied_squares[move_to].get_name()] == 0:
                        self._occupied_squares[move_to] = self._occupied_squares[move_from]
                        del self._occupied_squares[move_from]
                        self._game_state = 'WHITE_WON'
                        # self.print_board()    # Uncomment to print board after move.
                        return True
                else:
                    self._white_pieces[self._occupied_squares[move_to].get_name()] -= 1
                    if self._white_pieces[self._occupied_squares[move_to].get_name()] == 0:
                        self._occupied_squares[move_to] = self._occupied_squares[move_from]
                        del self._occupied_squares[move_from]
                        self._game_state = 'BLACK_WON'
                        # self.print_board()    # Uncomment to print board after move.
                        return True
            self._occupied_squares[move_to] = self._occupied_squares[move_from]
            del self._occupied_squares[move_from]
            # self.print_board()    # Uncomment to print board after move.
            if self._active_player == 'black':
                self._active_player = 'white'
                self._turn += 1
            else:
                self._active_player = 'black'
            return True
        return False

    def print_board(self):
        """Prints the board with labels for game state, turn, and rows and columns. Uncomment print_board calls in
        __init__ and make_move to print board at game start and after each move."""

        # Game state and turn labels.
        print("")
        if self._turn == 0:
            print("Game Start")
        elif self._game_state == 'WHITE_WON':
            print("Turn " + str(self.get_turn()) + " White Victory")
        elif self._game_state == 'BLACK_WON':
            print("Turn " + str(self.get_turn()) + " Black Victory")
        elif self._active_player == 'white':
            print("Turn " + str(self.get_turn()) + " White Phase")
        else:
            print("Turn " + str(self.get_turn()) + " Black Phase")

        # Print actual board.
        print("   a   b   c   d   e   f   g   h  ")
        for row in range(8, 0, -1):
            row_print = str(row) + " "
            for column in range(ord('a'), ord('i')):
                if chr(column) + str(row) not in self._occupied_squares:
                    row_print += " -- "
                else:
                    row_print += self._occupied_squares[(chr(column) + str(row))].get_symbol()
            row_print += " " + str(row)
            print(row_print)
        print("   a   b   c   d   e   f   g   h  ")


class Piece:
    """Represents a chess piece with color and name. Communicates with ChessVar to get locations of particular pieces.
    Inheriting classes represent specific types of pieces with specific move ranges and methods to get those ranges.
    Piece instances are never used; the class is only for inheritance. """

    def __init__(self, color, name, symbol):
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = 'w' + symbol
        else:
            self._symbol = 'b' + symbol

    def get_color(self):
        """Returns color."""
        return self._color

    def get_name(self):
        """Returns name."""
        return self._name

    def get_symbol(self):
        """Returns symbol."""
        return self._symbol


class King(Piece):
    """Represents a King, which may move one square in any direction."""

    def __init__(self, color, name='king', symbol='K '):
        super().__init__(color, name, symbol)
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Move right.
        if ord('a') <= (ord(location[0])) + 1 <= ord('h'):
            if chr((ord(location[0])) + 1) + location[1] not in occupied_squares \
                    or occupied_squares[chr((ord(location[0])) + 1) + location[1]].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + location[1])

        # Move left.
        if ord('a') <= (ord(location[0])) - 1 <= ord('h'):
            if chr((ord(location[0])) - 1) + location[1] not in occupied_squares \
                    or occupied_squares[chr((ord(location[0])) - 1) + location[1]].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + location[1])

        # Move up.
        if 1 <= int(location[1]) + 1 <= 8:
            if location[0] + str(int(location[1]) + 1) not in occupied_squares \
                    or occupied_squares[location[0] + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(location[0] + str(int(location[1]) + 1))

        # Move down.
        if 1 <= int(location[1]) - 1 <= 8:
            if location[0] + str(int(location[1]) - 1) not in occupied_squares \
                    or occupied_squares[location[0] + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(location[0] + str(int(location[1]) - 1))

        # Move right-up.
        if ord('a') <= (ord(location[0])) + 1 <= ord('h') and 1 <= int(location[1]) + 1 <= 8:
            if chr(ord(location[0]) + 1) + str(int(location[1]) + 1) not in occupied_squares \
                    or occupied_squares[chr(ord(location[0]) + 1)
                                        + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) + 1))

        # Move right-down.
        if ord('a') <= (ord(location[0])) + 1 <= ord('h') and 1 <= int(location[1]) - 1 <= 8:
            if chr(ord(location[0]) + 1) + str(int(location[1]) - 1) not in occupied_squares \
                    or occupied_squares[chr(ord(location[0]) + 1)
                                        + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) - 1))

        # Move left-up.
        if ord('a') <= (ord(location[0])) - 1 <= ord('h') and 1 <= int(location[1]) + 1 <= 8:
            if chr(ord(location[0]) - 1) + str(int(location[1]) + 1) not in occupied_squares \
                    or occupied_squares[chr(ord(location[0]) - 1)
                                        + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) + 1))

        # Move left-down.
        if ord('a') <= (ord(location[0])) - 1 <= ord('h') and 1 <= int(location[1]) - 1 <= 8:
            if chr(ord(location[0]) - 1) + str(int(location[1]) - 1) not in occupied_squares \
                    or occupied_squares[chr(ord(location[0]) - 1)
                                        + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) - 1))

        return piece_range


class Queen(Piece):
    """Represents a Queen, which may move any number of squares in any direction."""

    def __init__(self, color, name='queen', symbol='Q '):
        super().__init__(color, name, symbol)
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Moves right.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h'):
                if chr(square) + location[1] in occupied_squares \
                        and occupied_squares[chr(square) + location[1]].get_color() == self._color:
                    break
                piece_range.add(chr(square) + location[1])
                if chr(square) + location[1] in occupied_squares:
                    break

        # Moves left.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h'):
                if chr(square) + location[1] in occupied_squares \
                        and occupied_squares[chr(square) + location[1]].get_color() == self._color:
                    break
                piece_range.add(chr(square) + location[1])
                if chr(square) + location[1] in occupied_squares:
                    break

        # Moves up.
        for square in range(int(location[1]) + 1, 9):
            if 1 <= square <= 8:
                if location[0] + str(square) in occupied_squares \
                        and occupied_squares[location[0] + str(square)].get_color() == self._color:
                    break
                piece_range.add(location[0] + str(square))
                if location[0] + str(square) in occupied_squares:
                    break

        # Moves down.
        for square in range(int(location[1]) - 1, 0, - 1):
            if 1 <= square <= 8:
                if location[0] + str(square) in occupied_squares \
                        and occupied_squares[location[0] + str(square)].get_color() == self._color:
                    break
                piece_range.add(location[0] + str(square))
                if location[0] + str(square) in occupied_squares:
                    break

        # Moves right-up.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) + square - ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) + square -
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) + square - ord(location[0])))
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares:
                    break

        # Moves right-down.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) - square + ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) - square +
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) - square + ord(location[0])))
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares:
                    break

        # Moves left-up.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) + square - ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) + square -
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) + square - ord(location[0])))
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares:
                    break

        # Moves left-down.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) - square + ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) - square +
                                                               ord(location[0]))].get_color() == self._color:
                    break
            piece_range.add(chr(square) + str(int(location[1]) - square + ord(location[0])))
            if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares:
                break

        return piece_range


class Bishop(Piece):
    """Represents a Bishop, which may move any number of squares diagonally."""

    def __init__(self, color, name='bishop', symbol='B '):
        super().__init__(color, name, symbol)
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Moves right-up.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) + square - ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) + square -
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) + square - ord(location[0])))
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares:
                    break

        # Moves right-down.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) - square + ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) - square +
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) - square + ord(location[0])))
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares:
                    break

        # Moves left-up.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) + square - ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) + square -
                                                               ord(location[0]))].get_color() == self._color:
                    break
                piece_range.add(chr(square) + str(int(location[1]) + square - ord(location[0])))
                if chr(square) + str(int(location[1]) + square - ord(location[0])) in occupied_squares:
                    break

        # Moves left-down.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h') and 1 <= int(location[1]) - square + ord(location[0]) <= 8:
                if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares \
                        and occupied_squares[chr(square) + str(int(location[1]) - square +
                                                               ord(location[0]))].get_color() == self._color:
                    break
            piece_range.add(chr(square) + str(int(location[1]) - square + ord(location[0])))
            if chr(square) + str(int(location[1]) - square + ord(location[0])) in occupied_squares:
                break

        return piece_range


class Knight(Piece):
    """Represents a Knight, which may move two squares vertically and one horizontally, or two horizontally and one
    vertically."""

    def __init__(self, color, name='knight', symbol='Kn'):
        super().__init__(color, name, symbol)
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Move two right, one up.
        if ord('a') <= (ord(location[0])) + 2 <= ord('h') and 1 <= int(location[1]) + 1 <= 8:
            if chr(ord(location[0]) + 2) + str(int(location[1]) + 1) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) + 2) + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 2) + str(int(location[1]) + 1))

        # Move two right, one down.
        if ord('a') <= (ord(location[0])) + 2 <= ord('h') and 1 <= int(location[1]) - 1 <= 8:
            if chr(ord(location[0]) + 2) + str(int(location[1]) - 1) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) + 2) + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 2) + str(int(location[1]) - 1))

        # Move two left, one up.
        if ord('a') <= (ord(location[0])) - 2 <= ord('h') and 1 <= int(location[1]) + 1 <= 8:
            if chr(ord(location[0]) - 2) + str(int(location[1]) + 1) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) - 2) + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 2) + str(int(location[1]) + 1))

        # Move two left, one down.
        if ord('a') <= (ord(location[0])) - 2 <= ord('h') and 1 <= int(location[1]) - 1 <= 8:
            if chr(ord(location[0]) - 2) + str(int(location[1]) - 1) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) - 2) + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 2) + str(int(location[1]) - 1))

        # Move one right, two up.
        if ord('a') <= (ord(location[0])) + 1 <= ord('h') and 1 <= int(location[1]) + 2 <= 8:
            if chr(ord(location[0]) + 1) + str(int(location[1]) + 2) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) + 1) + str(int(location[1]) + 2)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) + 2))

        # Move one right, two down.
        if ord('a') <= (ord(location[0])) + 1 <= ord('h') and 1 <= int(location[1]) - 2 <= 8:
            if chr(ord(location[0]) + 1) + str(int(location[1]) - 2) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) + 1) + str(int(location[1]) - 2)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) - 2))

        # Move one left, two up.
        if ord('a') <= (ord(location[0])) - 1 <= ord('h') and 1 <= int(location[1]) + 2 <= 8:
            if chr(ord(location[0]) - 1) + str(int(location[1]) + 2) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) - 1) + str(int(location[1]) + 2)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) + 2))

        # Move one left, two down.
        if ord('a') <= (ord(location[0])) - 1 <= ord('h') and 1 <= int(location[1]) - 2 <= 8:
            if chr(ord(location[0]) - 1) + str(int(location[1]) - 2) not in occupied_squares or \
                    occupied_squares[chr(ord(location[0]) - 1) + str(int(location[1]) - 2)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) - 2))

        return piece_range


class Rook(Piece):
    """Represents a Rook, which may move any number of squares vertically or horizontally."""

    def __init__(self, color, name='rook', symbol='R '):
        super().__init__(color, name, symbol)
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Moves right.
        for square in range(ord(location[0]) + 1, ord('i')):
            if ord('a') <= square <= ord('h'):
                if chr(square) + location[1] in occupied_squares \
                        and occupied_squares[chr(square) + location[1]].get_color() == self._color:
                    break
                piece_range.add(chr(square) + location[1])
                if chr(square) + location[1] in occupied_squares:
                    break

        # Moves left.
        for square in range(ord(location[0]) - 1, ord('a') - 1, - 1):
            if ord('a') <= square <= ord('h'):
                if chr(square) + location[1] in occupied_squares \
                        and occupied_squares[chr(square) + location[1]].get_color() == self._color:
                    break
                piece_range.add(chr(square) + location[1])
                if chr(square) + location[1] in occupied_squares:
                    break

        # Moves up.
        for square in range(int(location[1]) + 1, 9):
            if 1 <= square <= 8:
                if location[0] + str(square) in occupied_squares \
                        and occupied_squares[location[0] + str(square)].get_color() == self._color:
                    break
                piece_range.add(location[0] + str(square))
                if location[0] + str(square) in occupied_squares:
                    break

        # Moves down.
        for square in range(int(location[1]) - 1, 0, - 1):
            if 1 <= square <= 8:
                if location[0] + str(square) in occupied_squares \
                        and occupied_squares[location[0] + str(square)].get_color() == self._color:
                    break
                piece_range.add(location[0] + str(square))
                if location[0] + str(square) in occupied_squares:
                    break

        return piece_range


class Pawn(Piece):
    """Represent a Pawn, which may move one square forward, or one diagonally to capture, or two forward on each
    player's first turn."""

    def __init__(self, start_square, color, name='pawn', symbol='p '):
        super().__init__(color, name, symbol)
        self._start_square = start_square
        self._color = color  # 'white' or 'black'
        self._name = name
        if color == 'white':
            self._symbol = ' w' + symbol
        else:
            self._symbol = ' b' + symbol

    def move_range(self, location, occupied_squares):
        """Compares allowed move range with occupied squares and board dimensions to return set of moves in range."""
        piece_range = set()

        # Move two forward on first move.
        if location == self._start_square:
            if self._color == 'white' and location[0] + str(int(location[1]) + 2) not in occupied_squares:
                piece_range.add(location[0] + str(int(location[1]) + 2))
            if self._color == 'black' and location[0] + str(int(location[1]) - 2) not in occupied_squares:
                piece_range.add(location[0] + str(int(location[1]) - 2))

        # Standard move forward for white.
        if 1 <= int(location[1]) + 1 <= 8 and self._color == 'white' and location[0] + str(int(location[1]) + 1) \
                not in occupied_squares:
            piece_range.add(location[0] + str(int(location[1]) + 1))

        # Standard move forward for black.
        if 1 <= int(location[1]) - 1 <= 8 and self._color == 'black' and location[0] + str(int(location[1]) - 1) \
                not in occupied_squares:
            piece_range.add(location[0] + str(int(location[1]) - 1))

        # Diagonal capture for white.
        if self._color == 'white':
            if chr(ord(location[0]) + 1) + str(int(location[1]) + 1) in occupied_squares and \
                    occupied_squares[chr(ord(location[0]) + 1) + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) + 1))
            if chr(ord(location[0]) - 1) + str(int(location[1]) + 1) in occupied_squares and \
                    occupied_squares[chr(ord(location[0]) - 1) + str(int(location[1]) + 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) + 1))

        # Diagonal capture for black.
        if self._color == 'black':
            if chr(ord(location[0]) + 1) + str(int(location[1]) - 1) in occupied_squares and \
                    occupied_squares[chr(ord(location[0]) + 1) + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) + 1) + str(int(location[1]) - 1))
            if chr(ord(location[0]) - 1) + str(int(location[1]) - 1) in occupied_squares and \
                    occupied_squares[chr(ord(location[0]) - 1) + str(int(location[1]) - 1)].get_color() != self._color:
                piece_range.add(chr(ord(location[0]) - 1) + str(int(location[1]) - 1))

        return piece_range


# It is possible for the Piece classes' respective move_range methods to ignore the color of the other pieces in their
# range and let make_move rule out moves onto pieces of the same color. This could be done with a couple lines of code
# in make_move; it would be more efficient and much easier to code. I have the move_range methods check color so that
# the returned piece_range sets contain exclusively legal moves, which might make things easier on the as-yet unwritten
# chess-playing program I think might be fun to experiment with.
