# Title??
from turtle import *
import time
import random

FONT = ("Arial", 18, "normal")
wn = Screen()
wn.bgpic('dungeon.gif')
wn.bgcolor('black')
wn.colormode(255)
wn.listen()
wn.register_shape('coin32.gif')
wn.register_shape('ball.gif')
wn.register_shape('player.gif')
# 960x810
width = wn.window_width()/2
height = wn.window_height()/2
player_defeat = False

enemy_list = []
enemy_count = 0
enemy_max = 10 # keep max enemys to 5, for now
enemy_width = 3
enemy_length = 3
enemy_outline = enemy_width // 2

coin_collected = 0 # number of coins that player has collected
coin_list = []
coin_count = 0
coin_max = 5
# DO NOT CHANGE COIN DIMENSIONS, it goes wonky
coin_width = 1.4
coin_length = 1.4
coin_outline = coin_width // 1

score = 0
score_shown = Turtle()
score_shown.penup()
score_shown.hideturtle()
score_shown.goto(width - 200, height - 50)
score_shown.pencolor('white')
start = time.time()
time_elapsed = 0.0

turt = Turtle()
turt.speed('fastest')
turt.penup()
turt.resizemode("user")
turt.shapesize(coin_width, coin_length, coin_outline)
turt.shape("player.gif") 

######################## GAME STATE LOGIC ########################
def game_over():
    global player_defeat, score
    if player_defeat:
        wn.reset()
        final_score = Turtle(visible='False')
        final_score.penup()
        final_score.pencolor('white')
        final_score.goto(-60, 50)
        final_score.write(f"GAME OVER!", font=FONT)
        final_score.goto(-60, 0)
        final_score.write(f"Score: {score:>10}", font=FONT)
        play_btn = create_button(130, 90, "Play Again")
        play_btn.onclick(register_click)

def create_button(x: int, y: int, text: str) -> Screen:
    # this method is used to create and return button turtles that can be pressed
    button = Screen()
    penup()
    goto(x, y)
    color('white')
    write(f"{text}", font=FONT)
    return button

def register_click(x: int, y: int):
    # returns click coordinates
    print(x,  y)
    return (x, y)

######################## TIME LOGIC ########################
def calc_time(start: float):
    global time_elapsed
    time_elapsed = time.time() - start 
    wn.ontimer(lambda: calc_time(start), 100)

######################## ENEMY LOGIC ########################
# TODO: difficulty increase, 'kill' enemies, fix enemy bounce angle?


def move_enemy(enemy: Turtle):
    global time_elapsed, player_defeat
    if player_defeat:
        return
    tracer(False)  # we update everything together for performance reasons
    enemy.speed(4)
    enemy.forward(1 + (int(time_elapsed)*0.2)) # move forward 1 + (1 unit for every 5 seconds)
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
    global player_defeat
    x_player = turt.xcor()
    y_player = turt.ycor()
    for enemy in enemy_list:
        x_enemy = enemy.xcor()
        y_enemy = enemy.ycor()
        if abs(x_enemy - x_player) < 8 * enemy_width and abs(y_enemy - y_player) < 8 * enemy_length: # tolerance for collision, 8 seems to work NO IDEA WHY
            # GAME OVER STATE HERE
            player_defeat = True # player has been defeated
            game_over()
            return
            
    wn.ontimer(lambda: check_collision_enemy(enemy_list), 16)

def spawn_enemy(enemy_count, enemy_max):
    global player_defeat
    if player_defeat:
        return
    if enemy_count < enemy_max:
        enemy_count += 1
        enemy = Turtle(visible=False)
        enemy.resizemode("user")
        enemy.shapesize(enemy_width, enemy_length, enemy_outline)
        enemy.shape("ball.gif")
        enemy_list.append(enemy) # add enemy to enemy list
        enemy.speed('fastest')
        enemy.penup()
        enemy.setheading(random.randint(0,359))
        enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
        while check_collision_onSpawn(enemy): # make sure the enemy cannot spawn inside of the player
            enemy.goto(random.randint(-1 * width + 20, width - 20), random.randint(-1 * height + 20, height - 20))
        move_enemy(enemy)
    wn.ontimer(lambda: spawn_enemy(enemy_count, enemy_max), 5000)
    # use current time to speed up the spawning of enemy?

######################## COIN LOGIC ########################
def spawn_coin(coin_max):
    global coin_count
    if coin_count < coin_max:
        coin_count += 1
        coin = Turtle(visible=False)
        coin.resizemode("user")
        coin.shapesize(coin_width, coin_length, coin_outline) 
        coin.shape("coin32.gif")
        coin.color(255,200,150)
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

######################## SCORING LOGIC ########################

def calc_score(score_shown: Turtle):
    global time_elapsed, score, player_defeat
    if player_defeat:
        return
    # 10 points per second, 100 per coin
    score = int(time_elapsed // 0.1) + (coin_collected * 100)
    draw_score(score_shown)
    wn.ontimer(lambda: calc_score(score_shown), 100)

def draw_score(score_shown: Turtle):
    global score
    score_shown.clear()
    score_shown.write(f"Score: {score:>10}", font=FONT) # left pad it to look nicer

######################## PLAYER LOGIC ########################

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


def start_game():
    # initiate scoring
    calc_time(start)
    calc_score(score_shown)

    # check for game_over():
    game_over()

    # initiate collision check
    checkbounds_player() 

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

start_game()
wn.exitonclick()