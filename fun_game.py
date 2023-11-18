# Title??
from turtle import *
import time
import random
# TODO: ART BACKGROUND, LOCK WINDOW SIZE, ENEMY SKIN
wn = Screen()
# 960x810
width = wn.window_width()/2
height = wn.window_height()/2
wn.register_shape('coin32.gif')
######################## ENEMY LOGIC ########################

# TODO: difficulty increase, 'kill' enemies, fix enemy bounce angle?
start = time.time()
end = start
start = start - end
#print(start)
enemy_list = []
enemy_count = 0
enemy_max = 10 # keep max enemys to 5, for now
enemy_width = 3
enemy_length = 3
enemy_outline = enemy_width // 2

def move_enemy(enemy: Turtle):
    tracer(False)  # we update everything together for performance reasons
    enemy.speed(4)
    enemy.forward(8)
    enemy.showturtle()
    checkbounds_enemy(enemy)
    update()
    wn.ontimer(lambda: move_enemy(enemy), 16) # kinda breaks code on exit but its fine.

def checkbounds_enemy(enemy: Turtle):
    if enemy.xcor() >= width - 20 or enemy.ycor() >= height - 20 or enemy.xcor() <= -1 * width + 20 or enemy.ycor() <= -1 * height + 20:
        angle_modifier = random.randint(0,15)
        enemy.setheading((120 + angle_modifier + enemy.heading()) % 360) # bounce off a wall
        enemy.forward(20) # "boost" enemy away from wall

# check collision can take either a list or a single turtle, and returns whether a collision occurred
def check_collision_onSpawn(enemy: Turtle):
    x_player = turt.xcor()
    y_player = turt.ycor()
    x_enemy = enemy.xcor()
    y_enemy = enemy.ycor()
    if abs(x_enemy - x_player) < 32 * enemy_width and abs(y_enemy - y_player) < 32 * enemy_length: # larger tolerance on spawn so enemy doesn't obliterate player
            return True # returns true if collision occurred
    return False

def check_collision_enemy(enemy_list: list):
    x_player = turt.xcor()
    y_player = turt.ycor()
    for enemy in enemy_list:
        x_enemy = enemy.xcor()
        y_enemy = enemy.ycor()
        if abs(x_enemy - x_player) < 8 * enemy_width and abs(y_enemy - y_player) < 8 * enemy_length: # tolerance for collision, 8 seems to work NO IDEA WHY
            enemy.color("yellow") # for now, I just set color of enemy to yellow to "tag" a collision
            # GAME OVER STATE HERE
    wn.ontimer(lambda: check_collision_enemy(enemy_list), 16)

def spawn_enemy(enemy_count, enemy_max):
    if enemy_count < enemy_max:
        enemy_count += 1
        enemy = Turtle(visible=False)
        enemy.resizemode("user")
        enemy.shapesize(enemy_width, enemy_length, enemy_outline)
        enemy.shape("circle")
        enemy_list.append(enemy) # add enemy to enemy list
        enemy.speed('fastest')
        enemy.penup()
        enemy.setheading(random.randint(0,359))
        enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
        while check_collision_onSpawn(enemy): # make sure the enemy cannot spawn inside of the player
            enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
        move_enemy(enemy)
    wn.ontimer(lambda: spawn_enemy(enemy_count, enemy_max), 1000)
        #print(1000 - int(time.time() - start))
        #wn.ontimer(spawn_enemy, 1000 - 2 * int(time.time() - start)) # use current time to speed up the spawning of enemy?

######################## COIN LOGIC ########################
coin_collected = 0 # number of coins that player has collected
coin_list = []
coin_count = 0
coin_max = 10
# DO NOT CHANGE COIN DIMENSIONS, it goes wonky
coin_width = 1.4
coin_length = 1.4
coin_outline = coin_width // 1

def spawn_coin(coin_max):
    global coin_count
    if coin_count < coin_max:
        coin_count += 1
        coin = Turtle(visible=False)
        coin.resizemode("user")
        coin.shapesize(coin_width, coin_length, coin_outline) # change this later lol
        coin.shape("coin32.gif") # change this later lol
        coin.color(255,200,150) # change this later lol
        coin_list.append(coin) # add coin to coin list
        coin.penup()
        coin.goto(random.randint(-1 * width + 100, width - 100), random.randint(-1 * height + 100, height - 100))
        while check_collision_onSpawn(coin): # make sure the enemy cannot spawn inside of the player
            coin.goto(random.randint(-1 * width + 100, width - 100), random.randint(-1 * height + 100, height - 100))
        coin.showturtle()
    wn.ontimer(lambda: spawn_coin(coin_max), 1000)

def check_collision_coin(coin_list: list):
    global coin_collected, coin_count
    x_player = turt.xcor()
    y_player = turt.ycor()
    for coin in coin_list:
        x_coin = coin.xcor()
        y_coin = coin.ycor()
        if abs(x_coin - x_player) < 16 * coin_width and abs(y_coin - y_player) < 16 * coin_length: # 16 tolerance coeff, idk why
            coin_list.remove(coin)
            # use global to modify the variable
            coin_collected = coin_collected + 1
            coin_count -= 1
            coin.hideturtle()
            del coin # dunno what this does exactly, but hopefully it works
            #
    wn.ontimer(lambda: check_collision_coin(coin_list), 16)

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

def checkbounds_player():
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
    wn.ontimer(checkbounds_player, 20)


wn.bgcolor('red')
wn.colormode(255)
wn.listen()

checkbounds_player() # initiate collision check

# initiate turtle objects
spawn_enemy(enemy_count, enemy_max)
spawn_coin(coin_max)

# check collisions
check_collision_enemy(enemy_list)
check_collision_coin(coin_list)

# controls
wn.onkeypress(up, key="w")
wn.onkeypress(left, key="a")
wn.onkeypress(down, key="s")
wn.onkeypress(right, key="d")

wn.exitonclick()
