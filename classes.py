# Imports
import pandas as pd
import numpy as np

# Classes

# 2.1. Class 'Ship'
class Ship:
    """Create a ship that will be placed in a board"""

    def __init__(self, numSquares):
        """Params:            
            numSquares: length of the ship (int)
        """
        self.length = numSquares

    def long(self):
        """Returns the length of the ship, based on the square numbers"""
        length = self.length
        return length

    def coordinate(self):
        """Generate a random coordinate, to get a row and a column"""
        square = np.random.randint(low=1, high=11, size=2)
        return square

# 2.2. Class 'Board'
class Board:
    """Create a game board to play the game"""

    def __init__(self, name):
        """Receives a name, related to the board. Method 'df' returns the DataFrame"""
        self.name = name
        self.df = pd.DataFrame(data = np.full((10,10), "."), index=list(range(1,11)), columns=list(range(1,11)))