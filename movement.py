
class Move_Turtle:
    def __init__(self):
        pass
        
    def move_turtle_to_start(self, t, position):
        if position:
            x, y = position
            t.penup()
            t.goto(x, y)
            t.pendown()
            t.fillcolor('red')  # Set turtle fill color
            
    def move_up(self, t, TILE_SIZE):
        t.setheading(90)
        t.forward(TILE_SIZE)
        
    def move_down(self, t, TILE_SIZE):
        t.setheading(270)
        t.forward(TILE_SIZE)

    def move_left(self, t, TILE_SIZE):
        t.setheading(180)
        t.forward(TILE_SIZE)

    def move_right(self, t, TILE_SIZE):
        t.setheading(0)
        t.forward(TILE_SIZE)