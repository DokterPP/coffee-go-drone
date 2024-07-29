import turtle

class Tile:
    def __init__(self, turtle_instance):
        self.turtle = turtle_instance

    def draw_tile(self, x, y, color, size, text=None, special_color=None):
        self.turtle.penup()
        self.turtle.goto(x, y)
        self.turtle.pendown()
        self.turtle.fillcolor(color)
        self.turtle.begin_fill()
        for _ in range(4):
            self.turtle.forward(size)
            self.turtle.right(90)
        self.turtle.end_fill()
        self.turtle.penup()

        if text:
            self.turtle.goto(x + size / 1.9, y - size + 3)
            self.turtle.write(text, align="center", font=("Arial", 10, "bold"))
            self.turtle.goto(x + size / 2, y - size + 2)
            self.turtle.pendown()
            self.turtle.pencolor(special_color)
            self.turtle.pen(pensize=3)
            self.turtle.circle(size / 2.5)
            self.turtle.pencolor('black')
            self.turtle.pen(pensize=1)
            self.turtle.penup()
