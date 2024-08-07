import turtle
import os
import sys
import tkinter as tk
from tkinter import Toplevel, Entry, Button, messagebox
from maze.tile import Tile
from maze.generate_maze import Maze_Generator
from maze.movement import Move_Turtle
from maze.maze_validator import Validator

from Algorithms.left_hand import LeftHand_MazeSolver
from Algorithms.depth_first import DepthFirst_MazeSolver
from Algorithms.breadth_first import BreadthFirst_MazeSolver
from Algorithms.astar import AStar_MazeSolver


# Define constants
TILE_SIZE = 20
MAZE_FILE = 'maze.txt'
DEFAULT_MAZE = 'default.txt'
FILE_IN_PLAY = None
steps = 0
point = 's'
maze_str = None
paused = False
continue_flag = False
show_path = True

# Global variables to store the initial start position and the solved path
initial_start_position = None
solved_path_coordinates = []


# HELPER FUNCTIONS
# change it such that if a file is passed as an argument, it will read the file and generate the maze
def read_file_from_argument(file_name=None):
    global FILE_IN_PLAY
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        try:
            # Open and read the file
            with open(file_name, 'r') as file:
                content = file.read()
                FILE_IN_PLAY = file_name
                return content
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
    else:
        print("Please provide a text file as an argument.")
        return read_file(DEFAULT_MAZE)

        
def read_file(file_name=None):
    global FILE_IN_PLAY
    if file_name:
        try:
            # Open and read the file
            with open(file_name, 'r') as file:
                content = file.read()
                FILE_IN_PLAY = file_name
                return content
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
    else:
        print("Please provide a text file as an argument.")

def string_to_maze(maze_str):
    return [list(row) for row in maze_str.split('\n') if row]

  
def disable_key_controls():
    screen.onkey(None, 'Up')
    screen.onkey(None, 'Down')
    screen.onkey(None, 'Left')
    screen.onkey(None, 'Right')
    screen.onkey(None, 'f')
    screen.onkey(None, 'g')
    screen.onkey(None, 'r')
    screen.onkey(None, 'h')

def disable_buttons():
    generate_button.config(state=tk.DISABLED)
    solve_button.config(state=tk.DISABLED)
    file_input_button.config(state=tk.DISABLED)
    show_path_label.config(state=tk.DISABLED)
    
def enable_key_controls():
    global maze_str
    screen.onkey(lambda: move('U'), 'Up')
    screen.onkey(lambda: move('D'), 'Down')
    screen.onkey(lambda: move('L'), 'Left')
    screen.onkey(lambda: move('R'), 'Right')
    screen.onkey(lambda: solve_maze(t, tile_drawer), 'f')
    screen.onkey(lambda: follow_path(t), 'g')
    screen.onkey(lambda: reset_position(), 'r')
    screen.onkey(lambda: toggle_path_visibility(), 'h')

def enable_buttons():
    generate_button.config(state=tk.NORMAL)
    solve_button.config(state=tk.NORMAL)
    file_input_button.config(state=tk.NORMAL)  
    show_path_label.config(state=tk.NORMAL)
    
def toggle_pause(event=None):
    global paused
    paused = not paused
    if paused:
        update_status("pause", "Autopilot Paused")
    else:
        update_status("pause", "Autopilot active")

def quit_application():
    root.quit()

def wait_for_continue(event=None):
    global continue_flag, steps
    disable_key_controls()
    disable_buttons()
    content = "Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)"
    update_label(content)
    gx,gy,x,y = find_position()
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    solved_path_coordinates.clear()
    draw_maze(maze_str, t, tile_drawer)
    Move_Turtle().move_turtle_to_start(t, (x, y))
    steps = 0
    root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    screen.update()
    enable_key_controls()
    enable_buttons()
    continue_flag = True

