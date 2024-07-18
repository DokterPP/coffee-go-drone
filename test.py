import turtle
import sys
from maze.tile import tile
from generate_maze import Maze_Generator
# Define constants
TILE_SIZE = 20
MAZE_FILE = 'maze.txt'

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
        
def move_turtle_to_start(position):
    x, y = position
    turtle.goto(x, y)
    turtle.pendown()                
        
def draw_maze(maze):
    turtle.speed(0)
    turtle.penup()
    turtle.tracer(0, 0)

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
                tile().draw_tile(screen_x, screen_y, 'grey', TILE_SIZE)
            elif char == '.':
                tile().draw_tile(screen_x, screen_y, 'white', TILE_SIZE)
            elif char == 's':
                tile().draw_tile(screen_x, screen_y, 'lime', TILE_SIZE, 's', 'lime green')
                start_position = (screen_x + TILE_SIZE / 2, screen_y - TILE_SIZE / 2)
            elif char == 'e':
                tile().draw_tile(screen_x, screen_y, 'cyan', TILE_SIZE, 'e', 'royal blue')
            elif char == '-':
                tile().draw_tile(screen_x, screen_y, 'yellow', TILE_SIZE)
            elif char == ',':
                tile().draw_tile(screen_x, screen_y, 'red', TILE_SIZE)
    turtle.hideturtle()            
    turtle.update()  # Update the screen once all the tiles are drawn
    

    move_turtle_to_start(start_position)



def main():
    maze_str = read_file_from_argument()
    maze_rand = Maze_Generator().remove_random_walls()
    Maze_Generator().write_maze_to_file(maze_rand, 'maze.txt')
    maze_str = read_file_from_argument()
    draw_maze(maze_str)

    turtle.done()

if __name__ == "__main__":
    main()
