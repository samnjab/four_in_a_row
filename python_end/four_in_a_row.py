from __future__ import annotations

import sys
from io import StringIO
from random import shuffle
from class_def import Grid

######################
# The FourInARow class
######################
WIN = 2
DRAW = 1
LOSS = 0
IN_PROGRESS = -1

# An example of a script for a played game
GAME_SCRIPT_X_WINS = '5 True True\n' \
                     '1\n' \
                     '0\n' \
                     '1\n' \
                     '0\n' \
                     '1\n' \
                     '0\n' \
                     '1\n'
GAME_SCRIPT_X_ROW_WIN = '5 True True\n' \
                        '0\n' \
                        '0\n' \
                        '1\n' \
                        '1\n' \
                        '2\n' \
                        '2\n' \
                        '3\n'
GAME_SCRIPT_UP_DIAG_WIN = '5 True True\n' \
                          '2\n' \
                          '1\n' \
                          '2\n' \
                          '2\n' \
                          '3\n' \
                          '1\n' \
                          '1\n' \
                          '0\n' \
                          '0\n' \
                          '3\n' \
                          '3\n' \
                          '3\n'
GAME_SCRIPT_DOWN_DIAG_WIN = '5 True True\n' \
                            '0\n' \
                            '0\n' \
                            '0\n' \
                            '0\n' \
                            '0\n' \
                            '1\n' \
                            '1\n' \
                            '1\n' \
                            '1\n' \
                            '1\n' \
                            '2\n' \
                            '2\n' \
                            '2\n' \
                            '2\n' \
                            '3\n' \
                            '2\n' \
                            '3\n' \
                            '3\n' \
                            '3\n' \
                            '3\n' \
                            '4\n' \
                            '4\n' \
                            '4\n' \
                            '4\n' \
                            '4\n'
GAME_SCRIPT_DRAW = '5 True True\n' \
                    '0\n' \
                    '0\n' \
                    '0\n' \
                    '0\n' \
                    '0\n' \
                    '1\n' \
                    '1\n' \
                    '1\n' \
                    '1\n' \
                    '1\n' \
                    '2\n' \
                    '2\n' \
                    '2\n' \
                    '2\n' \
                    '3\n' \
                    '2\n' \
                    '4\n' \
                    '3\n' \
                    '3\n' \
                    '3\n' \
                    '3\n' \
                    '4\n' \
                    '4\n' \
                    '4\n' \
                    '4\n'


