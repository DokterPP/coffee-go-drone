
class Move_Turtle:
    def __init__(self):
        pass
        
    def move_turtle_to_start(self, t, position):
        if position:
            
            x, y = position
            t.penup()
            t.goto(x, y)
            t.pendown()
            t.setheading(0)
            t.fillcolor('red')  # Set turtle fill color
            
    def move_up(self, t, TILE_SIZE):
        t.penup()
        t.setheading(90)
        t.forward(TILE_SIZE)
        t.pendown()
        
    def move_down(self, t, TILE_SIZE):
        t.penup()
        t.setheading(270)
        t.forward(TILE_SIZE)
        t.pendown()

    def move_left(self, t, TILE_SIZE):
        t.penup()
        t.setheading(180)
        t.forward(TILE_SIZE)
        t.pendown()

    def move_right(self, t, TILE_SIZE):
        t.penup()
        t.setheading(0)
        t.forward(TILE_SIZE)
        t.pendown()
        
    def is_move_valid(self, start_x, start_y, x , y ,maze, TILE_SIZE):

        maze = [list(row) for row in maze.split('\n') if row]

        grid_x = int((x - start_x) // TILE_SIZE)  # Convert x to grid index
        grid_y = int((start_y - y) // TILE_SIZE)  # Convert y to grid index

        # Print dimensions for debugging

        # Check if the grid indices are within bounds
        if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
            return False

        # Check if the cell is a wall
        if maze[grid_y][grid_x] == "X":  # Use grid_y for rows, grid_x for columns
            return False

        return True