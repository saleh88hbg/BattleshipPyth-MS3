# python code goes here
from random import randint


def random_coordinate(grid_size):
    """
    Helper function to return a random coordinate
    """
    x = randint(0, grid_size - 1)
    y = randint(0, grid_size - 1)
    return (x, y)


def valid_coordinates(x, y, grid_size):
    """
    Verifies that a pair of coordinates are within the grid size
    """
    if 0 <= x < grid_size and 0 <= y < grid_size:
        return True
    
    return False


class Board:
    """
    Main board class. Sets board size, the number of ships,
    the player's name and if it's a computer playing or a player.
    Has methods for adding ships and guesses and printing the board
    """

    def __init__(self, size, num_ships, name, player=False):
        self.size = size
        self.num_ships = num_ships
        self.name = name
        self.player = player
        self.ships = []
        self.guesses = []
        self.populate()

    def print(self):
        """
        Prints the current board state.
        """
        print(f"{self.name}'s Board:")
        for row in self.board:
            print(" ".join(row))

    def guess(self, x, y):
        """
        Makes a guess and marks it on the board
        """
        self.guesses.append((x, y))
        self.board[x][y] = "X"

        if (x, y) in self.ships:
            self.board[x][y] = "*"
            return True
        else:
            return False
    
    def already_guessed(self, x, y):
        """
        Returns true if the coordinates have already been guessed before
        """
        if (x, y) in self.guesses:
            return True
        return False
    
    def last_guess(self):
        """
        Returns the last guess performed on the board
        """
        return self.guesses[-1]

    def populate(self):
        """
        Populates the board with ships
        """
        self.board = [["." for x in range(self.size)] for y in range(self.size)]
        for _ in range(self.num_ships):
            x, y = random_coordinate(self.size)
            while (x, y) in self.ships:
                x, y = random_coordinate(self.size)
            self.ships.append((x, y))
            if self.player:
                self.board[x][y] = "@"

class Game:
    """
    Class to initialize the game, set up the player boards and
    other parameters and handle the playing of it
    """

    def __init__(self, size, num_ships):
        self.size = size
        self.num_ships = num_ships
        self.scores = {"computer": 0, "player": 0}

    def start(self):
        """
        Show welcome screen, initialize the boards and start the game
        """
        self.show_info()
        self.computer_board = Board(self.size, self.num_ships, "Computer", player=False)
        player_name = input("Please enter your name:\n")
        self.player_board = Board(self.size, self.num_ships, player_name, player=True)
        
        self.play()
    
    def play(self):
        """
        Main game loop that takes care of guesses and exits the game if it's
        completed or if the player no longer want to play.
        """
        while True:
            self.print_boards()
            if self.game_over():
                print("Game over!")
                break

            # player guess
            x, y = self.make_guess()
            while not self.valid_guess(x, y):
                x, y = self.make_guess()
            player_hit = self.computer_board.guess(x, y)

            # computer guess
            x, y = random_coordinate(self.size)
            while self.player_board.already_guessed(x, y):
                x, y = random_coordinate(self.size)
            computer_hit = self.player_board.guess(x, y)

            
            self.round_tally(player_hit, computer_hit)
            round_choice = input("Type \"quit\" to quit or anything else to continue.\n")
            if round_choice == "quit":
                break
    
    def make_guess(self):
        """
        Asks the user for 
        """
        x = input("Guess a row:\n")
        y = input("Guess a column:\n")
        while True:
            try:
                x = int(x)
                y = int(y)
                break
            except ValueError:
                print("Row and column must be numbers")

            x = input("Guess a row:\n")
            y = input("Guess a column:\n")

        return (x, y)

    def print_boards(self):
        self.player_board.print()
        self.computer_board.print()

    def valid_guess(self, x, y):
        if not valid_coordinates(x, y, self.size):
            print(f"Row and column must be between 0 and {self.size - 1}")
            return False
        if self.computer_board.already_guessed(x, y):
            print("You cannot guess the same coordinates more than once.")
            return False

        return True

    def game_over(self):
        """
        Checks if a player
        """
        if self.scores["player"] >= self.num_ships or self.scores["computer"] >= self.num_ships:
            return True
        return False

    def round_tally(self, player_hit, computer_hit):
        """
        Output the scores after each round
        """
        print("-" * 35)
        print(f"{self.player_board.name} guessed {self.computer_board.last_guess()}")
        if player_hit:
            self.scores["player"] += 1
            print("That was a hit!")
        else:
            print("That was a miss!")
        print(f"Computer guessed {self.player_board.last_guess()}")
        if computer_hit:
            self.scores["computer"] += 1
            print("That was a hit!")
        else:
            print("That was a miss!")
        print("\nAfter this round, the scores are:")
        print(f"{self.player_board.name}:{self.scores['player']} . Computer:{self.scores['computer']}")
        print("-" * 35)

    def show_info(self):
        """
        Show data here
        """
        print("-" * 35)
        print(" Welcome to the greatest BATTLESHIPS game!")
        print(f" Board Size: {self.size}. Number of ships: {self.num_ships}")
        print(" The top left corner is Row : 0 and Column : 0")
        print(" The @ on the board is your ships")
        print(" The * on the computer board will show the computer sinking ship")
        print("-" * 35)


size = input("Please choose a grid size you want to use?\n")
while True:
    try:
        size = int(size)
        break
    except ValueError:
        print("Row and column must be numbers")
    size = input("Please choose a grid size you want to use?\n")

game = Game(size=size, num_ships=4)
game.start()
