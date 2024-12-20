import random
import copy
import time
import math
# Model: Chat-GPT 4-o, Prompt: Build a heuristic that scans for groups of 2 for both you and the opponent in Teeko
# Model: Chat-GPT 4-o, Prompt: Add alpha beta pruning to my current minimax algorithm

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        # Set to True if you would like to run gradescope against the challenge AI!
        # Leave as False if you would like to run the gradescope tests faster for debugging.
        # You can still get full credit with this set to False
        return False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """

        def is_drop_phase(state):
            return sum([row.count(' ') for row in state]) >= 5*5 - 7

        def get_succ(state):
            succs = []
            length, width = range(5), range(5)
            if is_drop_phase(state):
                for i in length:
                    for j in width:
                        if state[i][j] == ' ':
                            new_state = copy.deepcopy(state)
                            new_state[i][j] = self.my_piece
                            succs.append(new_state)
                return succs
            
            else:
                for i in length:
                    for j in width:
                        if state[i][j] == self.my_piece:
                            # move up-left
                            if 0 <= i-1 < 5 and 0 <= j-1 < 5 and state[i-1][j-1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i-1][j-1] = self.my_piece
                                succs.append(new_state)
                            # move up
                            if 0 <= i-1 < 5 and state[i-1][j] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i-1][j] = self.my_piece
                                succs.append(new_state)
                            # move up-right
                            if 0 <= i-1 < 5 and 0 <= j+1 < 5 and state[i-1][j+1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i-1][j+1] = self.my_piece
                                succs.append(new_state)
                            # move left
                            if 0 <= j-1 < 5 and state[i][j-1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i][j-1] = self.my_piece
                                succs.append(new_state)
                            # move right
                            if 0 <= j+1 < 5 and state[i][j+1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i][j+1] = self.my_piece
                                succs.append(new_state)
                            # move down-left
                            if 0 <= i+1 < 5 and 0 <= j-1 < 5 and state[i+1][j-1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i+1][j-1] = self.my_piece
                                succs.append(new_state)
                            # move down
                            if 0 <= i+1 < 5 and state[i+1][j] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i+1][j] = self.my_piece
                                succs.append(new_state)
                            # move down-right
                            if 0 <= i+1 < 5 and 0 <= j+1 < 5 and state[i+1][j+1] == ' ':
                                new_state = copy.deepcopy(state)
                                new_state[i][j] = ' '
                                new_state[i+1][j+1] = self.my_piece
                                succs.append(new_state)
                return succs
                            

        #if not drop_phase:
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!
            #pass

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        statee = copy.deepcopy(state)

        def minimax(statee, max_depth=3):
            start_time = time.time()

            def heuristic(statee):
                """
                Heuristic is based on:
                - Number of 2-in-a-row sequences for me/my pieces
                - Blocking 2-in-a-row sequences of the opponent
                """
                score = 0
                for row in statee:
                    for i in range(2):
                        # Favor my pieces
                        if row[i:i+3].count(self.my_piece) == 2 and row[i:i+3].count(' ') == 1:
                            score += 10
                        # Block opponent's sequences
                        if row[i:i+3].count(self.opp) == 2 and row[i:i+3].count(' ') == 1:
                            score -= 10

                # Vertical evaluation
                for col in range(5):
                    for i in range(2):
                        column_segment = [statee[row][col] for row in range(i, i+3)]
                        if column_segment.count(self.my_piece) == 2 and column_segment.count(' ') == 1:
                            score += 10
                        if column_segment.count(self.opp) == 2 and column_segment.count(' ') == 1:
                            score -= 10

                if -1 <= score/160 <= 1:
                    return score/160
                else:
                    return math.tanh(score)

            def max_value(state, depth, alpha, beta):
                if self.game_value(state) != 0:
                    return self.game_value(state)
                elif depth == 0:
                    if self.game_value(state) == 0:
                        return heuristic(state)
                    return self.game_value(state)
                #if self.game_value(state) != 0 or depth == 0:
                    #return self.game_value(state) or heuristic(state)
                value = -float('inf')
                for s in get_succ(state):
                    value = max(value, min_value(s, depth - 1, alpha, beta))
                    if value >= beta:
                        return value
                    alpha = max(alpha, value)
                return value

            def min_value(state, depth, alpha, beta):
                if self.game_value(state) != 0:
                    return self.game_value(state)
                elif depth == 0:
                    if self.game_value(state) == 0:
                        return heuristic(state)
                    return self.game_value(state)
                #if self.game_value(state) != 0 or depth == 0:
                    #return self.game_value(state) or heuristic(state)
                value = float('inf')
                for s in get_succ(state):
                    value = min(value, max_value(s, depth - 1, alpha, beta))
                    if value <= alpha:
                        return value
                    beta = min(beta, value)
                return value


            best_move = None
            best_value = -float('inf')
            alpha = -float('inf')
            beta = float('inf')

            for s in get_succ(statee):
                if time.time() - start_time > 5:  # Check time limit
                    break
                v = min_value(s, max_depth - 1, alpha, beta)
                if v > best_value:
                    best_value = v
                    best_move = s

            return best_move


        
        def find_move_tuple(state, next_best_state):

            start_pos = None
            end_pos = None
            length, width = range(5), range(5)

            for i in length:
                for j in width:
                    if state[i][j] != next_best_state[i][j]:
                        if state[i][j] == ' ':  # Piece was added here
                            end_pos = (i, j)
                        elif next_best_state[i][j] == ' ':  # Piece was removed from here
                            start_pos = (i, j)

            return (start_pos, end_pos)
            
        best_state = minimax(statee)
        move = find_move_tuple(state, best_state)
        if is_drop_phase(state):
            return [move[1]]
        else:
            return list(move)


    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):  # Rows to start diagonal checks (0 or 1)
            for j in range(2):  # Columns to start diagonal checks (0 or 1)
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1
        # TODO: check / diagonal wins
        for i in range(2):  # Rows to start diagonal checks (0 or 1)
            for j in range(2):  # Columns to start diagonal checks (0 or 1)
                if state[i][j+3] != ' ' and state[i][j+3] == state[i+1][j+2] == state[i+2][j+1] == state[i+3][j]:
                    return 1 if state[i][j+3] == self.my_piece else -1
        # TODO: check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i][j+1] == state[i+1][j+1]:
                    return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
