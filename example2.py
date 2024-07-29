#*****************************************************
# EXAMPLE 2:  Setting up a python turtle program
#             to draw (stamp) images fast!
#
#   You may run this from Anaconda command prompt as:
#
#       python example2.py
#
#   Press left mouse button to quit the application
#
#*****************************************************
 
import turtle
 
#----------------------------------------------------
# Classes (currently we have only one class here!)
#----------------------------------------------------

# Used to draw (stamp) an image 
class ImageTurtle(turtle.Turtle):              
    def __init__(self,imageFileName): 
        turtle.Turtle.__init__(self) 
        self.up()
        self.speed( 'fastest')  
        self.shape(imageFileName )
        self.hideturtle()
        
#----------------------------------------------------
# Functions
#----------------------------------------------------
def drawAxisSystem(tur): 
    tur.color('blue') 
    # Draw x-axis 
    tur.goto(0,0)
    tur.setheading(0) # RIGHT
    tur.forward(1000) 
    # Draw a y-axis
    tur.goto(0,0)
    tur.setheading(90) # UP
    tur.forward(1000)

#----------------------------------------------------
# Main program
#---------------------------------------------------- 

# Configure the screen and pen
pen = turtle.Turtle() # is like a pen
scr = turtle.Screen() # is like a canvas
pen.speed( 'fastest') # 'fastest' to 'slowest'
pen.hideturtle()   

# Set window dimensions (we go for fullscreen window)
scr.setup(width=1.0, height=1.0) 
 
# Register our Shape (so it can be used to stamp an image)
scr.register_shape("smiley.gif" ) 

# Our ImageTurtle
imageTurtle= ImageTurtle("smiley.gif")

# Draw your things here 
drawAxisSystem(pen) 

# Draw a bunch of smileys
GAP = 80 # Gap between smileys
noOfSmileys= 10
for i in range(noOfSmileys):
    imageTurtle.goto(i*GAP , 0)   
    imageTurtle.stamp()  
 
# When we click we will exit the application
scr.exitonclick()


 


 