class FourInARow:
    """
    A class representing a game of Four-in-a-Row.

    Attributes:
    - board: the instance of Grid the game is being played on.
    - result: the current status of the game being played.
    - p1_human: bool representing whether the first player is human.
    - p2_human: bool representing whether the second player is human.
    - p1_to_play: bool representing whether the first player is allowed to play.

    Representation Invariants:
    - self.result in (WIN, DRAW, LOSS, IN_PROGRESS)
    """

    board: Grid
    result: int
    p1_human: bool
    p2_human: bool
    p1_to_play: bool

    def __init__(self, n: int, p1_human: bool, p2_human: bool) -> None:
        """
        Initialize this game of four-in-a-row to be played on an n-by-n grid.

        The game begins with a result of IN_PROGRESS and p1 to play.

        <p1_human> and <p2_human> indicate whether each of p1 and p2 are human
        or computer players.

        Preconditions:
        - n > 3
        """
        self.result = IN_PROGRESS
        self.p1_human = p1_human
        self.p2_human = p2_human
        self.board = Grid(n)
        self.p1_to_play = True

    def play(self) -> None:
        """
        Play this game and update the result attribute to indicate the outcome.

        Preconditions:
        - self.result == IN_PROGRESS

        Since this function has a lot of text output, we use a feature
        of doctest which allows us to conveniently ignore part of the output.
        The doctest:+ELLIPSIS comment tells doctest to ignore the ... and
        any output after it when checking for matching output.

        >>> my_input = StringIO(GAME_SCRIPT_X_WINS)
        >>> sys.stdin = my_input
        >>> g = load_game()  # doctest:+ELLIPSIS
        Enter game...
        >>> g.play()  # doctest:+ELLIPSIS
        Initial Board...
        >>> g.result == WIN
        True
        """
        i = 1
        print('Initial Board')
        print(self.board)
        last_player = self.p1_to_play
        while not self._take_turn():
            print(f"Turn {i}")
            print(self.board)
            i += 1
            last_player = self.p1_to_play

        if self.p1_to_play != last_player:  # board became full!
            self.result = DRAW
        elif self.p1_to_play:  # first player won!
            self.result = WIN
        else:  # first player lost!
            self.result = LOSS
        print(f"Turn {i}")
        print(self.board)

    def _take_turn(self) -> bool:
        """
        Return True if this play has caused the game to end or False otherwise.

        This could happen either by the board becoming full or the current
        player winning the game.

        If the game has not ended, then whose turn it is will be updated.

        Preconditions:
        - self.result == IN_PROGRESS

        Note: # doctest:+ELLIPSIS is a feature of doctest used below, which
              tells doctest to treat ... as a wildcard match. For example,
              below where it says "X computer..." this means that the doctest
              will pass if the result of g._take_turn() prints "X computer"
              followed by anything. Since both players are computers, we
              can't know what the exact output will be, so using a wildcard
              match is convenient here.

        >>> g = FourInARow(4, False, False)  # a game between computer players
        >>> g._take_turn()  # doctest:+ELLIPSIS
        X computer...
        >>> g.p1_to_play
        False
        >>> g._take_turn()  # doctest:+ELLIPSIS
        O computer...
        >>> g.p1_to_play
        True
        """
        # determine whose turn it is
        if self.p1_to_play:
            symbol = 'X'
            is_human = self.p1_human
        else:
            symbol = 'O'
            is_human = self.p2_human

        # get the coordinate that the player chooses to play their piece at
        column_move = None
        row_move = None
        if is_human:  # get input from the user
            while row_move is None:
                column_move = int(input(f"{symbol} to move: "))
                print(column_move)
                row_move = self.board.drop(column_move, symbol)
        else:
            # random computer move
            print(f"{symbol} computer moving...", end="")
            column_moves = list(range(self.board.n))
            shuffle(column_moves)
            while row_move is None:
                column_move = column_moves.pop()
                row_move = self.board.drop(column_move, symbol)
            print(column_move)
        # given where the move was made, check if this player won
        if self.board.has_fiar((row_move, column_move)):
            return True

        self.p1_to_play = not self.p1_to_play  # update whose turn it is
        # return whether the grid is full
        return self.board.is_full()


###################################################
# The provided client code for the FourInARow class
###################################################
def load_game() -> FourInARow:  # pragma: no cover
    """
    Return a four-in-a-row game.

    Input from the user is read from standard input which specifies:
    n is_p1_human? is_p2_human?

    >>> my_input = StringIO('4 True False\\n')
    >>> sys.stdin = my_input
    >>> g = load_game()  # note: this will print the prompt for input, as below.
    Enter game parameters (<n> <is_p1_human?> <is_p2_human?>):
    >>> g.board.n
    4
    >>> g.p1_human
    True
    >>> g.p2_human
    False
    >>> g.p1_to_play
    True
    >>> g.result == IN_PROGRESS
    True
    """
    input_string = input("Enter game parameters (<n> <is_p1_human?> "
                         "<is_p2_human?>):\n")
    # pull out the three pieces of information
    n, p1_human, p2_human = input_string.split()
    # return the actual game based on this information
    return FourInARow(int(n), p1_human == 'True', p2_human == 'True')


def play_game(script: str | None = None) -> FourInARow:  # pragma: no cover
    """
    Play a game of four-in-a-row, returning the FourInARow object created.

    If <script> is provided, it is used to read input from.
    Otherwise, the user will be prompted for the moves of the first player in
    a game against a computer on a 6-by-6 board.

    See test_a0.py for a sample test. Since this function has a lot of text
    output, no doctest examples are provided.
    """
    if script is not None:
        sys.stdin = StringIO(script)
        fiar = load_game()
    else:
        fiar = FourInARow(6, True, False)  # play human versus computer

    fiar.play()

    if fiar.result == DRAW:
        print("Game ended in a draw!")
    elif fiar.result == WIN:
        print("Game won by X player!")
    else:  # fiar.result == LOSS
        print("Game won by O player!")

    return fiar


##########################################
# Main: where you can run the full program
##########################################
if __name__ == '__main__':
    use_script = True
    if use_script:
        play_game(GAME_SCRIPT_X_WINS)
    else:
        play_game()
