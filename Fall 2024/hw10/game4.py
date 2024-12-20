import random
import copy

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko. """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its piece color. """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def run_challenge_test(self):
        return False

    def make_move(self, state):
        """ Selects a (row, col) space for the next move using minimax with alpha-beta pruning. """
        drop_phase = sum(row.count(' ') for row in state) > 17  # Detect drop phase (fewer than 8 pieces placed)

        if drop_phase:
            best_move = self.minimax(state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            return [best_move[1]]  # Drop phase only needs the destination
        else:
            best_move = self.minimax(state, depth=3, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
            return [best_move[1], best_move[2]]  # Move includes destination and source

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation. """
        if len(move) > 1:
            source_row, source_col = move[1]
            if source_row is not None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece. """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board. """
        for row in range(len(self.board)):
            print(f"{row}: {' '.join(self.board[row])}")
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition. """
        # Check horizontal and vertical wins
        for i in range(5):
            for j in range(2):
                if state[i][j] != ' ' and len(set(state[i][j:j+4])) == 1:
                    return 1 if state[i][j] == self.my_piece else -1
                if state[j][i] != ' ' and len({state[j+k][i] for k in range(4)}) == 1:
                    return 1 if state[j][i] == self.my_piece else -1

        # Check diagonal wins (\ and /)
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and all(state[i+k][j+k] == state[i][j] for k in range(4)):
                    return 1 if state[i][j] == self.my_piece else -1
                if state[i][j+3] != ' ' and all(state[i+k][j+3-k] == state[i][j+3] for k in range(4)):
                    return 1 if state[i][j+3] == self.my_piece else -1

        # Check box wins
        for i in range(4):
            for j in range(4):
                box = {state[i+x][j+y] for x in range(2) for y in range(2)}
                if len(box) == 1 and ' ' not in box:
                    return 1 if self.my_piece in box else -1

        return 0  # No winner

    def heuristic(self, state):
        """ Evaluates the state and returns a score for the AI player.
        A positive score favors the AI, while a negative score favors the opponent.

        Args:
            state (list of lists): The current state of the board.

        Returns:
            int: Heuristic score of the board state.
        """
        score = 0
        center_positions = [(2, 2), (1, 2), (2, 1), (2, 3), (3, 2)]  # Center and adjacent
        my_piece, opp_piece = self.my_piece, self.opp

        # Center control
        for row, col in center_positions:
            if state[row][col] == my_piece:
                score += 3
            elif state[row][col] == opp_piece:
                score -= 3

        # Horizontal, Vertical, Diagonal, and Box patterns
        directions = [
            [(0, 1), (0, 2), (0, 3)],  # Horizontal
            [(1, 0), (2, 0), (3, 0)],  # Vertical
            [(1, 1), (2, 2), (3, 3)],  # \ Diagonal
            [(1, -1), (2, -2), (3, -3)]  # / Diagonal
        ]

        def score_line(row, col, deltas):
            """ Score a line starting from (row, col) with given deltas. """
            my_count = opp_count = empty_count = 0
            for dr, dc in deltas:
                r, c = row + dr, col + dc
                if 0 <= r < 5 and 0 <= c < 5:
                    if state[r][c] == my_piece:
                        my_count += 1
                    elif state[r][c] == opp_piece:
                        opp_count += 1
                    else:
                        empty_count += 1
                # Scoring based on counts
            if my_count > 0 and opp_count == 0:
                return my_count ** 2  # Favor larger clusters
            elif opp_count > 0 and my_count == 0:
                return -(opp_count ** 2)  # Penalize opponent's clusters
            return 0

        # Evaluate all positions
        for row in range(5):
            for col in range(5):
                if state[row][col] != ' ':
                    for deltas in directions:
                        score += score_line(row, col, deltas)

        # Box patterns (2x2 squares)
        for row in range(4):
            for col in range(4):
                sub_square = [state[row + dr][col + dc] for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]]
                my_count = sub_square.count(my_piece)
                opp_count = sub_square.count(opp_piece)
                if my_count == 3 and sub_square.count(' ') == 1:
                    score += 10  # Strong advantage
                elif opp_count == 3 and sub_square.count(' ') == 1:
                    score -= 10  # Block the opponent

        return score

    def minimax(self, state, depth, alpha, beta, maximizing_player):
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_successors(state, self.my_piece):
                eval = self.minimax(move[0], depth-1, alpha, beta, False)[0]
                if eval > max_eval:
                    max_eval, best_move = eval, move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return (max_eval, best_move[1], best_move[2])
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_successors(state, self.opp):
                eval = self.minimax(move[0], depth-1, alpha, beta, True)[0]
                if eval < min_eval:
                    min_eval, best_move = eval, move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return (min_eval, best_move[1], best_move[2])

    def get_successors(self, state, piece):
        """ Generates successor states for the current player. """
        successors = []
        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ':
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = piece
                    successors.append((new_state, (i, j), None))
        return successors
