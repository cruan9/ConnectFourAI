from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
from typing import List
from connect_four import State, Game, Player
from copy import deepcopy
from random import randint

class MinimaxNode:
    """
    One node in the Minimax search tree.

    """
    def __init__(self, state: State):
        """
        Stores the node's state, (heuristic) value, and a dictionary of successor nodes,
        where the keys are possible moves and the values are the successor nodes resulting from those moves

        :param  state: The state associated with this node
        :type state: State
        """
        self.state = state
        self.value = 0
        self.successors = {}

    def __eq__(self, other):
        """
        Recursively compares two MinimaxNodes, producing true if all have the same heuristic value,
        state, and successors. Used by the == operator.

        :param  other: The other MinimaxNode
        :type other: MinimaxNode
        :return: True if the nodes are equal, False otherwise
        :rtype: bool
        """
        return self.state == other.state and self.value == other.value and self.successors == other.successors



def minimax(node: MinimaxNode, depth: int, max_role: str, heuristic_fn):
    """
    Performs minimax search from the given node out to a maximum depth, when heuristic evaluation is performed.
    Generates a tree of MinimaxNodes rooted at node, with correct state, value, and successors attributes

    :param node: The node that will be the root of this search
    :type node: MinimaxNode
    :param depth: The search depth. When depth is 0, perform a heuristic evaluation.
    :type depth: int
    :param max_role: The maximizing player
    :type max_role: str (one of 'x' or 'o')
    :param heuristic_fn: The heuristic evaluation function to be used at the max search depth
    :type heuristic_fn: Function (State str -> float), which consumes the state to be evaluated and
    :                   the maximizing player's role (either 'x' or 'o')
    :return: The evaluation of the given node
    :rtype: int
    """
    if depth == 0 or node.state.is_terminal:
        value = heuristic_fn(node.state, max_role)
        node.value = value
        return value
    if max_role == node.state.turn:
        value = -100000
        moves = node.state.get_legal_moves()
        for i in moves:
            child = MinimaxNode(deepcopy(node.state))
            child.state.advance_state(i)
            childValue = minimax(child, depth - 1, max_role, heuristic_fn)
            value = max(value, childValue)
            child.value = childValue
            node.successors[i] = child
        node.value = value
        return value
    else:
        value = 100000
        moves = node.state.get_legal_moves()
        for i in moves:
            child = MinimaxNode(deepcopy(node.state))
            child.state.advance_state(i)
            childValue = minimax(child, depth - 1, max_role, heuristic_fn)
            value = min(value, childValue)
            child.value = childValue
            node.successors[i] = child
        node.value = value
        return value

def three_line_heur(state: State, max_role: str):
    """
    Performs a heuristic evaluation of the given state, equal to the number of three-in-a-rows for the
    maximizing player minus the number of three-in-a-rows for the minimizing player.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: int
    """
    col_dirs = [1, 1, 0, -1]
    row_dirs = [0, 1, 1, 1]
    result = 0

    #If the state is terminal, give the true evaluation
    if state.is_terminal:
        if state.winner == '':
            return 0
        elif state.winner == max_role:
            return 100
        else:
            return -100

    #If the state is not terminal, give the heuristic evaluation
    i = 0
    while i < state.num_cols:
        j = 0
        while j < state.num_rows:
            if state.board[i][j] != '.':
                piece = state.board[i][j]
                dir = 0
                while dir < len(col_dirs):
                    farthest_pnt = [i + 2 * col_dirs[dir], j + 2 * row_dirs[dir]]
                    if state.coords_legal(farthest_pnt[0], farthest_pnt[1]):
                        if piece == state.board[i + col_dirs[dir]][j + row_dirs[dir]] and \
                                piece == state.board[farthest_pnt[0]][farthest_pnt[1]]:
                            if piece == max_role:
                                result += 1
                            else:
                                result -= 1
                    dir += 1
            j += 1
        i += 1
    return result


def zero_heur(state: State, max_role: str):
    """
    Produces 0 for any non-terminal state.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: int
    """

    #If the state is terminal, give the true evaluation
    if state.is_terminal:
        if state.winner == '':
            return 0
        elif state.winner == max_role:
            return 100
        else:
            return -100

    #If the state is not terminal, produce 0
    return 0



