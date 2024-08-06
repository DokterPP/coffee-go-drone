import turtle
import sys
import tkinter as tk
from maze.tile import Tile
from generate_maze import Maze_Generator
from Algorithms import left_hand, depth_first, breadth_first, astar
from movement import Move_Turtle

# Define constants
TILE_SIZE = 20
MAZE_FILE = 'maze.txt'

# Global variables to store the initial start position and the solved path
initial_start_position = None
solved_path_coordinates = []

def read_file_from_argument():
    try:
        with open(MAZE_FILE, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"The file {MAZE_FILE} was not found.")
        sys.exit(1)

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
            elif char == 's':
                tile_drawer.draw_tile(screen_x, screen_y, 'lime', TILE_SIZE, 's', 'lime green')
                start_position = (screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2)
            elif char == 'e':
                tile_drawer.draw_tile(screen_x, screen_y, 'cyan', TILE_SIZE, 'e', 'royal blue')
            elif char == '-':
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
                tile_drawer.draw_circle(screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2, 'yellow', TILE_SIZE / 3)  # Draw circle
            else:
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
    screen.tracer(1, 0)  # Enable automatic screen updates            
    screen.update()  # Update the screen once all the tiles are drawn
    return start_position

def generate_new_maze(t, tile_drawer):
    global initial_start_position, solved_path_coordinates
    
    generate_button.config(state=tk.DISABLED)  # Disable the button
    disable_key_controls()  # Disable key controls
    
    # Move the turtle back to the initial starting position before generating the maze
    if initial_start_position:
        Move_Turtle().move_turtle_to_start(t, initial_start_position)

    maze_rand = Maze_Generator().generate_maze_final()
    Maze_Generator().write_maze_to_file(maze_rand, MAZE_FILE)
    maze_str = read_file_from_argument()
    initial_start_position = draw_maze(maze_str, t, tile_drawer)  # Save the new starting position
    solved_path_coordinates = []  # Clear any previous path
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    screen.update()
    
    generate_button.config(state=tk.NORMAL)  # Re-enable the button
    enable_key_controls()  # Re-enable key controls

def disable_key_controls():
    screen.onkey(None, 'Up')
    screen.onkey(None, 'Down')
    screen.onkey(None, 'Left')
    screen.onkey(None, 'Right')
    screen.onkey(None, 'r')
    screen.onkey(None, 'g')

def enable_key_controls():
    
    screen.onkey(lambda: Move_Turtle().move_up(t, TILE_SIZE), 'Up')
    screen.onkey(lambda: Move_Turtle().move_down(t, TILE_SIZE), 'Down')
    screen.onkey(lambda: Move_Turtle().move_left(t, TILE_SIZE), 'Left')
    screen.onkey(lambda: Move_Turtle().move_right(t, TILE_SIZE), 'Right')
    screen.onkey(lambda: solve_maze(t, tile_drawer), 'r')
    screen.onkey(lambda: follow_path(t), 'g')

def solve_maze(t, tile_drawer):
    global initial_start_position, solved_path_coordinates
    solve_button.config(state=tk.DISABLED)  # Disable the button
    generate_button.config(state=tk.DISABLED)  # Disable the button
    disable_key_controls()  # Disable key controls
    # Move the turtle back to the initial starting position before solving the maze
    if initial_start_position:
        Move_Turtle().move_turtle_to_start(t, initial_start_position)

    maze_str = read_file_from_argument()
    maze = string_to_maze(maze_str)
    
    if selected_algorithm.get() == "left_hand":
        solved_maze, solved_path = left_hand.solve_maze(maze)
    elif selected_algorithm.get() == "depth_first":
        solved_maze, solved_path = depth_first.solve_maze_dfs(maze)
    elif selected_algorithm.get()== "breadth_first":
        solved_maze, solved_path  = breadth_first.solve_maze_bfs(maze)
    elif selected_algorithm.get() == "a_star":
        solved_maze, solved_path  = astar.solve_maze_astar(maze)
    # Convert the solved maze list back to a string
    solved_maze_str = '\n'.join([''.join(row) for row in solved_maze])
    solved_path_coordinates = solved_path
    initial_start_position = draw_maze(solved_maze_str, t, tile_drawer)  # Save the new starting position
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    screen.update()
    
    generate_button.config(state=tk.NORMAL)  # Re-enable the button
    solve_button.config(state=tk.NORMAL)  # Re-enable the button
    enable_key_controls()  # Re-enable key controls
    
def string_to_maze(maze_str):
    return [list(row) for row in maze_str.split('\n') if row]

def follow_path(t):
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    global solved_path_coordinates
    generate_button.config(state=tk.DISABLED)  # Disable the button
    solve_button.config(state=tk.DISABLED)  # Disable the button
    disable_key_controls()  
    if not solved_path_coordinates:
            print("No path to follow.")
            generate_button.config(state=tk.NORMAL)  # Re-enable the button
            solve_button.config(state=tk.NORMAL)  # Re-enable the button
            enable_key_controls()  
            return
    print("Path coordinates:", solved_path_coordinates)
    # Follow the path step by step in sequence
    
    t.penup()
    for i in range(1, len(solved_path_coordinates)):
        current_position = solved_path_coordinates[i - 1]
        next_position = solved_path_coordinates[i]
        print(f"Moving from {current_position} to {next_position}")
        t.speed(1)
        # Calculate the direction to move
        if next_position[0] > current_position[0]:
            t.setheading(0)  # Facing East (right)
            t.forward(TILE_SIZE)
        elif next_position[0] < current_position[0]:
            t.setheading(180)  # Facing West (left)
            t.forward(TILE_SIZE)
        elif next_position[1] > current_position[1]:
            t.setheading(270)  # Facing North (up)
            t.forward(TILE_SIZE)
        elif next_position[1] < current_position[1]:
            t.setheading(90)  # Facing South (down)
            t.forward(TILE_SIZE)

        screen.update()
    t.pendown()
    generate_button.config(state=tk.NORMAL)  # Re-enable the button
    solve_button.config(state=tk.NORMAL)  # Re-enable the button
    enable_key_controls()  
    
    
def main():
    global selected_algorithm
    global generate_button
    global solve_button
    global screen
    global t
    global tile_drawer
    root = tk.Tk()
    root.title("Maze Generator with Turtle")

    canvas = tk.Canvas(root, width=1000, height=700)
    canvas.pack(fill=tk.BOTH, expand=True)

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("white")
    
    t = turtle.RawTurtle(screen)
    t.speed(1)
    t.fillcolor('red')  # Set turtle fill color
    t.showturtle()  # Ensure the turtle is visible
    t.pencolor('black')  # Set the pen color explicitly
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
    astar_radio = tk.Radiobutton(algorithm_frame, text="A* Search", variable=selected_algorithm, value="a_star")

    left_hand_radio.pack(side=tk.LEFT)
    depth_first_radio.pack(side=tk.LEFT)
    breadth_first_radio.pack(side=tk.LEFT)
    astar_radio.pack(side=tk.LEFT)
    
    screen.onkey(lambda: solve_maze(t, tile_drawer), 'r')
    screen.onkey(lambda: follow_path(t), 'g')
    enable_key_controls()

    screen.listen()
    
    root.mainloop()

if __name__ == "__main__":
    main()