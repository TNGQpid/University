import heapq

def state_check(state):
    """check the format of state, and return corresponding goal state.
       Do NOT edit this function."""
    non_zero_numbers = [n for n in state if n != 0]
    num_tiles = len(non_zero_numbers)
    if num_tiles == 0:
        raise ValueError('At least one number is not zero.')
    elif num_tiles > 9:
        raise ValueError('At most nine numbers in the state.')
    matched_seq = list(range(1, num_tiles + 1))
    if len(state) != 9 or not all(isinstance(n, int) for n in state):
        raise ValueError('State must be a list contain 9 integers.')
    elif not all(0 <= n <= 9 for n in state):
        raise ValueError('The number in state must be within [0,9].')
    elif len(set(non_zero_numbers)) != len(non_zero_numbers):
        raise ValueError('State can not have repeated numbers, except 0.')
    elif sorted(non_zero_numbers) != matched_seq:
        raise ValueError('For puzzles with X tiles, the non-zero numbers must be within [1,X], '
                          'and there will be 9-X grids labeled as 0.')
    goal_state = matched_seq
    for _ in range(9 - num_tiles):
        goal_state.append(0)
    return tuple(goal_state)

def get_manhattan_distance(from_state, to_state):
    """
    TODO: implement this function. This function will not be tested directly by the grader. 

    INPUT: 
        Two states (The first one is current state, and the second one is goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    state = from_state
    goal_state = to_state
    for i in range(len(state)):
        tile = state[i]
        if tile != 0:
            # grab the final position from the goal state that we found above
            goal_index = goal_state.index(tile)
            # find the distance between the current position and the goal position
            # for the row, this is done with index floor division 3
            goal_row = goal_index // 3
            curr_row = i // 3
            # for a column, this is done with index mod 3
            goal_col = goal_index % 3
            curr_col = i % 3
            # manhatten distance is the sum of differences in y plus some of differences in x (everything is positive)
            distance += abs(goal_row - curr_row) + abs(goal_col - curr_col)

    return distance

def print_succ(state):
    """
    TODO: This is based on get_succ function below, so should implement that function.

    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """

    # given state, check state format and get goal_state.
    goal_state = state_check(state)
    # please remove debugging prints when you submit your code.
    # print('initial state: ', state)
    # print('goal state: ', goal_state)

    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state,goal_state)))


def get_succ(state):
    """
    TODO: implement this function.

    INPUT: 
        A state (list of length 9)

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    children = []
    # we have to count the number of zeros because this affects our available moves
    zeros = [i for i in range(len(state)) if state[i] == 0]

    for space in zeros:
        row, col = space // 3, space % 3

        moves = [(row - 1, col), # move it up
                 (row + 1, col), # move it down
                 (row, col - 1), # move it left
                 (row, col + 1)] # move it right]
        
        for (new_row, new_col) in moves:
            # check if the operation is in bounds
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # if it is in bounds, find the new position
                new_pos = new_row * 3 + new_col

                if state[new_pos] != 0: # make sure we're not swapping with another zero
                    new_state = state.copy()
                    # swap the values
                    new_state[space], new_state[new_pos] = new_state[new_pos], new_state[space]
                    # done
                    children.append(new_state)
    succ_states = children
    return sorted(succ_states)


def solvability(board):
    # the inversions of the board must be even for it to be solvable
    # an inversion is when a number (i) is greater than another number (j) that comes after it
    if board.count(0) > 1:
        return True
    inversions = 0
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                inversions += 1
    return inversions % 2 == 0

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    TODO: Implement the A* algorithm here.

    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """

    # This is a format helper，which is only designed for format purpose.
    # define "solvable_condition" to check if the puzzle is really solvable
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute "max_length", it might be useful in debugging
    # it can help to avoid any potential format issue.

    # given state, check state format and get goal_state.
    goal_state = list(state_check(state))
    # please remove debugging prints when you submit your code.
    # print('initial state: ', state)
    # print('goal state: ', goal_state)

    #if not solvable_condition:
        #print(False)
        #return
    #else:
        #print(True)

    try:
        state_check(state)
    except ValueError:
        print(False)
        return
    
    if not solvability(state):
        print(False)
        return
    
    print(True)

    visited = set()
    heap = []
    # heap should look like (g + h, state, g, path)
    heapq.heappush(heap, (0 + get_manhattan_distance(state, goal_state), state, 0, []))

    goal = goal_state
    while len(heap) > 0:
        # the priority is g + h, where g is the number of moves taken 
        # and h is the heuristic, or the estimated number of moves to go
        priority, current, g, path = heapq.heappop(heap)
        # on the first iteration, since there is nothing in the queue yet, the initial priority doesn't really matter
        # but after that, heapq will always pop the node with the lowest priority, which is like selecting min(g + h) from class
        if current == goal:
            final_state = [current]
            entire_path = path + final_state
            for i in range(len(entire_path)):
                h = get_manhattan_distance(entire_path[i], goal)
                print(f"{entire_path[i]} h={h} moves: {i}")
            
            # print(iterations)
            return # terminate the function
        
        # I wanted to use a list but since lists are mutable I have to use a tuple, which is immutable
        if tuple(current) in visited:
            continue # no need to re-expand this state, that just leads to circles
        else:
            visited.add(tuple(current))
        
        # expand the node
        for child in get_succ(current):
            g1 = g + 1 # we made a move to get to this node/child, so increment g by 1
            h1 = get_manhattan_distance(child, goal)
            heapq.heappush(heap, (g1 + h1, child, g1, path + [current]))


    #for state_info in state_info_list:
        #current_state = state_info[0]
        #h = state_info[1]
        #move = state_info[2]
        #print(current_state, "h={}".format(h), "moves: {}".format(move))
    #print("Max queue length: {}".format(max_length))

if __name__ == "__main__":
    """
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    """
    # print_succ([2,5,1,4,0,6,7,0,3])
    # print()
    #
    # print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    # print()

    solve([2,5,1,4,0,6,7,0,3])
    print(get_manhattan_distance([4,3,0,5,1,6,7,2,0],list(state_check([4,3,0,5,1,6,7,2,0]))))
    print()
