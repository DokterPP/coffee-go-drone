import turtle


# Define the maze
maze = [
    "XXXXXXXXXXXX",
    "X...X..X..eX",
    "X.X....X.XXX",
    "X..X.X.X.X.X",
    "XX.XXX.X...X",
    "X........X.X",
    "XsXX...X....",
    "XXXXXXXXXXXX"
]

# Define the cell size for turtle graphics
CELL_SIZE = 20

# Find the starting point (s)
start_x, start_y = None, None
for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 's':
            start_x, start_y = x, y
            break
    if start_x is not None:
        break

# Ensure the start point is found
if start_x is None or start_y is None:
    raise ValueError("Start point 's' not found in the maze.")

# Initialize turtle
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Maze Navigation")

pen = turtle.Turtle()
pen.penup()
pen.speed(0)
pen.hideturtle()

# Draw the maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            screen_x = x * CELL_SIZE - 200
            screen_y = 200 - y * CELL_SIZE
            if cell == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("square")
                pen.fillcolor("black")
                pen.stamp()
            elif cell == "e":
                pen.goto(screen_x, screen_y)
                pen.shape("circle")
                pen.fillcolor("green")
                pen.stamp()

draw_maze()

# Create the turtle for navigation
player = turtle.Turtle()
player.shape("turtle")
player.color("blue")
player.penup()
player.goto(start_x * CELL_SIZE - 200, 200 - start_y * CELL_SIZE)

# Movement functions
def move_up():
    new_x, new_y = player.xcor(), player.ycor() + CELL_SIZE
    if is_move_valid(new_x, new_y):
        player.goto(new_x, new_y)

def move_down():
    new_x, new_y = player.xcor(), player.ycor() - CELL_SIZE
    if is_move_valid(new_x, new_y):
        player.goto(new_x, new_y)

def move_left():
    new_x, new_y = player.xcor() - CELL_SIZE, player.ycor()
    if is_move_valid(new_x, new_y):
        player.goto(new_x, new_y)

def move_right():
    new_x, new_y = player.xcor() + CELL_SIZE, player.ycor()
    if is_move_valid(new_x, new_y):
        player.goto(new_x, new_y)

# Check if the move is valid
def is_move_valid(x, y):
    # Convert turtle coordinates to maze grid indices
    grid_x = int((x + 200) // CELL_SIZE)
    grid_y = int((200 - y) // CELL_SIZE)
    
    if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
        return False
    if maze[grid_y][grid_x] == "X":
        return False
    return True

# Keyboard bindings
screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")

# Start the main loop
turtle.done()
