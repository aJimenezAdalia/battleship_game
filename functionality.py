# Imports
import pandas as pd
import numpy as np
import time
from classes import Ship, Board

# 3. Global Variables

# 3.1. Dictionary to control the amount of available ships to place (User)
ship_dict = {4:1, 3:2, 2:3, 1:4}

# 3.2. Dictionary to control the amount of available ships to place (CPU)
cpu_ship_dict = {4:1, 3:2, 2:3, 1:4}

# 3.3. User hit counter
user_hits = 0

# 3.4. CPU hit counter
cpu_hits = 0

# 3.5. User name
userName = None

# 3.6. User Self Board
userSelfBoard = None

# 3.7. CPU Self Board
cpuSelfBoard = None

# 3.8. List to to avoid the CPU shoots to repeated coordinates
cpu_coordinates_used = [(11, 11)]




# 4.1. Capturing User's name, Creating User Self Board
def start_game():
    """Start the script, and capture the user's name
    
        Returns: 
            user_name: name provided by the user capitalized (str)
            board: Pandas.DataFrame, shape (10,10)
    """
    # Taking the user's name
    user = input("Welcome to BattleShip. Please, write your name: ")
    user = user.capitalize()
    time.sleep(1)
    print(f"{user}, now you'll choose your ships and the positioning over the game board")
    time.sleep(1)

    # Creating User Self Board
    board = Board(user)
    board = board.df

    # Showing the game board to the user
    print(board)
    time.sleep(1)

    # Calling the 'create_ship_user' function    
    return create_ship_user(user_name=user, board=board)


# 4.2. The User choose the kind of ship he wants to place
def create_ship_user(user_name, board):
    """Allow the user to select the length of his next ship to place.
    Call two functions, depending of the ships remaining.
    
        Params:
            user_name: name of the User (str)
            board: board where the user will place their ships (Pandas DataFrame)
            
        Returns:
            When the user have placed all their ships:
                returns 'cpu_placing_ships' function
            When the user have ships remaining:
                returns 'choose_coord' function
    """

    user = user_name

    # We need to capture the user's name in a global variable
    global userName

    if not userName:
        userName = user

    # If the User placed all their ships, we place the CPU ships
    if sum(ship_dict.values()) == 0:
        print("You have placed all your ships. Now the CPU will place their ships.")
        # CPU Self board (name = "CPU")
        cpu_self_board = Board("CPU")
        cpu_self_board = cpu_self_board.df

        # Capturing the UserSelfBoard (all ships placed)
        global userSelfBoard

        userSelfBoard = board

        return cpu_placing_ships("CPU", cpu_self_board)
        

    # If this ship is not the first to place, we print this sentence
    else:
        print(f"{user}, let's place your next ship.")

    # Printing ships remaining
    print(f"Ships remaining:")
    for ship,qty in ship_dict.items():
        print(f"- Length {ship}: {qty}")
    time.sleep(0.5)

    # Asking the user the ship type
    long = None
    while not isinstance(long, int):
        try:      
            long = int(input(f"{user}, choose the length of your ship: 1, 2, 3, 4 \n"))
            time.sleep(1)
            if 1 <= long <= 4:
                break
            else:
                print("Error, the length must be a number between 1 and 4.")
                time.sleep(0.5)
                long = None
        except ValueError:
            input(f"{user}, you must type a number.")
            time.sleep(1)
    

    # Evaluating if the user have remaining ships of this length to place
    if ship_dict[long] == 0:
        print(f"You can't place more ships of length {long}. Please, choose another length.")
        print(f"Ships remaining:")
        for ship,qty in ship_dict.items():
            if qty > 0:
                print(f"- Length {ship}: {qty}")
        return create_ship_user(user, board)
    
    # Creating the ship with the length provided by the user
    ship = Ship(long)

    # Subtracting the ship
    ship_dict[long] -= 1

    
    # Now the user must choose the coordinate of the board where the ship will be placed
    return choose_coord(ship=ship, board=board, name=user)

