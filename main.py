import time
from window import Window
from maze import Maze


# Main
if __name__ == "__main__":
    win = Window(800,600)

    maze = Maze(50,50,15,15,30,30, win, 101)

    time.sleep(5)

    start_time = time.time()


    solved = maze.solve()

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Display the elapsed time on the canvas
    win.draw_text(600, 10, f"Time taken: {elapsed_time:.2f} seconds")

    win.wait_for_close()