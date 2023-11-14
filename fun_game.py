# Title??
from turtle import *


######################## PLAYER MOVEMENT ########################

turt = Turtle()
turt.speed('fastest')
turt.penup()

def up():
    turt.seth(90) # set turtle direction to north
    turt.forward(20)

def down():
    turt.seth(270) # set turtle direction to south
    turt.forward(20)
def right():
    turt.seth(0) # set turtle direction to east
    turt.forward(20)
def left():
    turt.seth(180) # set turtle direction to west
    turt.forward(20)
def checkbounds():
    # by default, screen is 960x960.
    # coords go from (-480,-480) to (480, 480)
    width = wn.window_width()/2
    height = wn.window_height()/2
    if turt.xcor() >= width - 20:
        turt.setx(width - 20)
    if turt.ycor() >= height - 20:
        turt.sety(height - 20)
    
    if turt.xcor() <= -1 * width + 20:
        turt.setx( -1 * width + 20)    
    if turt.ycor() <= -1 * height + 20:
        turt.sety(-1 * height + 20)
    wn.ontimer(checkbounds, 20)
getscreen()
wn = Screen()
wn.listen()
checkbounds()
wn.onkeypress(up, key="w")
wn.onkeypress(left, key="a")
wn.onkeypress(down, key="s")
wn.onkeypress(right, key="d")





wn.exitonclick()