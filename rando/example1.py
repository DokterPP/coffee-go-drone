#*****************************************************
# EXAMPLE 1:  Setting up a python turtle program
#             with timer and key handling.
#
#   You may run this from Anaconda command prompt as:
#
#       python example.py
#
#   Press the 'r','g' and 'b' keys to change colors
#
#*****************************************************
 
import turtle
 
#----------------------------------------------------
# Classes (currently we have only one class here!)
#----------------------------------------------------

class Square:

    def __init__(self, x,y,color,pen):
        self.x = x
        self.y = y
        self.color = color 
        self.pen = pen
        self.DIM = 100 # size
        self.needsTitleBarUpdate= True
        self.needsRedraw= True 

    def draw(self): 
        self.pen.color('black',self.color)   
        self.pen.begin_fill()
        self.pen.pensize(2)
        self.pen.up()
        self.pen.goto(self.x,self.y)   
        self.pen.down()
        for i in range(4): 
            self.pen.forward(self.DIM)
            self.pen.right(90) 
        self.pen.end_fill()

        # To tell timer the redraw is done
        square.needsRedraw= False

#----------------------------------------------------
# Functions
#----------------------------------------------------
def updateTitleBar(square):  
    # To update the title bar text
    text = "Press the 'r','g' and 'b' keys to change colors => "  + square.color
    turtle.title(text) 
    square.needsTitleBarUpdate= False 

def handleTimer(): 
    if square.needsTitleBarUpdate:  
        updateTitleBar(square)   
    if square.needsRedraw:
        square.draw() 
    scr.ontimer(handleTimer,10)   

def setColor(square,col):
    square.color = col
    square.needsTitleBarUpdate= True
    square.needsRedraw= True 

#----------------------------------------------------
# Main program
#---------------------------------------------------- 

# Configure the screen and pen
pen = turtle.Turtle() # is like a pen
scr = turtle.Screen() # is like a canvas
pen.speed( 'fastest') # from 'fastest' to 'slowest'
pen.hideturtle()   

# Our one and only Square
square =  Square(0,0,'Green',pen) 

# Window dimensions (we go for fullscreen window)
scr.setup(width=1.0, height=1.0) 
 
# Draw your things here 
pen.color('black','white') 
pen.showturtle()  
square.draw()

# Define key press handling functions
scr.onkey(lambda: setColor(square,'Red'), 'r')
scr.onkey(lambda: setColor(square,'Green'), 'g')
scr.onkey(lambda: setColor(square,'Blue'), 'b')  
 
# Start the timer & main loop
handleTimer()  
scr.listen() 
scr.mainloop()
 


 