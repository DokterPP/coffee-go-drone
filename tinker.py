import turtle
import sys
import tkinter as tk
from maze.tile import Tile
from generate_maze import Maze_Generator
from Algorithms import left_hand, depth_first, breadth_first

# Define constants
TILE_SIZE = 20
MAZE_FILE = 'maze.txt'

def read_file_from_argument():
    try:
        with open(MAZE_FILE, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {MAZE_FILE} was not found.")
        sys.exit(1)

def move_turtle_to_start(t, position):
    if position:
        x, y = position
        t.penup()
        t.goto(x, y)
        t.pendown()

def draw_maze(maze, t, tile_drawer):
    screen.tracer(0, 0)  # Disable automatic screen updates
    t.clear()  # Clear previous drawings

    maze_lines = maze.splitlines()
    maze_height = len(maze_lines)
    maze_width = len(maze_lines[0]) if maze_lines else 0

    start_x = -maze_width * TILE_SIZE / 2
    start_y = maze_height * TILE_SIZE / 2
    
    start_position = None

    for y, row in enumerate(maze_lines):
        for x, char in enumerate(row):
            screen_x = start_x + x * TILE_SIZE
            screen_y = start_y - y * TILE_SIZE
            if char == 'X':
                tile_drawer.draw_tile(screen_x, screen_y, 'grey', TILE_SIZE)
            elif char == '.':
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
            elif char == 's':
                tile_drawer.draw_tile(screen_x, screen_y, 'lime', TILE_SIZE, 's', 'lime green')
                start_position = (screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2)
            elif char == 'e':
                tile_drawer.draw_tile(screen_x, screen_y, 'cyan', TILE_SIZE, 'e', 'royal blue')
            elif char == '-':
                tile_drawer.draw_tile(screen_x, screen_y, 'yellow', TILE_SIZE)
            elif char == ',':
                tile_drawer.draw_tile(screen_x, screen_y, 'red', TILE_SIZE)
    
    screen.update()  # Update the screen once all the tiles are drawn
    return start_position

def generate_new_maze(t, tile_drawer):
    maze_rand = Maze_Generator().remove_random_walls()
    Maze_Generator().write_maze_to_file(maze_rand, MAZE_FILE)
    maze_str = read_file_from_argument()
    start_position = draw_maze(maze_str, t, tile_drawer)
    move_turtle_to_start(t, start_position)

def solve_maze(t, tile_drawer):
    maze_str = read_file_from_argument()
    maze = string_to_maze(maze_str)
    
    if selected_algorithm.get() == "left_hand":
        solved_maze = left_hand.solve_maze(maze)
    elif selected_algorithm.get() == "depth_first":
        solved_maze = depth_first.solve_maze_dfs(maze)
    elif selected_algorithm.get()== "breadth_first":
        solved_maze = breadth_first.solve_maze_bfs(maze)
    # Convert the solved maze list back to a string
    solved_maze_str = '\n'.join([''.join(row) for row in solved_maze])

    start_position = draw_maze(solved_maze_str, t, tile_drawer)
    move_turtle_to_start(t, start_position)

def string_to_maze(maze_str):
    return [list(row) for row in maze_str.split('\n') if row]

def main():
    global selected_algorithm

    root = tk.Tk()
    root.title("Maze Generator with Turtle")

    canvas = tk.Canvas(root, width=900, height=700)
    canvas.pack(fill=tk.BOTH, expand=True)

    global screen
    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("white")
    
    t = turtle.RawTurtle(screen)
    t.speed(0)

    tile_drawer = Tile(t)

    generate_button = tk.Button(root, text="Generate New Maze", command=lambda: generate_new_maze(t, tile_drawer))
    solve_button = tk.Button(root, text="Solve Maze", command=lambda: solve_maze(t, tile_drawer))
    
    generate_button.pack(side=tk.BOTTOM)
    solve_button.pack(side=tk.BOTTOM)

    algorithm_frame = tk.Frame(root)
    algorithm_frame.pack(side=tk.BOTTOM)

    selected_algorithm = tk.StringVar(value="left_hand")

    left_hand_radio = tk.Radiobutton(algorithm_frame, text="Left Hand", variable=selected_algorithm, value="left_hand")
    depth_first_radio = tk.Radiobutton(algorithm_frame, text="Depth First", variable=selected_algorithm, value="depth_first")
    breadth_first_radio = tk.Radiobutton(algorithm_frame, text="Breadth First", variable=selected_algorithm, value="breadth_first")

    left_hand_radio.pack(side=tk.LEFT)
    depth_first_radio.pack(side=tk.LEFT)
    breadth_first_radio.pack(side=tk.LEFT)

    screen.onkey(lambda: solve_maze(t, tile_drawer), 'r')
    screen.listen()
    root.mainloop()

if __name__ == "__main__":
    main()