# 4.3. The User must choose the coordinate where he wants to place the ship
def choose_coord(ship, board, name):
    """Allows the user to select the coordinate of his next ship.
    Call a function to evaluate that coordinate in the user's board.
    
    Params:
        ship: ship that the user wants to place in his board (class Ship)
        board: user's board (Pandas DataFrame)
        name: user's name (str)

    Returns:
        call 'evaluate_placement' function
    """
    row = None
    col = None
    lon = ship.length

    print("Select the coordinate to place your ship (row, column)")

    print(board)

    while True:
        try:
            row = int(input("Choose the row (number between 1 and 10): "))        
        except ValueError:
            print("Error. Row must be a number between 1 and 10.")
            continue
        if row < 1 or row > 10:
            print("Error. Row must be a number between 1 and 10.")
            continue
        else:
            break
    while True:
        try:
            col = int(input("Choose the column (number between 1 and 10): "))
        except ValueError:
            print("Error. Column must be a number between 1 and 10.")
            continue
        if col < 1 or col > 10:
            print("Error. Row must be a number between 1 and 10.")
            continue
        else:
            break
     
    return evaluate_placement((row, col, lon, board, name, ship))


# 5. Board mechanics

# 5.1. Evaluating if the ship can be placed in the given coordinate
def evaluate_placement(args_tuple):
    """Receives data to evaluate a specific coordinate in a specific board.
    If the ship can be placed (according with the game rules), place the ship.
    If not, call functions to retry again, depending of the board owner.
    This function only place ships in Horizontal orientation.
    
    Params:
        arg_tuple: tuple with data to evaluate a coordinate (tuple)
        
    Returns:
        If the board owner is the User:
            call function 'choose_coord' if the ship can't be placed
            call function 'create_ship_user' if the ship was placed
        If the board owner is the CPU:
            call function 'cpu_placing_ships', every time.
    """

    # Variables
    row = args_tuple[0]
    col = args_tuple[1]
    lon = args_tuple[2]
    board = args_tuple[3]  # CPU or human
    name = args_tuple[4]  # CPU or human
    ship = args_tuple[5]   
    

    # Final column of the ship
    colF = col + lon - 1

    if colF > 10:
        if name != "CPU":
            print("Can't place ship here because it's outside of the limits of the board")
            return choose_coord(ship, board, name)
        else:
            return cpu_placing_ships(name, board)

    elif colF != 10 and col != 1:
        if row != 10 and row != 1:
            if "X" in list(board.loc[row-1, col-1:colF+1]) or \
               "X" in list(board.loc[row+1, col-1:colF+1]) or \
               "X" in list(board.loc[row-1:row+1, col-1]) or \
               "X" in list(board.loc[row-1:row+1, colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)

        elif row == 1:
            if "X" in list(board.loc[row+1, col-1:colF+1]) or \
               "X" in list(board.loc[row:row+1, col-1]) or \
               "X" in list(board.loc[row:row+1, colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        elif row == 10:
            if "X" in list(board.loc[row-1, col-1:colF+1]) or \
               "X" in list(board.loc[row-1:row, col-1]) or \
               "X" in list(board.loc[row-1:row, colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)      
        else:            
            if name != "CPU":
                board.loc[row, col:colF] = "X"
                print("Ship succesfully placed.")
                print(board)
                return create_ship_user(name, board)
            else:
                board.loc[row, col:colF] = "X"
                cpu_ship_dict[lon] -= 1
                return cpu_placing_ships(name, board)
    # Final column == 10
    elif colF == 10:
        if row != 10 and row != 1:
            if "X" in list(board.loc[row-1, col-1:colF]) or \
               "X" in list(board.loc[row+1, col-1:colF]) or \
               "X" in list(board.loc[row-1:row+1, col-1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        elif row == 1:
            if "X" in list(board.loc[row:row+1, col-1]) or \
                "X" in list(board.loc[row+1, col-1:colF]) or \
                "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        elif row == 10:
            if "X" in list(board.loc[row-1:row, col-1]) or \
                "X" in list(board.loc[row-1, col-1:colF]) or \
                "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        else:            
            if name != "CPU":
                board.loc[row, col:colF] = "X"
                print("Ship succesfully placed.")
                print(board)
                return create_ship_user(name, board)
            else:
                board.loc[row, col:colF] = "X"
                cpu_ship_dict[lon] -= 1
                return cpu_placing_ships(name, board)
    # Column == 1
    elif col == 1:
        if row != 10 and row != 1:
            if "X" in list(board.loc[row-1, col:colF+1]) or \
               "X" in list(board.loc[row+1, col:colF+1]) or \
               "X" in list(board.loc[row-1:row+1, colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        elif row == 1:
            if "X" in list(board.loc[row:row+1, colF+1]) or \
               "X" in list(board.loc[row+1, col:colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        elif row == 10:
            if "X" in list(board.loc[row-1, col:colF+1]) or \
               "X" in list(board.loc[row-1:row, colF+1]) or \
               "X" in list(board.loc[row, col:colF]):
                if name != "CPU":
                    print("Can't place ship here, already exists one around.")
                    return choose_coord(ship, board, name)
                else:
                    return cpu_placing_ships(name, board)
            else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)
        else:                
                if name != "CPU":
                    board.loc[row, col:colF] = "X"
                    print("Ship succesfully placed.")
                    print(board)
                    return create_ship_user(name, board)
                else:
                    board.loc[row, col:colF] = "X"
                    cpu_ship_dict[lon] -= 1
                    return cpu_placing_ships(name, board)

# 5.2. Random placing for CPU ships
def cpu_placing_ships(user_name, cpu_self_board):
    """Generates random coordinates to place the CPU ships. 
    Evaluates how many CPU ships remaining to place; when all of them 
    are placed, starts the game.
    
    Params:
        user_name: name of the user (str)
        cpu_self_board: board where CPU place their ships (Pandas DataFrame)
    
    Returns:
        If the CPU have placed all their ships:
            call 'play' function
        If not:
            call 'evaluate_placement' function
    """

    # If the CPU placed all their ships, the game starts
    if sum(cpu_ship_dict.values()) == 0:
        print("The CPU have placed all their ships. Let's start the Battle!")
        global userName, userSelfBoard
        user_shot_board = Board("user_shot_board")
        user_shot_board = user_shot_board.df
        cpu_shot_board = Board("cpu_shot_board")
        cpu_shot_board = cpu_shot_board.df
        return play(userName, userSelfBoard, user_shot_board, cpu_self_board, cpu_shot_board)
    
    # Name of the user (Human or CPU)
    user = user_name

    # Taking the ship length
    long=0
    for key, value in cpu_ship_dict.items():
        if value > 0:
            long=key
            break
        
    # Creating a ship with the length we have
    ship_to_place = Ship(long)
    
    # Row and Column to evaluate
    coord = ship_to_place.coordinate()
    row = coord[0]
    col = coord[1]
    row = int(row)
    col = int(col)
    
    # Calling the function to evaluate the coordinate
    return evaluate_placement((row, col, long, cpu_self_board, user, ship_to_place))

# 6. Playing the game

# 6.1. Start of the Battle
def play(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Call the function 'user_first_turn' to 
    starts the battle between the User and the CPU.
    
    Params:
        user_name: Name of the User (str)
        user_self_board: DataFrame that contains the User's ships (Pandas.DataFrame)
        user_shot_board: empty DataFrame to compare with cpu_self_board (Pandas.Dataframe)
        cpu_self_board: DataFrame that contains the CPU's ships (Pandas.DataFrame)
        cpu_shot_board: empty DataFrame to compare with user_self_board (Pandas.DataFrame)
    
    Returns:
        call 'user_first_turn' function
    """

    # Welcoming the user
    print(f"Welcome to BATTLESHIP, {user_name}. The CPU is ready to play vs you.")
    time.sleep(1)

    return user_first_turn(user_name, user_self_board, user_shot_board, 
                    cpu_self_board, cpu_shot_board)

# 6.2. Function to call CPU turn and avoid errors
def call_cpu_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Just call function 'cpu_turn', to avoid errors and keep all the data: names and boards.
    """
    return cpu_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)

# 6.3. Function that starts the CPU turns and determine if CPU won
def cpu_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Starts the CPU's turn. Generate random coordinates, 
    where the CPU will shoot. Evaluate that coordinates in the User's board. 
    Save the coordinates in tuples, to avoid repetition.
    
    Params:
        user_name: Name of the User (str)
        user_self_board: DataFrame that contains the User's ships (Pandas.DataFrame)
        user_shot_board: empty DataFrame to compare with cpu_self_board (Pandas.Dataframe)
        cpu_self_board: DataFrame that contains the CPU's ships (Pandas.DataFrame)
        cpu_shot_board: empty DataFrame to compare with user_self_board (Pandas.DataFrame)

    Returns:
        If the CPU hits the user:
            call 'call_cpu_turn' function
        If the CPU miss the shot:
            call 'call_user_turn' function
    """

    global cpu_hits

    # Evaluating if CPU won
    if cpu_hits == 20:
        print(f"CPU Won!!! {user_name}, next time you'll perform better. Bye!")
        return None
   
    # The CPU shots
    cpu_coord = (11, 11)
    while cpu_coord in cpu_coordinates_used:
        row_cpu_shot = np.random.randint(low=1, high=11)
        col_cpu_shot = np.random.randint(low=1, high=11)
        # CPU coordinate
        cpu_coord = (row_cpu_shot, col_cpu_shot)
    cpu_coordinates_used.append(cpu_coord)

    # Evaluating hit/water
    cpu_shot = user_self_board.loc[row_cpu_shot, col_cpu_shot]
    if cpu_shot == "X":  # CPU hits
        cpu_hits += 1
        print(f"CPU hits you in coordinate {cpu_coord}!")
        time.sleep(1)
        print("It's CPU turn again.")
        time.sleep(1)
        return call_cpu_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)
    else:
        print(f"The CPU missed the shot in coordinate {cpu_coord}.")
        time.sleep(1)
        print(f"{user_name}, it's your turn again.")
        return call_user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)
    
# 6.4. Function used only once. First turn of the User
def user_first_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Just show an empty board to the User, where his 
    shots will be displayed. Calls 'user_turn' function.
    This function is only used once per game.
    """

    print(f"{user_name}, in this board you will see your shots.")
    print(user_shot_board)
    time.sleep(2)
    print("HOW THE HITS ARE DISPLAYED:\n- Hit: will be marked with X\n- Water: will be marked with O\n")
    time.sleep(2)
    return user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)

# 6.5. Function to call User turn and avoid errors
def call_user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Keep the data safely to call 'user_turn' function
    """
    return user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)   

# 6.6. Starts the User's turns and determine if the User won
def user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board):
    """Define the user's turn. Evaluates if the user hitted the CPU 20 times, 
    in that case the user won. Else, allows the user to select a row and column 
    to make his shot.

    Params: 
        user_name: Name of the User (str)
        user_self_board: DataFrame that contains the User's ships (Pandas.DataFrame)
        user_shot_board: empty DataFrame to compare with cpu_self_board (Pandas.Dataframe)
        cpu_self_board: DataFrame that contains the CPU's ships (Pandas.DataFrame)
        cpu_shot_board: empty DataFrame to compare with user_self_board (Pandas.DataFrame)

    Returns: 
        If the user hits the CPU:
            call 'call_user_turn' function
        If not:
            call 'call_cpu_turn' function
    """

    global user_hits, cpu_hits

    # Evaluating if user won
    if user_hits == 20:
        print("Congratulations, YOU WON!!!")                            
        return None

    # The user must shot
    print(f"{user_name}, Make your shot!")

    # Capturing shot coordinates:
        # 1. Row
    row_shot = None
    while not isinstance(row_shot, int):
        row_shot = input("Choose the row you want to shot: ")
        time.sleep(1)
        try:
            row_shot = int(row_shot)
            if 1 <= row_shot <= 10:
                break
            else:
                print("ERROR. The row has to be a number between 1 and 10!")
                row_shot=None
                time.sleep(1)
        except ValueError:
            print(f"{user_name}, the row must be a number!")
        # 2. Column
    col_shot = None
    while not isinstance(col_shot, int):
        col_shot = input("Choose the column you want to shot: ")
        time.sleep(1)
        try:
            col_shot = int(col_shot)
            if 1 <= col_shot <= 10:
                break
            else:
                print("ERROR. The column has to be a number between 1 and 10!")
                col_shot=None
                time.sleep(1)
        except ValueError:
            print(f"{user_name}, the column must be a number!")
    
    # Here we have the coordinates to shot
    user_target = cpu_self_board.loc[row_shot, col_shot]
    # 1. User miss the shot
    if user_target == ".":  # User miss
        print("You missed the shot. CPU's turn.")
        time.sleep(1)
        user_shot_board.loc[row_shot, col_shot] = 'O'
        print(user_shot_board)
        return call_cpu_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)
    elif user_target == "X":  # User hit
        print("Nice shot! You hitted an enemy ship!")
        user_shot_board.loc[row_shot, col_shot] = "X"
        user_hits += 1
        print(user_shot_board)
        print("It's your turn again...")
        time.sleep(1)
        return call_user_turn(user_name, user_self_board, user_shot_board, cpu_self_board, cpu_shot_board)