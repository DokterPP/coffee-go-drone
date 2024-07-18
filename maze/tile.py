import turtle


class tile():

    def draw_tile(self, x, y, color, size, text=None, special_color=None):
        turtle.goto(x, y)
        turtle.pendown()
        turtle.fillcolor(color)
        turtle.begin_fill()
        for _ in range(4):
            turtle.forward(size)
            turtle.right(90)
        turtle.end_fill()
        turtle.penup()

        if text:
            turtle.goto(x + size /1.9 , y - size+3)
            turtle.write(text, align="center", font=("Arial", 10, "bold"))
            turtle.goto(x + size / 2, y - size+2)
            turtle.pendown()
            turtle.pencolor(special_color)
            turtle.pen(pensize=3)
            turtle.circle(size / 2.5)
            turtle.pencolor('black')
            turtle.pen(pensize=1)
            turtle.penup()
