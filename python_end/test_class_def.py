from __future__ import annotations
from four_in_a_row import *
from class_def import *


class TestHelpers:
    """
    These are provided tests related to Task 1, which are meant to remind you
    of the structure of a pytest for later tasks. For Task 1, you are asked
    to write doctests instead.

    While not required, you are welcome to add other pytests here as you
    develop your code.
    """

    def test_within_grid_in_grid(self):
        """Test that (0, 0) is inside a 4-by-4 grid."""
        assert within_grid((0, 0), 4)

    def test_within_grid_outside_grid(self):
        """Test that (4, 4) is outside a 4-by-4 grid."""
        assert not within_grid((4, 4), 4)

    def test_all_within_grid_all_in_grid(self):
        """Test when the four coordinates are all within a 4-by-4 grid."""
        assert all_within_grid([(0, 0), (1, 1), (2, 2), (3, 3)], 4)

    def test_reflect_vertically_above(self):
        """Test reflecting vertically for a coordinate above the middle."""
        assert reflect_vertically((0, 1), 5) == (4, 1)

    def test_reflect_vertically_middle(self):
        """Test reflecting vertically for a coordinate on the middle row."""
        assert reflect_vertically((2, 1), 5) == (2, 1)

    def test_reflect_points(self):
        """Test reflecting a very short line"""
        assert reflect_points([(0, 1), (1, 2)], 5) == [(4, 1), (3, 2)]


class TestLine:
    def test_row_is_row(self):
        """Test a valid row is a row"""
        assert is_row([Square((2, 2)), Square((2, 3)), Square((2, 4)), Square((2, 5))])

    def test_disordered_row_is_not_row(self):
        """Test a non-ordered set of coordinates in a row is not a row"""
        assert not is_row([Square((3, 4)), Square((3, 3)), Square((3, 5)),
                           Square((3, 6))])

    def test_diff_row_is_not_row(self):
        """Test a  set of points with different row coords is not a row"""
        assert not is_row([Square((2, 1)), Square((2, 2)), Square((2, 3)),
                           Square((3, 4))])

    def test_column_is_column(self):
        """Test a valid column is a column"""
        assert is_column([Square((2, 2)), Square((3, 2)), Square((4, 2)),
                          Square((5, 2))])

    def test_disordered_column_is_not_column(self):
        """Test a non-ordered set of coordinates in column is not a column"""
        assert not is_column([Square((1, 4)), Square((2, 4)), Square((4, 4)),
                              Square((3, 4))])

    def test_diff_column_is_not_column(self):
        """Test a set of points with different column coords is not a column"""
        assert not is_column([Square((0, 2)), Square((1, 2)), Square((3, 2)),
                              Square((4, 3))])

    def test_up_diagonal_is_diagonal(self):
        """Test a valid up diagonal line is diagonal"""
        assert is_diagonal([Square((5, 0)), Square((4, 1)), Square((3, 2)),
                            Square((2, 3))])

    def test_down_diagonal_is_diagonal(self):
        """Test a valid down diagonal line is diagonal"""
        assert is_diagonal([Square((1, 0)), Square((2, 1)), Square((3, 2)),
                            Square((4, 3))])

    def test_same_row_is_not_diagonal(self):
        """Test a set of points with at least one shared row coord is not a
        diagonal"""
        assert not is_diagonal([Square((1, 1)), Square((2, 2)), Square((3, 3)),
                                Square((3, 4))])

    def test_disordered_diagonal_is_not_diagonal(self):
        """Test a disordered set of points in a diagonal is not a diagonal"""
        assert not is_diagonal([Square((4, 1)), Square((3, 2)), Square((1, 4)),
                                Square((2, 3))])

    def test_line_drop_empty_column(self):
        """Test a drop in an empty column"""
        l = Line([Square((0, 0)), Square((1, 0)),
                  Square((2, 0)), Square((3, 0))])
        assert l.drop('X') == 3

    def test_line_drop_non_empty_column(self):
        """Test a drop in a non-empty column"""
        l = Line([Square((0, 0)), Square((1, 0), 'X'),
                  Square((2, 0), 'X'), Square((3, 0), 'X')])
        assert l.drop('O') == 0

    def test_line_drop_symbol_mutated(self):
        """Test a drop in the column successfully mutates symbol of square"""
        l = Line([Square((0, 0)), Square((1, 0), 'X'),
                  Square((2, 0), 'X'), Square((3, 0), 'X')])
        row = l.drop('O')
        assert l[row].symbol == 'O'

    def test_full_line_is_full(self):
        """Test a full line is full"""
        l = Line([Square((0, 0), 'O'), Square((1, 0), 'X'),
                  Square((2, 0), 'X'), Square((3, 0), 'O')])
        assert l.is_full()

    def test_non_full_line_is_full(self):
        """Test a non-full column is not full"""
        l = Line([Square((0, 0)), Square((1, 0), 'X'),
                  Square((2, 0), 'X'), Square((3, 0), 'O')])
        assert not l.is_full()

    def test_empty_line_not_fiar(self):
        """Test an empty column does not contain four in a row passing through
        one of its points"""
        l = Line([Square((0, 1)), Square((0, 2)),
                  Square((0, 3)), Square((0, 4))])
        assert not l.has_fiar((0, 2))

    def test_full_diagonal_has_fiar(self):
        """Test a valid full diagonal has four in a row passing through one of
        its points"""
        l = Line([Square((0, 1), 'X'), Square((1, 2), 'X'),
                  Square((3, 3), 'X'), Square((4, 4), 'X')])
        assert l.has_fiar((3, 3))

    def test_mixed_symbol_not_fiar(self):
        """Test a full line with mixed symbols does not have four in a row
        passing through one of its points"""
        l = Line([Square((4, 0), 'X'), Square((3, 1), 'O'),
                  Square((2, 2), 'X'), Square((1, 3), 'X')])
        assert not l.has_fiar((3, 1))

    def test_long_line_fiar(self):
        """Test a line with len(line) >= 4 with four in a row X's and trailing
        None's at the end has fiar"""
        l = Line([Square((4, 0), 'X'), Square((4, 1), 'X'),
                  Square((4, 2), 'X'), Square((4, 3), 'X'),
                  Square((4, 4))])
        assert l.has_fiar((4, 3))

    def test_gap_fiar(self):
        """Test a line with four X's with a gap in the middle is not fiar"""
        l = Line([Square((4, 0), 'X'), Square((4, 1), 'X'),
                  Square((4, 2), 'X'), Square((4, 3), 'O'),
                  Square((4, 4), 'X')])
        assert not l.has_fiar((4, 4))


