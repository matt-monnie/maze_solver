from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.geometry(f"{width}x{height}")

        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.configure(background="black")
        self.__canvas.pack(fill=BOTH, expand=True)

        self.__running = False

        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

    def draw_line(self, line, fill_color):
        line.draw(self.__canvas, fill_color)

    def draw_text(self, x, y, text, font=("Arial", 12, "normal"), fill_color="Yellow"):
        self.__canvas.create_text(x, y, text=text, font=font, fill=fill_color)