def my_heuristic(state: State, max_role: str):
    """
    Performs a heuristic evaluation of the given state.
    If the state is terminal, gives the true evaluation instead (100 if the maximizer has won,
    0 for a draw, or -100 if the minimizer has won)

    :param state: The state to evaluate
    :type state: State
    :param max_role: The role of the maximizing player
    :type max_role: str (one of 'x' or 'o')
    :return: The evaluation of the given state
    :rtype: int
    """
    # Your code here!
    col_dirs = [1, 1, 0, 1]
    row_dirs = [0, 1, 1, -1]
    result = 0

    #If the state is terminal, give the true evaluation
    if state.is_terminal:
        if state.winner == '':
            return 0
        elif state.winner == max_role:
            return 100
        else:
            return -100

    #If the state is not terminal, give the heuristic evaluation
    i = 0
    while i < state.num_cols:
        j = 0
        while j < state.num_rows:
            dir = 0
            while dir < len(col_dirs):
                farthest_pnt = [i + 3 * col_dirs[dir], j + 3 * row_dirs[dir]]
                if state.coords_legal(farthest_pnt[0], farthest_pnt[1]):
                    curResult = 0
                    piece = ''
                    samePiece = 0
                    emptySquare = 0
                    maxConsecutive = 0
                    curConsecutive = 0
                    prevPiece = state.board[i][j]
                    if prevPiece != '.':
                        maxConsecutive = 1
                        curConsecutive = 1
                        samePiece += 1
                        piece = prevPiece
                    for k in range(1,4):
                        nextPiece = state.board[i + k *col_dirs[dir]][j + k * row_dirs[dir]]
                        if piece == '.' and nextPiece != '.':
                            piece = nextPiece
                        if(nextPiece == piece):
                            samePiece += 1
                        elif(nextPiece == '.'):
                            emptySquare += 1
                        else:
                            continue
                        if nextPiece == prevPiece:
                            curConsecutive += 1
                            maxConsecutive = max(curConsecutive, maxConsecutive)
                        elif nextPiece != prevPiece:
                            curConsecutive = 1
                        prevPiece = nextPiece
                    if samePiece == 3 and emptySquare == 1 and maxConsecutive == 3 and piece == max_role:
                        curResult += 1
                    elif samePiece == 3 and emptySquare == 1 and maxConsecutive == 3 and piece != max_role:
                        curResult -= 1
                    elif samePiece == 3 and emptySquare == 1 and maxConsecutive != 3 and piece == max_role:
                        curResult += 0.75
                    elif samePiece == 3 and emptySquare == 1 and maxConsecutive != 3 and piece != max_role:
                        curResult -= 0.75
                    elif samePiece == 2 and emptySquare == 2 and maxConsecutive == 2 and piece == max_role:
                        curResult += 0.15
                    elif samePiece == 2 and emptySquare == 2 and maxConsecutive == 2 and piece != max_role:
                        curResult -= 0.15
                    elif samePiece == 2 and emptySquare == 2 and maxConsecutive == 1 and piece == max_role:
                        curResult += 0.1
                    elif samePiece == 2 and emptySquare == 2 and maxConsecutive == 1 and piece != max_role:
                        curResult -= 0.1
                    if i == 0 or i == 6:
                        curResult *= 0.9
                    elif i == 1 or i == 5:
                        curResult *= 0.95
                    elif i == 3 or i == 4:
                        curResult *= 1.1
                    if j == 0 or j == 6:
                        curResult *= 0.9
                    elif j == 1 or j == 5:
                        curResult *= 0.95
                    elif j == 3 or j == 4:
                        curResult *= 1.1
                    result += curResult
                dir += 1
            j += 1
        i += 1
    return result


class MinimaxPlayer(Player):
    """
    An agent that uses minimax to select moves.

    """

    def __init__(self, depth: int, heur, display=True):
        """
        Stores minimax parameters

        :param depth: The depth at which search is terminated and a heuristic evaluation is performed
        :type depth: int
        :param heur: The heuristic evaluation function to be used at the max search depth
        :type heur: Function (State str -> float), which consumes the state to be evaluated and
        :           the maximizing player's role (either 'x' or 'o')
        :param display: If true, print board every play
        :type display: bool
        """
        self.role = ''
        self.depth = depth
        self.heur = heur
        self.display = display

    def initialize(self, role: str):
        """
        This function is called once for each agent at the beginning of a game, before any moves are made

        :param role: The role of the player
        :type role: str (one of 'x' or 'o')
        """
        self.role = role

    def play(self, state: State):
        """
        This function is called every time it is the player's turn. It produces the column number that a
        piece should be dropped into

        :param state: the game's current State
        :type state: State
        :return: A column number representing a valid move to be played
        :rtype: int
        """
        if self.display:
            state.display()
        root = MinimaxNode(state)
        minimax(root, self.depth, self.role, self.heur)
        best_moves = []
        for move in root.successors.keys():
            if len(best_moves) == 0 or root.successors[move].value > root.successors[best_moves[0]].value:
                best_moves = [move]
            elif root.successors[move].value == root.successors[best_moves[0]].value:
                best_moves.append(move)
        return best_moves[randint(0, len(best_moves)-1)]



class FirstMovePlayer(Player):
    """
    An agent that always plays the first legal move.

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        return state.get_legal_moves()[0]



class RandomPlayer(Player):
    """
    An agent that always plays a random move.

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        moves = state.get_legal_moves()
        return moves[randint(0,len(moves)-1)]


class HumanPlayer(Player):
    """
    An agent that allows you to play by keyboard input!

    """

    def initialize(self, role: str):
        pass

    def play(self, state: State):
        state.display()
        moves = state.get_legal_moves()
        valid = False
        col = -1
        while not valid:
            str = input("Enter a column number in the range [0,6]: ")
            try:
                col = int(str)
                if col in moves:
                    valid = True
                else:
                    print("Selected column is not valid.")
            except ValueError:
                print("Unable to parse input.")
        return col



if __name__ == "__main__":
    game = Game(MinimaxPlayer(4, my_heuristic), MinimaxPlayer(3, three_line_heur))
    winner = game.play_game()
    game.display()
