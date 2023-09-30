# Author: Louis Hwang
# GitHub username: hwanglosu
# Date: 3/10/2023
# Description: Class called Checkers that allows two people to play the game of Checkers
#              with modified rules. This program does not prevent standard pieces from moving backwards and
#              assumes a triple king jump on two or more pieces is only one move.
#              In addition, mandatory jumps are not enforced in this program.

class CheckerPiece:
    """Represents a checker piece on a checkers board. This class will be called by the Checkers class."""

    def __init__(self, color):
        """
        Creates a checker piece object with a color and a type, with type 1 being the starting piece
        type, type 2 being a King, and type 3 being a triple King. The color is passed as a parameter.
        """
        self._color = color
        self._type = 1

    def get_color(self):
        """Returns the color of the checker piece"""
        return self._color

    def get_type(self):
        """Returns the type of the checker piece. The type will be returned as a string."""
        names = ["Standard", "king", "Triple_King"]
        return names[self._type - 1]

    def promote(self):
        """Turns the checker piece into a king or triple king when appropriate"""
        self._type += 1


class Checkers:
    """
    Represents a game of checkers with a board and a dictionary of players. Utilizes CheckerPiece and Player classes
    to create objects for the checker game to function.
    """

    def __init__(self):
        """
        The constructor for Checkers class. Creates a board with the starting positions for all pieces.
        Pieces that are not None in the board are created using CheckerPiece class.
        self._players will contain objects from Players class in its values.
        All data members in this class are private.
        """
        self._board = [[CheckerPiece("White") if column % 2 == 1 else None for column in range(8)],
                       [CheckerPiece("White") if column % 2 == 0 else None for column in range(8)],
                       [CheckerPiece("White") if column % 2 == 1 else None for column in range(8)],
                       [None for column in range(8)],
                       [None for column in range(8)],
                       [CheckerPiece("Black") if column % 2 == 0 else None for column in range(8)],
                       [CheckerPiece("Black") if column % 2 == 1 else None for column in range(8)],
                       [CheckerPiece("Black") if column % 2 == 0 else None for column in range(8)]]
        self._players = {}
        self._turn = "Black"
        self._jump = "off"      # If on, then player can do multiple jumps

    def get_board(self):
        """Returns the contents of the game board"""
        return self._board

    def create_player(self, player_name, piece_color):
        """
        Takes as parameter the player_name and piece_color that the player wants to play with
        and puts the player object into self._players dictionary with the player name as the key and
        the object as the value. Also returns the player object.
        """
        if len(self._players) == 2:
            return "There are already two players"
        elif piece_color != "White" and piece_color != "Black":
            return "Invalid piece color"
        else:
            if len(self._players) == 1:
                for player in self._players:
                    if self._players[player].get_checker_color() == piece_color:
                        return piece_color + " has already been taken"
            self._players[player_name] = Player(player_name, piece_color)
            return self._players[player_name]

    def play_game(self, player_name, start_loc, destination_loc):
        """
        Simulates a move of a player's piece. Checks to see if a move is valid or invalid.
        Raises an exception for invalid moves and modifies self._board and other data attributes for
        CheckerPiece or Player objects as appropriate.
        """
        # Check if player name is valid
        try:
            if self._players[player_name].get_checker_color() != self._turn and self._jump == "off":
                raise OutofTurn
        except KeyError:
            raise InvalidPlayer

        # Check if white square or an empty square is selected
        if self._board[start_loc[0]][start_loc[1]] is None:  # If square selected is None
            raise InvalidSquare
        if start_loc[0] < 0 or start_loc[1] < 0 or destination_loc[0] < 0 or destination_loc[1] < 0 or \
                start_loc[0] > 7 or start_loc[1] > 7 or destination_loc[0] > 7 or destination_loc[1] > 7:
            raise InvalidSquare

        # Check if player does not own the piece on selected square
        try:
            if self._players[player_name].get_checker_color() != self._board[start_loc[0]][start_loc[1]].get_color():
                raise InvalidSquare
            # Regular move one space by any piece
            if abs(destination_loc[0]-start_loc[0]) == 1 and abs(destination_loc[1]-start_loc[1]) == 1:
                try:
                    if self._players[player_name].get_checker_color() != self._turn and self._jump == "on":
                        raise OutofTurn
                except KeyError:
                    raise InvalidPlayer
                if self._board[destination_loc[0]][destination_loc[1]] is not None:
                    raise InvalidSquare
                else:   # Make the move
                    self._board[start_loc[0]][start_loc[1]],self._board[destination_loc[0]][destination_loc[1]] = \
                        self._board[destination_loc[0]][destination_loc[1]], self._board[start_loc[0]][start_loc[1]]

                    # Check for promotion
                    if (destination_loc[0] == 7 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard") or \
                            (destination_loc[0] == 0 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard"):
                        self._board[destination_loc[0]][destination_loc[1]].promote()  # Standard to king
                        self._players[player_name].increment_king_count()
                    elif (destination_loc[0] == 0 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king") or \
                         (destination_loc[0] == 7 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king"):
                        self._board[destination_loc[0]][destination_loc[1]].promote()  # king to triple king
                        self._players[player_name].increment_triple_king_count()
                        self._players[player_name].decrement_king_count()
                    if self._turn == "White":
                        self._turn = "Black"
                    elif self._turn == "Black":
                        self._turn = "White"
                    self._jump = "off"
                    return 0
            # Single jump by any piece, note this does not check if a standard piece is jumping backwards
            elif abs(destination_loc[1]-start_loc[1]) == 2:
                try:
                    if self._players[player_name].get_checker_color() != self._turn and self._jump == "on":
                        self._turn = self._players[player_name].get_checker_color()
                except KeyError:
                    raise InvalidPlayer
                if (self._board[start_loc[0]+(destination_loc[0]-start_loc[0])//2][start_loc[1]+(destination_loc[1]-start_loc[1])//2].get_color()) != \
                        self._players[player_name].get_checker_color() and not self._board[destination_loc[0]][destination_loc[1]]:
                    self._board[start_loc[0]][start_loc[1]], self._board[destination_loc[0]][destination_loc[1]] = \
                        self._board[destination_loc[0]][destination_loc[1]], self._board[start_loc[0]][start_loc[1]]
                    captured_piece = self._board[start_loc[0]+(destination_loc[0]-start_loc[0])//2][start_loc[1]+(destination_loc[1]-start_loc[1])//2]
                    self._board[start_loc[0]+(destination_loc[0]-start_loc[0])//2][start_loc[1]+(destination_loc[1]-start_loc[1])//2] = None
                    self._players[player_name].increment_captured_pieces_count()

                    # Decrement king/triple king count for appropriate player
                    for player in self._players.values():
                        if player.get_checker_color() != self._turn:
                            if captured_piece.get_type() == "king":
                                player.decrement_king_count()
                            elif captured_piece.get_type() == "Triple_King":
                                player.decrement_triple_king_count()

                    # Check for promotion
                    if (destination_loc[0] == 7 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard") or \
                            (destination_loc[0] == 0 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard"):
                        self._board[destination_loc[0]][destination_loc[1]].promote()  # Standard to king
                        self._players[player_name].increment_king_count()
                    elif (destination_loc[0] == 0 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king") or \
                            (destination_loc[0] == 7 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king"):
                        self._board[destination_loc[0]][destination_loc[1]].promote()  # King to triple king
                        self._players[player_name].increment_triple_king_count()
                        self._players[player_name].decrement_king_count()
                    if self._turn == "White":
                        self._turn = "Black"
                    elif self._turn == "Black":
                        self._turn = "White"
                    self._jump = "on"
                    return 1
            # Otherwise consider king and triple king's jumping ability through a straight diagonal
            elif abs(destination_loc[0]-start_loc[0]) == abs(destination_loc[1]-start_loc[1]) and not self._board[destination_loc[0]][destination_loc[1]]:
                try:
                    if self._players[player_name].get_checker_color() != self._turn and self._jump == "on":
                        raise OutofTurn
                except KeyError:
                    raise InvalidPlayer
                self._board[start_loc[0]][start_loc[1]], self._board[destination_loc[0]][destination_loc[1]] = \
                    self._board[destination_loc[0]][destination_loc[1]], self._board[start_loc[0]][start_loc[1]]
                temp_spot = [start_loc[0], start_loc[1]]
                # Get the signs of which direction to move, for example [-1,-1] means up 1 and left 1
                difference = [(destination_loc[0]-start_loc[0]) // (abs(destination_loc[0]-start_loc[0])),
                              (destination_loc[1]-start_loc[1]) // (abs(destination_loc[1]-start_loc[1]))]
                # To look at each square between start and destination
                captured_pieces = 0
                for count in range(abs(destination_loc[0]-start_loc[0])):
                    temp_spot[0] += difference[0]
                    temp_spot[1] += difference[1]
                    try:
                        if self._board[temp_spot[0]][temp_spot[1]].get_color() != self._turn:
                            captured_pieces += 1
                            # Decrement king/triple king count for appropriate player
                            for player in self._players.values():
                                if player.get_checker_color() != self._turn:
                                    if self._board[temp_spot[0]][temp_spot[1]].get_type() == "king":
                                        player.decrement_king_count()
                                    elif self._board[temp_spot[0]][temp_spot[1]].get_type() == "Triple_King":
                                        player.decrement_triple_king_count()
                            self._board[temp_spot[0]][temp_spot[1]] = None
                            self._players[player_name].increment_captured_pieces_count()
                    except AttributeError:
                        continue
                # Check for promotion
                if (destination_loc[0] == 7 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard") or \
                    (destination_loc[0] == 0 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "Standard"):
                    self._board[destination_loc[0]][destination_loc[1]].promote()  # Standard to king
                    self._players[player_name].increment_king_count()
                elif (destination_loc[0] == 0 and self._turn == "White" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king") or \
                        (destination_loc[0] == 7 and self._turn == "Black" and self._board[destination_loc[0]][destination_loc[1]].get_type() == "king"):
                    self._board[destination_loc[0]][destination_loc[1]].promote()  # King to triple king
                    self._players[player_name].increment_triple_king_count()
                    self._players[player_name].decrement_king_count()
                if self._turn == "White":
                    self._turn = "Black"
                elif self._turn == "Black":
                    self._turn = "White"
                return captured_pieces

        except IndexError:          # square location given in any statement is out of bounds
            raise InvalidSquare
        except AttributeError:      # Calling get color or type method on square with None
            raise InvalidSquare
        else:
            raise InvalidSquare

    def get_checker_details(self, square_location):
        """
        Takes as parameter a square_location given as a tuple and returns the checker details
        present in the square_location in self._board. Returns None if no piece is on that square.
        """
        if square_location[0] < 0 or square_location[1] < 0 or square_location[0] > 7 or square_location[1] > 7:
            raise InvalidSquare
        else:
            try:
                if (self._board[square_location[0]][square_location[1]]).get_type() == "Standard":
                    return (self._board[square_location[0]][square_location[1]]).get_color()
                else:
                    return (self._board[square_location[0]][square_location[1]]).get_color() + "_" + \
                           (self._board[square_location[0]][square_location[1]]).get_type()
            except AttributeError:
                return None

    def print_board(self):
        """
        Prints the current board in the form of an array, with one list containing eight lists,
        each of the eight lists representing a row of the board. Prints out the contents of self._board
        except that the colors instead of the objects are displayed out instead.
        """
        new_row = []
        for row in range(len(self._board)):
            for column in range(len(self._board[row])):
                color = self.get_checker_details([row, column])
                if color == 'White':
                    new_row.append('w')
                elif color == 'White_king':
                    new_row.append('W')
                elif color == 'Black' or color == 'Black_king':
                    new_row.append('b')
                else:
                    new_row.append(' ')
            print(new_row)
            new_row = []

    def game_winner(self):
        """Returns the name of the player who won the game, or game has not ended if there is no winner yet"""
        for player in self._players:
            if self._players[player].get_captured_pieces_count() == 12:
                return player
        return "Game has not ended"

class Player:
    """Represents a player in the game. Used by Checkers class to simulate a checkers game."""

    def __init__(self, player_name, checker_color):
        """
        The constructor for Player class. Creates a player with a name and a checker
        color as well as a captured pieces count. All data members in this class are private.
        """
        self._player_name = player_name
        self._checker_color = checker_color
        self._captured_pieces_count = 0
        self._king_count = 0
        self._triple_king_count = 0

    def get_checker_color(self):
        """Returns the checker color for the player object"""
        return self._checker_color

    def increment_captured_pieces_count(self):
        """Increments the player's captured pieces count"""
        self._captured_pieces_count += 1

    def get_captured_pieces_count(self):
        """Returns the number of opponent pieces that the player has captured"""
        return self._captured_pieces_count

    def get_king_count(self):
        """Returns the number of king pieces that the player has"""
        return self._king_count

    def get_triple_king_count(self):
        """Returns the number of triple king pieces that the player has"""
        return self._triple_king_count

    def increment_king_count(self):
        """Increments the player's king count"""
        self._king_count += 1

    def decrement_king_count(self):
        """Decrements the player's king count"""
        self._king_count -= 1

    def increment_triple_king_count(self):
        """Increments the player's triple king count"""
        self._triple_king_count += 1

    def decrement_triple_king_count(self):
        """Decrements the player's triple king count"""
        self._triple_king_count -= 1


class OutofTurn(Exception):
    """
    Defines the exception class used by Checker's play_game method if a player
    attempts to move a piece out of turn.
    """
    pass


class InvalidSquare(Exception):
    """
    Defines the exception class used by Checker's play_game method if a player does not own the checker
    present in the square_location or if the square_location does not exist on the board.
    """
    pass


class InvalidPlayer(Exception):
    """
    Defines the exception class used by Checker's play_game method if a player name is not valid.
    """
    pass


if __name__ == "__main__":
    # Demonstrates the implementation of the checkers game.
    game = Checkers()
    print("Welcome to the Checkers game. The starting board is printed below.\n")
    game.print_board()
    Player1 = game.create_player("Adam", "White")
    Player2 = game.create_player("Lucy", "Black")
    input('To run a simulation, press enter.')

    print('')
    game.play_game("Lucy", (5, 0), (4, 1))
    game.print_board()
    input('Turn 1: Black has moved. Press enter to continue.')

    print('')
    game.play_game("Adam", (2, 1), (3, 0))
    game.print_board()
    input('Turn 2: White has moved. Press enter to continue.')

    print('')
    game.play_game("Lucy", (5, 2), (4, 3))
    game.print_board()
    input('Turn 3: Black has moved. Press enter to continue.')

    print('')
    game.play_game("Adam", (2, 7), (3, 6))
    game.print_board()
    input('Turn 4: White has moved. Press enter to continue.')

    print('')
    game.play_game("Lucy", (6, 1), (5, 0))
    game.print_board()
    input('Turn 5: Black has moved. Press enter to continue.')

    print('')
    game.play_game("Adam", (3, 6), (4, 7))
    game.print_board()
    input('Turn 6: White has moved. Press enter to continue.')

    print('')
    game.play_game("Lucy", (7, 0), (6, 1))
    game.print_board()
    input('Turn 7: Black has moved. Press enter to continue.')

    print('')
    game.play_game("Adam", (3, 0), (5, 2))
    game.print_board()
    input('Turn 8: White has captured a piece and is performing a double jump. Press enter to continue.')

    print('')
    game.play_game("Adam", (5, 2), (7, 0))
    game.print_board()
    print('Turn 8: White has captured another piece in a double jump and has been promoted '
          'to king. End of simulation')
