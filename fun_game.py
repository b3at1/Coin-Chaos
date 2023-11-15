# Title??
from turtle import *
import time
import random

wn = Screen()
width = wn.window_width()/2
height = wn.window_height()/2

######################## ENEMY LOGIC ########################

# TODO: make spawn_enemy method
start = time.time()
end = start
print(start)
enemy_count = 0
enemy_max = 5 # keep max enemys to 5, for now
def move_enemy(enemy):
        enemy.pendown()
        enemy.showturtle()
        enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
        # CALL COLLISION LISTENER HERE
        wn.ontimer(lambda: move_enemy(enemy) , 100) # kinda breaks code on exit but its fine.

def spawn_enemy(enemy_count, enemy_max):
        if enemy_count < enemy_max:
            enemy_count += 1
            enemy = Turtle(visible=False)
            enemy.speed('fastest')
            enemy.penup()
            enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
            move_enemy(enemy)
        # CALL COLLISION LISTENER HERE
        wn.ontimer(lambda: spawn_enemy(enemy_count, enemy_max), 1000)
        #print(1000 - int(time.time() - start))
        #wn.ontimer(spawn_enemy, 1000 - 2 * int(time.time() - start)) # use current time to speed up the spawning of enemy?

######################## PLAYER LOGIC ########################

turt = Turtle()
turt.speed('fastest')
turt.penup()
turt.shape("turtle")
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
    if turt.xcor() >= width - 20:
        turt.setx(width - 20)
    if turt.ycor() >= height - 20:
        turt.sety(height - 20)
    
    if turt.xcor() <= -1 * width + 20:
        turt.setx( -1 * width + 20)    
    if turt.ycor() <= -1 * height + 20:
        turt.sety(-1 * height + 20)
    wn.ontimer(checkbounds, 20)

wn.bgcolor('red')
wn.listen()

checkbounds()
spawn_enemy(enemy_count, enemy_max)

wn.onkeypress(up, key="w")
wn.onkeypress(left, key="a")
wn.onkeypress(down, key="s")
wn.onkeypress(right, key="d")

wn.exitonclick()
