# BATTLESHIP. DOCUMENTATION

# We will define three generic classes to make the objects:
    # class 'Ship'
    # class 'Board'
    # class 'Battle'

# The class 'Ship' has to be:
# 1. Length in squares: number between 1 and 4 (int) 
# 2. Coordinate: square of the board — row, column — where the ship will be placed (np.array)

# The class 'Board' has to be:
# 1. The board is a Pandas DataFrame: (pd.DataFrame())
# 2. Rows and columns: (np.array() / pd.Series())
# 3. Name: name of the owner of the board (str)

# The class 'Battle' has to be:
# 1. Function StartFight(arg1, arg2): 
    # Params: board1, board2
# 2. Function GetResult(arg1, arg2): staticmethod
    # Params: board1, board2


# How the game works?
    # 1. Start of the program: the user must choose:
        # 1.1. His/Her name: (str(input()))
        # 1.2. The position of the ships in the game board: (int, int)
    # 2. Each time the user choose to place a ship, we must write that ship on the DataFrame:
        # 2.1. We must evaluate if the ship can be placed, following the next criteria:
            # 2.1.1. We will show the current state of the board to the user. By default, all the squares are "."
            # 2.1.2. The whole ship has to be inside the board
            # 2.1.3. The ship must be totally surrounded by empty squares
            # 2.1.4. If the ship can't be placed in the coordinate choosed by the user, we raise an error message
            # 2.1.5. Every ship orientation will be horizontal; it's not allowed to place the ships vertically
        # 2.2. Once we know that the ship can be placed, then we place the ship
            # 2.2.1. The squares of the ship will be represented by an "X"
    # 3. Once the user has no ships remaining to place, we place the CPU ships:
        # 3.1. The CPU board has the same shape as the user board
        # 3.2. The ships of the CPU will be placed randomly, following the same criteria as the user's ships
        # 3.3. When all the ships will be placed, we will print an empty board to the user
    # 4. Game Boards:
        # 4.1. There will be a total of four boards:
            # 4.1.1. User Self Board: board where the user place himself their ships
            # 4.1.2. CPU Self Board: board where the CPU randomly place their ships
            # 4.1.3. User See Board: default board, it will be filled with "X" in the squares where the user impacts CPU
            # 4.1.4. CPU See Board: default board, it will be filled with "X" in the squares where the CPU impacts user    
    # 5. Game mechanics:
        # 5.1. The user always starts the game
        # 5.2. The user will choose a coordinate to shoot at
        # 5.3. We evaluate that coordinate in the CPU Self Board:
            # 5.3.1. If there is a ship, we print an "X" on that square in the User See Board; the user shoot again (5.2)
                # 5.3.1.1. If the number of "X" in the User See Board is equal to 20, then is Game Over and the user Wins
            # 5.3.2. If not, we print an "O" on that square in the User See Board. It's CPU turn
        # 5.4. When the user miss a shot, the CPU will choose a random coordinate to shoot at
        # 5.5. We evaluate that coordinate in the User Self Board:
            # 5.5.1. If there is a ship, we will print "X" in that square in the CPU See Board
                # 5.5.1.1. If the number of "X" in the CPU See Board is equal to 20, is Game Over and the CPU Wins.
            # 5.5.2. If not, the user shoot again (5.2)


from functionality import start_game


# 7. Starting the script
if __name__ == "__main__":
    start_game()