class TestGrid:
    def test_grid_drop_empty_col(self):
        """Test return value of a drop into an empty column of the grid"""
        grid = Grid(4)
        row = grid.drop(0, 'X')
        assert row == 3

    def test_grid_drop_full_col(self):
        """Test Grid.drop into a full column returns None"""

        grid = Grid(4)
        for _ in range(4):
            grid.drop(2, 'X')
        assert grid.drop(2, 'O') is None

    def test_grid_drop_symbol_mutation(self):
        """Test Grid.drop successfully mutates the symbol of the square it
        dropped into"""
        grid = Grid(4)
        grid.drop(0, 'X')
        grid.drop(0, 'O')
        row = grid.drop(0, 'X')
        assert grid._columns[0][row].symbol == 'X'

    def test_grid_is_full(self):
        """Test full grid is full"""
        grid = Grid(4)
        for j in range(4):
            for _ in range(4):
                grid.drop(j, 'O')
        assert grid.is_full()

    def test_grid_is_full(self):
        """Test not full grid is not full"""
        grid = Grid(4)
        for j in range(4):
            for _ in range(3):
                grid.drop(j, 'O')
        assert not grid.is_full()

    def test_create_rows_and_columns_rows_are_lines(self):
        """Test rows returned by create_rows and create_columns is a list of
        Lines"""
        squares = create_squares(4)
        rows, columns = create_rows_and_columns(squares)
        assert isinstance(rows[0], Line)

    def test_create_rows_and_columns_columns_are_lines(self):
        """Test columns returned by create_rows and create_columns is a list of
        Lines"""
        squares = create_squares(4)
        rows, columns = create_rows_and_columns(squares)
        assert isinstance(columns[0], Line)

    def test_create_rows_and_columns_squares(self):
        """Test rows and columns returned have rows[i][j] == columns[j][i] """
        squares = create_squares(4)
        rows, columns = create_rows_and_columns(squares)
        assert rows[1][2] == columns[2][1]

    def test_rows_and_columns_length(self):
        """Test the length of rows and columns returned , ie
        len(rows) == len(columns) == n"""
        squares = create_squares(4)
        rows, columns = create_rows_and_columns(squares)
        assert len(rows) == len(columns) == 4

    def test_empty_grid_fiar(self):
        """Test empty grid has no four is a row"""
        grid = Grid(4)
        assert not grid.has_fiar((0, 0))

    def test_grid_row_fiar(self):
        """Test empty grid has no four is a row"""
        grid = Grid(5)
        for j in range(5):
            grid.drop(j, 'O')
        assert grid.has_fiar((4, 3))

    def test_grid_column_fiar(self):
        """Test empty grid has no four is a row"""
        grid = Grid(4)
        for _ in range(4):
            grid.drop(2, 'X')
        assert grid.has_fiar((0, 2))

    def test_grid_out_of_range_fiar(self):
        """Test grid.has_fiar(i, j) could be false with column.has_fiar(i', j')
        true for some (i, j) !== (i', j')"""
        grid = Grid(6)
        for _ in range(4):
            grid.drop(2, 'X')
        assert not grid.has_fiar((0, 2))

    def test_grid_fiar_diagonal(self):
        """Test Grid.fiar() on a diagonal"""
        grid = Grid(5)
        for j in range(4):
            for _ in range(j + 1):
                grid.drop(j, 'X')
        assert grid.has_fiar((1, 3))

    def test_create_mapping_map_length(self):
        """Test the length of list of Lines returned for a corner square == 3"""
        squares = create_squares(4)
        mapping = create_mapping(squares)
        assert len(mapping[(3, 0)]) == 3

    def test_create_mapping_map_middle_length(self):
        """Test the length of list of Lines returned for a middle square with
         down and up diagonals == 4"""
        squares = create_squares(5)
        mapping = create_mapping(squares)
        assert len(mapping[(2, 2)]) == 4

    def test_create_mapping_first_is_row(self):
        """Test first line in mapping is a row"""
        squares = create_squares(4)
        mapping = create_mapping(squares)
        assert is_row(mapping[(2, 2)][0].cells)

    def test_create_mapping_second_is_column(self):
        """Test first line in mapping is a column"""
        squares = create_squares(4)
        mapping = create_mapping(squares)
        assert is_column(mapping[(2, 2)][1].cells)

    def test_create_mapping_second_is_diagonal(self):
        """Test 3rd line in mapping is a diagonal"""
        squares = create_squares(4)
        mapping = create_mapping(squares)
        assert is_diagonal(mapping[(2, 2)][2].cells)


class TestFourInARow:
    def test_x_wins(self) -> None:
        """
        Provided test demonstrating how you can test FourInARow.play using
        a StringIO object to "script" the input.

        See both the handout and the Task 4 section of the supplemental slides
        for a detailed explanation of this example.
        """
        fiar = play_game(GAME_SCRIPT_X_WINS)
        assert fiar.result == WIN

    def test_row_x_win(self):
        """Test a row fiar by X is WIN"""
        fiar = play_game(GAME_SCRIPT_X_ROW_WIN)
        print(fiar.result)
        assert fiar.result == WIN

    def test_up_diag_o_win(self):
        """Test an up diagonal fiar by O is a LOSS"""
        fiar = play_game(GAME_SCRIPT_UP_DIAG_WIN)
        assert fiar.result == LOSS

    def test_down_diag_x_win(self):
        """Test a down diagonal fiar by X is a WIN"""
        fiar = play_game(GAME_SCRIPT_DOWN_DIAG_WIN)
        assert fiar.result == WIN

    def test_draw(self):
        """Test full baord with no fiar is a DRAW"""
        fiar = play_game(GAME_SCRIPT_DRAW)
        assert fiar.result == DRAW