def wait_for_enter():
    global enter_flag
    enter_flag = False
    disable_buttons()
    disable_key_controls()
    def on_enter_press(event):
        global enter_flag
        enter_flag = True
    root.bind('<Return>', on_enter_press)
    while not enter_flag:
        screen.update()
        screen.ontimer(lambda: None, 100)  # Wait for 100ms before checking again
    root.unbind('<Return>')
    enable_key_controls()
    enable_buttons()
        
def toggle_path_visibility(event=None):
    global show_path
    show_path = not show_path
    disable_key_controls()
    disable_buttons()
    gx,gy,x,y = find_position()
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    draw_maze(maze_str, t, tile_drawer)  # Redraw the maze with the updated path visibility
    Move_Turtle().move_turtle_to_start(t, (x, y))
    enable_key_controls()
    enable_buttons()


def reset_position(event=None):
    # Reset the turtle to the starting point
    global initial_start_position, steps
    disable_key_controls()
    disable_buttons()
    content = "Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)"
    update_label(content)
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    solved_path_coordinates.clear()
    draw_maze(maze_str, t, tile_drawer)
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    steps = 0
    root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    screen.update()
    enable_key_controls()
    enable_buttons()
    
    
def update_label(new_content):
    label_turtle.clear()  # Clear the previous text
    label_turtle.write(f"DRONE STATUS= {new_content}", align="center", font=("Helvetica", 12))
    
def update_status(which, new_status):
    if which == "pause":
        status_pause_label.config(text=f"Status: {new_status}")
        status_pause_label.update()
    else:  
        status_path_label.config(text=f"Status: {new_status}")
        status_path_label.update()
        
# Movement functions
def move(direction):
    
    global maze_str, screen
    global new_x, new_y
    global steps
    disable_buttons()
    disable_key_controls()
    global point 
    
    if direction == 'U':
        new_x, new_y = t.xcor(), t.ycor() + TILE_SIZE
        if Move_Turtle().is_move_valid(start_x,start_y, new_x, new_y, maze_str, TILE_SIZE):
            Move_Turtle().move_up(t, TILE_SIZE)
            point == 'n'
            steps += 1
            root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    if direction == 'D':
        new_x, new_y = t.xcor(), t.ycor() - TILE_SIZE
        if Move_Turtle().is_move_valid(start_x,start_y, new_x, new_y, maze_str, TILE_SIZE):
            Move_Turtle().move_down(t, TILE_SIZE)
            point == 'n'
            steps += 1
            root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    if direction == 'L':
        new_x, new_y = t.xcor() - TILE_SIZE, t.ycor()
        if Move_Turtle().is_move_valid(start_x,start_y, new_x, new_y, maze_str, TILE_SIZE):
            Move_Turtle().move_left(t, TILE_SIZE)
            point == 'n'
            steps += 1
            root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    if direction == 'R':
        new_x, new_y = t.xcor() + TILE_SIZE, t.ycor()
        if Move_Turtle().is_move_valid(start_x,start_y, new_x, new_y, maze_str, TILE_SIZE):
            Move_Turtle().move_right(t, TILE_SIZE)
            point == 'n'
            steps += 1
            root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")

        
    enable_key_controls()
    enable_buttons()

def draw_maze(maze, t, tile_drawer):
    global start_x, start_y, maze_height, maze_width, screen_x, screen_y, solved_path_coordinates
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
                tile_drawer.draw_tile(screen_x, screen_y, 'lime', TILE_SIZE, 's', 'green')
                start_position = (screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2)
            elif char == 'e':
                tile_drawer.draw_tile(screen_x, screen_y, 'cyan', TILE_SIZE, 'e', 'royal blue')
            elif char == '-':
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
            elif char == '.':
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
            elif char == ',':
                tile_drawer.draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
            else:
                raise ValueError(f"Invalid character in maze: '{char}' at position ({x}, {y})")
    
    if show_path:
        update_status('path',"Showing path")
        for step in solved_path_coordinates:
            x, y = step
            screen_x = start_x + x * TILE_SIZE
            screen_y = start_y - y * TILE_SIZE
            tile_drawer.draw_circle(screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2, 'yellow', TILE_SIZE / 3)
    else:
        update_status('path',"Path hidden")
    screen.tracer(1, 0)  # Enable automatic screen updates            
    screen.update()  # Update the screen once all the tiles are drawn
    return start_position

