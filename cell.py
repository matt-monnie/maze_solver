from geometry import Point, Line

class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        if self._win is None:
            print("Cell is not associated with a window")
            return
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "green")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "green")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "green")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "green")
        # self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black" if self.has_left_wall else "white")

#         self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black" if self.has_right_wall else "white")

#         self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black" if self.has_top_wall else "white")

#         self._win.draw_line(Line(Point(self._x1, self._y2), Point(self._x2, self._y2)), "black" if self.has_bottom_wall else "white")


    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        from_center = Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)
        to_center = Point((to_cell._x1 + to_cell._x2) / 2, (to_cell._y1 + to_cell._y2) / 2)
        move_line = Line(from_center, to_center)
        self._win.draw_line(move_line, color)
