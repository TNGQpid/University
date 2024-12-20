# Citation:
# Model: GPT-4o
# Prompt: write a function to determine if a 3x3 puzzle game is solvable (it takes in a list of the positions of the tiles)
# Model: GitHub Copilot (version unknown)
# Prompt: how do I find the manhatten distance of a tile in a 3x3 puzzle game?
# Model: GitHub Copilot (version unknown)
# Prompt: What are all the possible moves you can do on a given tile in a 3x3 puzzle game?

import heapq

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

def find_goal_state(state):
    total_tiles = 0
    goal_state = []
    for i in state:
        if i != 0:
            total_tiles += 1
    for i in range(9):
        if i <= total_tiles - 1:
            goal_state.append(i+1)
        else:
            goal_state.append(0)
    return goal_state

def get_manhatten_distance(state):
    distance = 0
    goal_state = find_goal_state(state)
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

def get_children(state):
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
    return sorted(children)

def print_succ(state):
    children = get_children(state)
    # filler sapce
    for child in children:
        h = get_manhatten_distance(child)
        print(f"{child} h={h}")
    # done

def solve(state):

    if solvability(state):
        print(True)
    else:
        print(False)
        return

    visited = set()
    heap = []
    # heap should look like (g + h, state, g, path)
    heapq.heappush(heap, (0 + get_manhatten_distance(state), state, 0, []))

    iterations = 0 # for a infinite loop detector
    goal = find_goal_state(state)
    while len(heap) > 0:
        # make an extra infinite loop detector
        if iterations > 100000:
            print(False)
            return
        iterations += 1
        # the priority is g + h, where g is the number of moves taken 
        # and h is the heuristic, or the estimated number of moves to go
        priority, current, g, path = heapq.heappop(heap)
        # on the first iteration, since there is nothing in the queue yet, the initial priority doesn't really matter
        # but after that, heapq will always pop the node with the lowest priority, which is like selecting min(g + h) from class
        if current == goal:
            final_state = [current]
            entire_path = path + final_state
            for i in range(len(entire_path)):
                h = get_manhatten_distance(entire_path[i])
                print(f"{entire_path[i]} h={h} moves: {i}")
            
            # print(iterations)
            return # terminate the function
        
        # I wanted to use a list but since lists are mutable I have to use a tuple, which is immutable
        if tuple(current) in visited:
            continue # no need to re-expand this state, that just leads to circles
        else:
            visited.add(tuple(current))
        
        # expand the node
        for child in get_children(current):
            g1 = g + 1 # we made a move to get to this node/child, so increment g by 1
            h1 = get_manhatten_distance(child)
            heapq.heappush(heap, (g1 + h1, child, g1, path + [current]))
    # done