def generate_new_maze(t, tile_drawer):
    global initial_start_position, solved_path_coordinates, maze_rand, steps, maze_str
    steps = 0
    root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    disable_buttons() # Disable the button
    disable_key_controls()  # Disable key controls
    content = "Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)"
    update_label(content)
    log_text.config(text=" ")
    log_text.update()
    # Move the turtle back to the initial starting position before generating the maze
    if initial_start_position:
        Move_Turtle().move_turtle_to_start(t, initial_start_position)

    maze_rand = Maze_Generator().generate_maze_final()
    Maze_Generator().write_maze_to_file(maze_rand, MAZE_FILE)
    maze_str = read_file(MAZE_FILE)
    solved_path_coordinates = []
    initial_start_position = draw_maze(maze_str, t, tile_drawer)  # Save the new starting position
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    screen.update()
    
    enable_buttons()  # Re-enable the button
    enable_key_controls()  # Re-enable key controls


def find_position():
    global start_x, start_y
    
    x, y = t.xcor(), t.ycor()
    grid_x = int((x - start_x) // TILE_SIZE)  # Convert x to grid index
    grid_y = int((start_y - y) // TILE_SIZE)  # Convert y to grid index
    return grid_x, grid_y, x, y

def solve_maze(t, tile_drawer):
    global initial_start_position, solved_path_coordinates
    global gx, gy, x, y
    disable_buttons()  # Disable the button
    disable_key_controls()  # Disable key controls
    # Move the turtle back to the initial starting position before solving the maze
    gx,gy,x,y = find_position()
    t.setheading(0)  # Set the turtle to face up
    maze_str = read_file(FILE_IN_PLAY)
    maze = string_to_maze(maze_str)

## Using Left Hand
    if selected_algorithm.get() == "left_hand":
        left_hand_solver = LeftHand_MazeSolver(gx, gy, maze)
        solved_maze, solved_path = left_hand_solver.solve()

## Using Depth First
    elif selected_algorithm.get() == "depth_first":
        depth_first_solver = DepthFirst_MazeSolver(gx, gy, maze)
        solved_maze, solved_path = depth_first_solver.solve_maze_dfs()

## Using Breadth First
    elif selected_algorithm.get()== "breadth_first":
        breadth_first_solver = BreadthFirst_MazeSolver(gx, gy, maze)
        solved_maze, solved_path = breadth_first_solver.solve_maze_bfs()

## Using A Star
    elif selected_algorithm.get() == "a_star":
        astar_solver = AStar_MazeSolver(gx, gy, maze)
        solved_maze, solved_path = astar_solver.solve_maze_astar()



    # Convert the solved maze list back to a string
    solved_maze_str = '\n'.join([''.join(row) for row in solved_maze])
    solved_path_coordinates = solved_path
    initial_start_position = draw_maze(solved_maze_str, t, tile_drawer)  # Save the new starting position
    Move_Turtle().move_turtle_to_start(t,(x,y))
    screen.update()
    
    enable_buttons()# Re-enable the button
    enable_key_controls()  # Re-enable key controls
    
def follow_path(t):
    global paused, continue_flag
    global solved_path_coordinates, steps
    if not solved_path_coordinates:
        print("No path to follow.")
        return

    Move_Turtle().move_turtle_to_start(t, (x, y))
    screen.tracer(1, 10)  # Disable automatic screen updates
    content = "Automatic Pilot: Following pre-calculated path. Press ‘p’ to toggle pause/resume."
    update_label(content)
    steps = 0
    disable_buttons()
    disable_key_controls()
    if not solved_path_coordinates:
        print("No path to follow.")
        enable_buttons()
        enable_key_controls()
        return
    # Follow the path step by step in sequence

    t.penup()
    for i in range(1, len(solved_path_coordinates)):
        while paused:
            screen.update()
            screen.ontimer(lambda: None, 100)  # Wait for 100ms before checking again

        current_position = solved_path_coordinates[i - 1]
        next_position = solved_path_coordinates[i]
        steps += 1
        root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
        t.speed(1)
        t.penup()
        screen.tracer(1, 10)
        # Calculate the direction to move
        if next_position[0] > current_position[0]:
            t.setheading(0)  # Facing East (right)
            t.penup()
            t.forward(TILE_SIZE)
        elif next_position[0] < current_position[0]:
            t.setheading(180)  # Facing West (left)
            t.penup()
            t.forward(TILE_SIZE)
        elif next_position[1] > current_position[1]:
            t.setheading(270)  # Facing South (down)
            t.penup()
            t.forward(TILE_SIZE)
        elif next_position[1] < current_position[1]:
            t.setheading(90)  # Facing North (up)
            t.penup()
            t.forward(TILE_SIZE)

        screen.update()
    t.pendown()
    screen.tracer(1, 0)  # Enable automatic screen updates
        # Wait for the user to press 'c' before enabling key controls
    continue_flag = False
    px,py = next_position
    
    content = f"Automatic Pilot: Destination {(py,px)} reached in {steps} steps. Press ‘c’ to continue."
    update_label(content)
    while not continue_flag:
        screen.update()
        screen.ontimer(lambda: None, 100)  # Wait for 100ms before checking again
        
    

    
def run_called_maze(option=None):
    global initial_start_position, solved_path_coordinates, maze_str
    
    disable_buttons()  # Disable the button
    disable_key_controls()  # Disable key controls
    
    # Move the turtle back to the initial starting position before generating the maze
    if initial_start_position:
        Move_Turtle().move_turtle_to_start(t, initial_start_position)
    if option == None:    
        maze_str = read_file_from_argument()
    else:
        maze_str = read_file(option)
    maze = string_to_maze(maze_str)
    passed , error = Validator().run_all_checks(maze)
    if not passed:
        print("Maze failed validation checks. Please provide a valid maze.")
        error = error + "\n Press Enter to continue to generate random maze..."
        log_text.config(text=error)
        log_text.update()
        print("Press Enter to continue...")
        wait_for_enter()
        generate_new_maze(t, tile_drawer)
        return
    content = "Manual Mode: Use arrow keys to navigate (press ‘f’ to calculate shortest path)"
    update_label(content)
    initial_start_position = draw_maze(maze_str, t, tile_drawer)  # Save the new starting position
    solved_path_coordinates = []  # Clear any previous path
    Move_Turtle().move_turtle_to_start(t, initial_start_position)
    screen.update()
    
    enable_buttons() # Re-enable the button
    enable_key_controls()  # Re-enable key controls


def open_file_input_window():
    # Create a new window
    global FILE_IN_PLAY, initial_start_position
    file_input_window = Toplevel(root)
    file_input_window.title("Input File")
    disable_buttons() # Disable the button
    disable_key_controls() 
    # Create a label and text entry for file input
    file_label = tk.Label(file_input_window, text="Enter file path:", font='Helvetica 10')
    file_label.grid(padx=10, pady=10, row=0, column=0)

    file_entry = Entry(file_input_window, width=50)
    file_entry.grid(padx=10, pady=10, row=0, column=1)
    
    def submit_file(initial_start_position):

        if initial_start_position:
            Move_Turtle().move_turtle_to_start(t, initial_start_position)
        file_path = file_entry.get()

        # Check if the file has a .txt extension
        if not file_path.endswith('.txt'):
            messagebox.showerror("Invalid File", "Please select a file with a .txt extension.")
            enable_buttons()
            enable_key_controls()
            file_input_window.lift()
            return

        # Check if the file exists
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", "The specified file does not exist.")
            enable_buttons()
            enable_key_controls()
            file_input_window.lift()
            return     
        
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                FILE_IN_PLAY = file_path
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            
        maze = string_to_maze(content)
        passed , error = Validator().run_all_checks(maze)
        
        if not passed:
            print("Maze failed validation checks. Please provide a valid maze.")
            error = error + "\n Press Enter to continue to generate random maze..."
            log_text.config(text=error)
            log_text.update()
            print("Press Enter to continue...")
            wait_for_enter()
            generate_new_maze(t, tile_drawer)
            file_input_window.destroy()
            
            return
        else:
            run_called_maze(file_path)
            file_input_window.destroy()
        
    def cancel_file_input():
        enable_buttons()
        enable_key_controls()
        file_input_window.destroy()

    #if the window is closed, enable the buttons and key controls
    file_input_window.protocol("WM_DELETE_WINDOW", lambda: cancel_file_input())
    
    # Create a submit button
    submit_button = Button(file_input_window, text="Submit", command= lambda: submit_file(initial_start_position))
    cancel_button = Button(file_input_window, text="Cancel", command= lambda: cancel_file_input())
    submit_button.grid(padx=75, pady=10, row=1, column=1, sticky='nsew')
    cancel_button.grid(padx=75, pady=10, row=1, column=0, sticky='nsew')


        
def main():
    global selected_algorithm
    global generate_button
    global solve_button
    global screen
    global t
    global tile_drawer
    global root
    global steps
    global content
    global label_turtle
    global statuses, status_pause_label, status_path_label, error, log_text, file_input_button, show_path_label
    
    root = tk.Tk()
    root.title(f"COFFEE~GO~DRONE: Distance travelled ({steps})")
    
    canvas = tk.Canvas(root, width=1000, height=800)
    canvas.grid(padx=2, pady=2, row=0, column=0, rowspan=10, columnspan=10) # , sticky='nsew')

    screen = turtle.TurtleScreen(canvas)
    screen.bgcolor("white")
    content = " "
    statuses = "Autopilot active"
    error = " "
    t = turtle.RawTurtle(screen)
    t.speed(1)
    t.fillcolor('red')  # Set turtle fill color
    t.showturtle()  # Ensure the turtle is visible
    t.pencolor('black')  # Set the pen color explicitly
    
    
    title_turtle = turtle.RawTurtle(screen)
    title_turtle.hideturtle()
    title_turtle.penup()
    title_turtle.goto(0, 340)  # Position the label above the maze
    title_turtle.write("COFFEE~GO~DRONE: Done by Surya & Steve DAAA/2A/02", align="center", font=("Helvetica", 16))
    # Create a turtle for the label
    label_turtle = turtle.RawTurtle(screen)
    label_turtle.hideturtle()
    label_turtle.penup()

    label_turtle.goto(0, 310)  # Position the label above the maze
    label_turtle.write(f"DRONE STATUS= {content}", align="center", font=("Helvetica", 12))

    tile_drawer = Tile(t)
    generate_button = tk.Button(root, text="Generate New Maze", command=lambda: generate_new_maze(t, tile_drawer), bg='#d3d3d3')
    solve_button = tk.Button(root, text="Solve Maze", command=lambda: solve_maze(t, tile_drawer), bg='#d3d3d3')
    
    generate_button.grid(padx=75, pady=10, row=0, column=11, sticky='nsew')
    solve_button.grid(padx=75, pady=10, row=1, column=11, sticky='nsew')
    
    algorithm_frame = tk.Frame(root)
    algorithm_frame.grid(padx=2, pady=2, row=3, column=11, sticky='nsew')
    algorithm_frame.grid_rowconfigure(0, weight=1)
    algorithm_frame.grid_columnconfigure(0, weight=1)
    #add text to the frame make the font bold
    
    file_input_button = Button(root, text="Input File", command=open_file_input_window , bg='#d3d3d3')
    file_input_button.grid(padx=75, pady=10, row=2, column=11, sticky='nsew')

    
    algorithm_label = tk.Label(algorithm_frame, text="Select Algorithm", font='Helvetica 13 bold underline' )
    algorithm_label.grid(padx=2, pady=2, row=0, column=0, columnspan=4, sticky='nsew')
    
    radio_frame = tk.Frame(algorithm_frame, bg='#d3d3d3', bd=2, relief='groove')
    radio_frame.grid(padx=2, pady=2, row=1, column=0, columnspan=4, sticky='nsew')
    
    selected_algorithm = tk.StringVar(value="left_hand")
    left_hand_radio = tk.Radiobutton(radio_frame, text="Left Hand", variable=selected_algorithm, value="left_hand", bg='#d3d3d3')
    depth_first_radio = tk.Radiobutton(radio_frame, text="Depth First", variable=selected_algorithm, value="depth_first", bg='#d3d3d3')
    breadth_first_radio = tk.Radiobutton(radio_frame, text="Breadth First", variable=selected_algorithm, value="breadth_first", bg='#d3d3d3')
    astar_radio = tk.Radiobutton(radio_frame, text="A* Search", variable=selected_algorithm, value="a_star", bg='#d3d3d3')

    left_hand_radio.grid(padx=2, pady=2, row=1, column=0)
    depth_first_radio.grid(padx=2, pady=2, row=1, column=1)
    breadth_first_radio.grid(padx=2, pady=2, row=1, column=2)
    astar_radio.grid(padx=2, pady=2, row=1, column=3)
    
    status_frame = tk.Frame(root)
    status_frame.grid(padx=2, pady=2, row=4, column=11, sticky='nsew')
    
    status_frame.grid_rowconfigure(0, weight=1)
    status_frame.grid_columnconfigure(0, weight=1)
    
    status_pause_label = tk.Label(status_frame, text=f"AutoPilot Status: {statuses}", font='Helvetica 12 ')
    status_pause_label.grid(padx=2, pady=2, row=0, column=0, sticky='nsew')
    
    status_path_label = tk.Label(status_frame, text=f"Path Status: {statuses}", font='Helvetica 12 ')
    status_path_label.grid(padx=2, pady=2, row=1, column=0, sticky='nsew')
    
    log_frame = tk.Frame(root)
    log_frame.grid(padx=2, pady=2, row=5, column=11, sticky='nsew')
    
    log_frame.grid_rowconfigure(0, weight=1)
    log_frame.grid_columnconfigure(0, weight=1)
    
    log_text = tk.Label(log_frame, text=error, font='Helvetica 10 bold', fg='red')
    log_text.grid(row=0, column=0, sticky='nsew')

    move_frame = tk.Frame(root)
    move_frame.grid(padx=2, pady=2, row=6, column=11, sticky='nsew')
    
    move_frame.grid_rowconfigure(0, weight=1)
    move_frame.grid_columnconfigure(0, weight=1)
    
    pause_label = tk.Button(move_frame, text="Toggle Pause", command= lambda: toggle_pause(), bg='#d3d3d3' )
    pause_label.grid(padx=20, pady=2, row=0, column=0, sticky='nsew')
    
    show_path_label = tk.Button(move_frame, text="Toggle Path Visibility", command= lambda: toggle_path_visibility(), bg='#d3d3d3')
    show_path_label.grid(padx=20, pady=2, row=0, column=1, sticky='nsew')
    
    screen.onkey(lambda: solve_maze(t, tile_drawer), 'f')
    screen.onkey(lambda: follow_path(t), 'g')
    run_called_maze()
    enable_key_controls()
    screen.onkey(lambda: toggle_pause(), 'p')
    screen.onkey(lambda: wait_for_continue(), 'c')
    screen.onkey(lambda: quit_application(), 'q')

    screen.listen()
    
    root.mainloop()

if __name__ == "__main__":
    main()