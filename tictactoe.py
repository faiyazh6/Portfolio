"""
Tic Tac Toe Player
""" 

import math 
import copy

X = "X" 
O = "O"
EMPTY = None 

def initial_state(): 
    """ 
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY], 
            [EMPTY, EMPTY, EMPTY]] 

def player(board): 
    """
    Returns player who has the next turn on a board.
    """
    # setting the accumulators for X and O 
    x_count = 0
    o_count = 0

    # number of rows and columns is same since square board: 
    length = len(board) 
    for row in range(length): 
        for column in range(length): 
            loc_value = board[row][column] 
            # checking for every instance for X: 
            if loc_value == X: 
                x_count += 1 
            # checking for every instance for X: 
            elif loc_value == O: 
                o_count += 1 
    # figuring out who's turn it is: 
    if x_count == o_count: 
        return X 
    else: 
        return O 

def actions(board): 
    """
    Returns set of all possible actions (i, j) available on the board.
    """ 
    empty_locs = [] 
    length = len(board)
    for row in range(length): 
        for column in range(length):  
            # adding every instance of an empty spot on the board to empty_locs for the players to make a move on
            if board[row][column] == EMPTY: 
                empty_locs.append((row, column)) 
    # turning empty_locs into a set 
    return set(empty_locs) 

def result(board, action):
    """ 
    Returns the board that results from making move (i, j) on the board.
    """ 
    # figuring out who's turn it is by calling player(board) and then making a deepcopy of the board
    turn = player(board) 
    board_copy = copy.deepcopy(board) 
    board_copy[action[0]][action[1]] = turn 
    return board_copy 

def winner(board): 
    """
    Returns the winner of the game, if there is one.
    """ 
    length = len(board) 

    # checking column 
    for row in range(length): 
        initial_val = board[row][0] 
        # checking if the initial spot is empty, because if it is empty then no winning combinations can be achieved
        if initial_val != EMPTY: 
            for column in range(1, length): 
                # if any of the spots are not equal to initial_val, then the loop breaks 
                if board[row][column] != initial_val: 
                    break 
                # checks for if we are at the end of the column, meaning every spot along the column had the same character
                if column == length - 1: 
                    return initial_val 
    
    # checking row 
    for column in range(length): 
        initial_val = board[0][column] 
        # checking if the initial spot is empty, because if it is empty then no winning combinations can be achieved
        if initial_val != EMPTY: 
            for row in range(1, length): 
                # if any of the spots are not equal to initial_val, then the loop breaks 
                if board[row][column] != initial_val: 
                    break 
                # checks for if we are at the end of the row, meaning every spot along the row had the same character
                if row == length - 1: 
                    return initial_val 
    
    # checking left diagonal (\): 
    initial_val = board[0][0]  
    # checking if the initial spot is empty, because if it is empty then no winning combinations can be achieved
    if initial_val != EMPTY: 
        for position in range(1, length): 
            # if any of the spots are not equal to initial_val, then the loop breaks
            if board[position][position] != initial_val: 
                break 
            # checks for if we are at the end of the diagonal, meaning every spot along the diagonal had the same character
            if position == length - 1: 
                return initial_val 
        
    #checking right diagonal (/): 
    initial_val = board[0][length - 1] 
    # checking if the initial spot is empty, because if it is empty then no winning combinations can be achieved
    if initial_val != EMPTY: 
        for position in range(1, length): 
            # if any of the spots are not equal to initial_val, then the loop breaks
            if board[position][length - 1 - position] != initial_val: 
                break 
            # checks for if we are at the end of the diagonal, meaning every spot along the diagonal had the same character
            if position == length - 1: 
                return initial_val 
    
    # if no one wins: 
    return None 

def terminal(board): 
    """
    Returns True if game is over, False otherwise.
    """
    # indicating someone won: 
    if winner(board) != None: 
        return True
    else: 
        # if there is an empty spot, it means the game still did not end: 
        for row in range(len(board)): 
            for column in range(len(board[row])): 
                if board[row][column] == EMPTY: 
                    return False 
        # otherwise, true is returned (as in the game ended because of a tie) 
        return True 

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """ 
    grid_val = winner(board) 
    # if the winner is X: 
    if grid_val == X: 
        return 1
    # if the winner is O: 
    elif grid_val == O: 
        return -1 
    # if it is a tie: 
    else: 
        return 0 

# helper function for optimal move for X - code taken from lecture 0 (Search) slides: 
def max_value(board): 
    # checking if the board is terminal: 
    if terminal(board): 
        return utility(board) 
    v = -math.inf 
    for action in actions(board): 
        # maximizing the score 
       v = max(v, min_value(result(board, action))) 
    return v 

# helper function for optimal move for O - code taken from lecture 0 (Search) slides 
def min_value(board): 
    # checking if the board is terminal 
    if terminal(board): 
        return utility(board) 
    v = math.inf  
    for action in actions(board): 
        # mainimizing the score 
        v = min(v, max_value(result(board, action))) 
    return v 

# https://levelup.gitconnected.com/mastering-tic-tac-toe-with-minimax-algorithm-3394d65fa88f 
# https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/ 
def minimax(board): 
    """
    Returns the optimal action for the current player on the board.
    """ 
    # checking if the board is terminal 
    if terminal(board): 
        return None 
    # initially setting best_score and best_move to None: 
    best_score = None 
    best_move = None 
    # figuring out who's turn it is: 
    turn = player(board) 
    for action in actions(board):
        # deciding the optimal move for X: 
        if turn == X: 
            score = min_value(result(board, action)) 
            if best_score == None or score > best_score:
                best_score = score 
                best_move = action 
        # deciding the optimal move for O: 
        else:
            score = max_value(result(board, action)) 
            if best_score == None or score < best_score:
                best_score = score 
                best_move = action 
    # returning the optimal move for whoever's turn it is: 
    return best_move 