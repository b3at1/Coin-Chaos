# Title??
from turtle import *

def functionname(turt:Turtle):
    turt.forward(10)

turt = Turtle()
turt.forward(50)
turt.right(5)

def forward():
    turt.forward(20)
def backward():
    turt.back(20)
def right():
    turt.right(20)
def left():
    turt.left(20)

getscreen()
wn = Screen()
wn.listen()
wn.onkey(forward, key="w")
wn.onkey(backward, key="a")
wn.onkey(right, key="s")
wn.onkey(left, key="d")

wn.exitonclick()