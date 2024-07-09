import sys
import os
import tkinter as tk

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

def draw_maze(maze):
    root = tk.Tk()
    root.title("Maze")

    maze_lines = maze.splitlines()
    maze_height = len(maze_lines)
    maze_width = len(maze_lines[0]) if maze_lines else 0

    # Assuming tile_size is a constant defined elsewhere
    tile_size = 20  # Size of the square tile

    # Calculate window dimensions to make the maze 50% of the window
    window_width = maze_width * tile_size * 1.5
    window_height = maze_height * tile_size * 1.5

    canvas = tk.Canvas(root, width=window_width, height=window_height)
    canvas.pack()

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
    root.mainloop()

if __name__ == "__main__":
    maze_content = read_file_from_argument()
    if maze_content:
        draw_maze(maze_content)