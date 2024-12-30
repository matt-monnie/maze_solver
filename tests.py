import unittest
from unittest.mock import Mock, patch

from cell import Cell
from maze import Maze


class TestMaze(unittest.TestCase):

    def setUp(self):
        self.x1 = 0
        self.y1 = 0
        self.num_rows = 5
        self.num_columns = 5
        self.cell_size_x = 10
        self.cell_size_y = 10
        self.mock_window = Mock()

    @patch('maze.Cell')
    def test_create_cells_structure(self, MockCell):
        maze = Maze(
            self.x1,
            self.y1,
            self.num_rows,
            self.num_columns,
            self.cell_size_x,
            self.cell_size_y
        )
        self.assertEqual(len(maze._cells), self.num_columns)
        self.assertEqual(len(maze._cells[0]), self.num_rows)

    @patch('maze.Cell')
    def test_cells_initialized_correctly(self, MockCell):
        MockCell.side_effect = lambda x1, y1, x2, y2, win: Mock()
        Maze(
            self.x1,
            self.y1,
            self.num_rows,
            self.num_columns,
            self.cell_size_x,
            self.cell_size_y
        )
        self.assertTrue(MockCell.called)
        self.assertEqual(MockCell.call_count, self.num_rows * self.num_columns)


    @patch('maze.Cell')
    @patch('maze.time.sleep', return_value=None)
    def test_animate_without_window(self, mock_sleep, MockCell):
        with patch('builtins.print') as mock_print:
            Maze(
                self.x1,
                self.y1,
                self.num_rows,
                self.num_columns,
                self.cell_size_x,
                self.cell_size_y
            )
            mock_print.assert_called_with("Window is not associated with maze")

    @patch('maze.Cell')
    @patch('maze.time.sleep', return_value=None)
    def test_animate_with_window(self, mock_sleep, MockCell):
        mock_window_instance = Mock()

        x1 = 0
        y1 = 0
        num_rows = 5
        num_columns = 5
        cell_size_x = 10
        cell_size_y = 10

        maze = Maze(
            x1,
            y1,
            num_rows,
            num_columns,
            cell_size_x,
            cell_size_y,
            mock_window_instance
        )
        mock_window_instance.redraw.assert_called()


    def test_break_entrance_and_exit(self):
        num_columns = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_columns, 10, 10)
        self.assertFalse(
            m1._cells[0][0].has_top_wall,
            False
        )
        self.assertEqual(
            m1._cells[num_columns - 1][num_rows - 1].has_bottom_wall,
            False
        )

    def test_maze_reset_cells_visited(self):
        num_columns = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_columns, 10, 10)
        for column in m1._cells:
            for cell in column:
                self.assertFalse(cell.visited)

if __name__ == '__main__':
    unittest.main()