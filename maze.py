import random
import time
from cell import Cell

class Maze:
    def __init__(self, x1, y1, num_rows, num_columns, cell_size_x, cell_size_y, win=None, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_columns = num_columns
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._cells = []
        self._create_cells()


        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_columns):
            column = []
            for j in range(self._num_rows):
                x1 = self._x1 + i * self._cell_size_x
                y1 = self._y1 + j * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y
                cell = Cell(x1, y1, x2, y2, self._win)
                column.append(cell)
            self._cells.append(column)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)

        for i in range(self._num_columns):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

        self._animate()

    def _draw_cell(self, i, j):
        if self._win is None:
            print("Window is not associated with maze")
            return

        self._cells[i][j].draw()


    def _animate(self):
        if self._win is None:
            print("Window is not associated with maze")
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        if self._win is None:
            print("Window is not associated with maze")

        # Break the entrance at the top of the top-left cell
        self._cells[0][0].has_top_wall = False
        # self._draw_cell(0, 0)

        # Break the exit at the bottom of the bottom-right cell
        self._cells[self._num_columns - 1][self._num_rows - 1].has_bottom_wall = False
        # self._draw_cell(self._num_columns - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self._num_columns - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self._draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False


    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, current_row, current_column):
        self._animate()
        self._cells[current_row][current_column].visited = True

        # Check if the current cell is the "end" cell
        if self._is_end_cell(current_row, current_column):
            return True

        # Define possible directions: (dx, dy, wall_check_function)
        directions = [
            (0, -1, self._cells[current_row][current_column].has_top_wall),  # Up
            (0, 1, self._cells[current_row][current_column].has_bottom_wall),  # Down
            (-1, 0, self._cells[current_row][current_column].has_left_wall),  # Left
            (1, 0, self._cells[current_row][current_column].has_right_wall),  # Right
        ]

        for dx, dy, wall_type in directions:
            next_row, next_column = current_row + dx, current_column + dy

            is_valid_cell = (
                0 <= next_row < self._num_columns
                and 0 <= next_column < self._num_rows
                and not self._cells[next_row][next_column].visited
                and self.can_access(wall_type)
            )

            if is_valid_cell:
                # Draw the move between the current cell and the next cell
                self._cells[current_row][current_column].draw_move(self._cells[next_row][next_column])

                # Recursively try solving from the next cell
                if self._solve_r(next_row, next_column):
                    return True

                # If solution was not found, undo the move
                self._cells[next_row][next_column].draw_move(self._cells[current_row][current_column], undo=True)

        # If no directions worked, return False (loser cell)
        return False

    def _is_end_cell(self, row, column):
        """ Check if the cell is the goal (end cell)"""
        return row == self._num_columns - 1 and column == self._num_rows - 1


    def can_access(self, wall_present):
        """ Return True if the wall restriction for the move is not present."""
        return not wall_present
