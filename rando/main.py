import sys
import os
import tkinter as tk
from generate_maze import Maze_Generator
import random
from Algorithms import left_hand
from tkinter import messagebox
from tkinter import Canvas, Button
import turtle
import time

def read_file_from_argument():
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        try:
            # Open and read the file
            with open(file_name, 'r') as file:
                content = file.read()
                return content
        except FileNotFoundError:
            print(f"The file {file_name} was not found.")
    else:
        print("Please provide a text file as an argument.")

def draw_maze(maze, canvas):
    # check how big maze map is 
   
    canvas.delete("all")  # Clear the canvas to redraw

    if isinstance(maze, str):
        maze_lines = maze.splitlines()
    elif isinstance(maze, list):
        maze_lines = maze  # Use the list directly if it's already a list
    else:
        print("Unsupported maze format")
        return
    
    maze_height = len(maze_lines)
    maze_width = len(maze_lines[0]) if maze_lines else 0

    # Assuming tile_size is a constant defined elsewhere
    tile_size = 20  # Size of the square tile

    # Calculate window dimensions to make the maze ?% of the window
    window_width = maze_width * tile_size * 1.5
    window_height = maze_height * tile_size * 1.5

    # canvas = tk.Canvas(root, width=window_width, height=window_height)
    # canvas.pack()

    # Calculate starting x and y to center the maze
    start_x = (window_width - maze_width * tile_size) // 2
    start_y = (window_height - maze_height * tile_size) // 2


    for y, row in enumerate(maze_lines):
        for x, char in enumerate(row):
            if char == 'X':
                color = 'grey'
            elif char == '.':
                color = 'white'
            elif char == 's':
                color = 'green2'
            elif char == 'e':
                color = 'cyan'
            elif char == '-':
                color = 'yellow'
            elif char == ',':
                color = 'brown1'
                canvas.create_oval(start_x + x*tile_size, start_y + y*tile_size, start_x + (x+1)*tile_size, start_y + (y+1)*tile_size, fill=color)
            else:
                continue  # Skip unknown characters
            canvas.create_rectangle(start_x + x*tile_size, start_y + y*tile_size, start_x + (x+1)*tile_size, start_y + (y+1)*tile_size, fill=color, outline="black")
            if char in ('s', 'e'):  # Add text for start and end
                text_x = start_x + (x+0.5)*tile_size
                text_y = start_y + (y+0.5)*tile_size
                canvas.create_text(text_x, text_y, text=char, font=("Arial", "16", "bold"))
                # Calculate coordinates for the circle around the text
                circle_margin = 4.5  # Adjust the size of the circle by changing the margin
                top_left_x = text_x - tile_size/4 - circle_margin
                top_left_y = text_y - tile_size/4 - circle_margin
                bottom_right_x = text_x + tile_size/4 + circle_margin
                bottom_right_y = text_y + tile_size/4 + circle_margin

                # Set different colors and thickness for the circles
                if char == 's':
                    circle_color = 'green4'  # Color for the circle around 's'
                    circle_thickness = 3  # Thickness for the circle around 's'
                elif char == 'e':
                    circle_color = 'blue2'  # Color for the circle around 'e'
                    circle_thickness = 3  # Thickness for the circle around 'e'

                # Draw the circle with specified color and thickness
                canvas.create_oval(top_left_x, top_left_y, bottom_right_x, bottom_right_y, outline=circle_color, width=circle_thickness)

    
def solve_maze(maze, canvas):
    solved_maze = left_hand.solve_maze(maze)
    canvas.delete("all")
    draw_maze(solved_maze, canvas)

def string_to_maze(maze_str):
    return [list(row) for row in maze_str.split('\n') if row]
    
    
def main():
    root = tk.Tk()
    root.title("Maze Solver Visualization")

    canvas = Canvas(root, width=2000, height=700)
    canvas.pack(fill=tk.X)

    # Generate and display the initial maze
    width = random.randint(10, 50)
    height = random.randint(10, 30)
    maze_rand = Maze_Generator().remove_random_walls()
    Maze_Generator().write_maze_to_file(maze_rand, 'maze.txt')
    maze_str = read_file_from_argument()
    draw_maze(maze_str, canvas)
    print("Initial maze:")
    print(maze_str)
    # Button to start solving
    maze = string_to_maze(maze_str)
    solve_button = tk.Button(root, text="Solve Maze",command=lambda: solve_maze(maze, canvas))
    solve_button.pack(side=tk.TOP, padx=10, pady=10)
    
    root.mainloop()
        
        
# Generate and print a maze
width = random.randint(10, 50)
height = random.randint(10, 40)


if __name__ == "__main__":
    main()