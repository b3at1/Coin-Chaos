# By submitting this assignment, I agree to the following:
# "Aggies do not lie, cheat, or steal, or tolerate those who do."
# "I have not given or received any unauthorized aid on this assignment."
#
# Names: Claire Wu
# Annabelle Erdberg
# Sam Bederman
# Section: 518
# Assignment: LAB 13.1
# Date: 25 November 2023
from turtle import *
from pathlib import Path
import time
import random
   
######################## GAME STATE LOGIC ########################
def game_over():
    global player_defeat, score, wn, gamestate
    # the wait_times() are necessary otherwise a race condition will occur
    if player_defeat:
        wn.clear()
        wn = Screen()
        # hardcoded to fix certain scaling issues
        wn.setup(960,810)
        wn.bgpic('dungeon_blank.gif')
        wn.bgcolor('black')
        wn.colormode(255)
        wn.listen()
        wn.register_shape('coin32.gif')
        wn.register_shape('ball.gif')
        wn.register_shape('player.gif')
        final_score = Turtle(visible=False)
        final_score.penup()
        final_score.pencolor('white')
        final_score.goto(-100, 50)
        final_score.write(f"GAME OVER!", font=FONT)
        final_score.goto(-100, 0)
        gamestate = "DEFEAT"
        # had to make my own function, since time.sleep() interrupts gameloop
        wait_time(2)
        final_score.write(f"Score: {score:>10}", font=FONT)
        wait_time(1)
        btn = create_button(-80, -50, 130, 30, "Play Again")
        btn = create_button(-80, -100, 130, 30, "Menu")
        btn = create_button(-80, -150, 130, 30, "Quit")
        btn.onclick(register_click)
        update()

def create_button(x: int, y: int, txt_width: int, txt_height: int, text: str) -> Screen:
    '''used to create and return button turtles that can be pressed'''
    button_box = Turtle(visible=False)
    button_box.penup()
    button_box.goto(x, y)
    button_box.color('white')
    button_box.write(f"{text}", font=FONT)
    button_box.goto(x - 10, y)
    tracer(False)
    
    # button boxxing
    button_box.pendown()
    button_box.color('white')
    button_box.pensize(2)
    for i in range(2):
        button_box.forward(txt_width)
        button_box.left(90)
        button_box.forward(txt_height)
        button_box.left(90)
    update()
    button = Screen()
    return button

def register_click(x: int, y: int):
    '''returns click coordinates, check if the button was pressed'''
    global gamestate
    if gamestate == "DEFEAT":
        if x >= -90 and x <= 40 and y >= -50 and y <= -20: # play game is clicked
            start_game()
        elif x >= -90 and x <= 40 and y >= -100 and y <= -70: # menu is clicked
            start_menu()
        elif x >= -90 and x <= 40 and y >= -150 and y <= -120: # quit is clicked
            wait_time(0.2)
            exit()
        else:
            pass # this satisfies having an if - elif - else
    elif gamestate == "MENU":
        if x >= -90 and x <= 40 and y >= -50 and y <= -20: # play game is clicked
            start_game()
        elif x >= -90 and x <= 40 and y >= -100 and y <= -70: # about is clicked
           start_about() # placeholders
        elif x >= -90 and x <= 40 and y >= -150 and y <= -120: # quit is clicked
            wait_time(0.4)
            exit()
        else:
            pass
    elif gamestate == "ABOUT":
        if x >= -90 and x <= 40 and y >= -350 and y <= -320: # back (menu) is clicked
            start_menu()
    return (x, y)

######################## TIME LOGIC ########################
def calc_time(start: float):
    '''calculate elapsed time'''
    global time_elapsed, player_defeat
    if player_defeat:
        return
    time_elapsed = time.time() - start 
    wn.ontimer(lambda: calc_time(start), 100)

def wait_time(amnt: float):
    '''wait in this function for a certain time amount (in seconds)'''
    # waits amnt seconds
    startT = time.time()
    i = amnt
    while i - startT < amnt:
        i = time.time()

######################## ENEMY LOGIC ########################
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
    global time_elapsed
    if player_defeat:
        return
    if enemy.xcor() >= width + 40 or  enemy.xcor() <= -1 * width - 40:
        enemy.setheading(180 - enemy.heading())
        enemy.forward(20) # "boost" enemy away from wall
    elif  enemy.ycor() >= height + 70 or enemy.ycor() <= -1 * height - 70:
        enemy.setheading(-enemy.heading())
        enemy.forward(20)

def check_collision_onSpawn(enemy: Turtle):
    '''check collision can take either a list or a single turtle, and returns whether a collision occurred'''
    global time_elapsed
    if player_defeat:
        return
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
        if abs(x_enemy - x_player) < 12 * enemy_width and abs(y_enemy - y_player) < 12 * enemy_length: # tolerance for collision, 8 seems to work NO IDEA WHY
            # GAME OVER STATE HERE
            player_defeat = True # player has been defeated
            wait_time(1) # these waits reduce chance of race condition
            game_over()
            return
    wn.ontimer(lambda: check_collision_enemy(enemy_list), 32)

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
    global coin_count, player_defeat
    if player_defeat:
        return
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
    global coin_collected, coin_count, player_defeat
    if player_defeat:
        return
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
    global time_elapsed
    if player_defeat:
        return
    turt.seth(90) # set turtle direction to north
    turt.forward(20)

def down():
    global time_elapsed
    if player_defeat:
        return 
    turt.seth(270) # set turtle direction to south
    turt.forward(20)
def right():
    global time_elapsed
    if player_defeat:
        return
    turt.seth(0) # set turtle direction to east
    turt.forward(20)
def left():
    global time_elapsed
    if player_defeat:
        return
    turt.seth(180) # set turtle direction to west
    turt.forward(20)

def checkbounds_player():
    global time_elapsed
    if player_defeat:
        return
    # by default, screen is 960x960.
    # coords go from (-480,-480) to (480, 480)
    if turt.xcor() >= width + 60:
        turt.setx(width + 60)
    if turt.ycor() >= height + 80:
        turt.sety(height + 80)
    
    if turt.xcor() <= -1 * width - 60:
        turt.setx( -1 * width - 60)    
    if turt.ycor() <= -1 * height - 80:
        turt.sety(-1 * height - 80)
    wn.ontimer(checkbounds_player, 20)

def start_menu():
    global FONT, wn, width, height, gamestate
    FONT = ("Arial", 18, "normal")
    wn = Screen()
    wn.clear()
    # hardcoded to fix certain scaling issues
    wn.setup(960,810)
    wn.bgpic('dungeon_title.gif')
    wn.bgcolor('black')
    wn.colormode(255)
    wn.listen()
    gamestate = "MENU"
    # 960x810 (default)
    width = wn.screensize()[0]
    height = wn.screensize()[1]
    btn = create_button(-80, -50, 130, 30, "Play")
    btn = create_button(-80, -100, 130, 30, "About")
    btn = create_button(-80, -150, 130, 30, "Quit")
    btn.onclick(register_click)
    update()
    wn.mainloop()
def start_game(): 
    # this is what happens when you dont make classes :(
    global FONT, wn, width, height, player_defeat, enemy_list, enemy_count, enemy_max, enemy_width, enemy_length, enemy_outline, coin_collected, coin_list, coin_count, coin_width, coin_length, coin_outline, score, score_shown, start, time_elapsed, turt, gamestate
    FONT = ("Arial", 18, "normal")
    wn = Screen()
    wn.clear()
    # hardcoded to fix certain scaling issues
    wn.setup(960,810)
    wn.bgpic('dungeon.gif')
    wn.bgcolor('black')
    wn.colormode(255)
    wn.listen()
    wn.register_shape('coin32.gif')
    wn.register_shape('ball.gif')
    wn.register_shape('player.gif')

    # 960x810 (default)
    width = wn.screensize()[0]
    height = wn.screensize()[1]

    # player is now undefeated
    player_defeat = False

    '''
    gamestate tracks what 'state' the game is in
    ''MENU' == main menu
    'PLAY' == playing game
    'DEFEAT' == gameover screen
    'ABOUT' == about screen
    'QUIT' == quit game (exits)
    '''
    # game is now being played
    gamestate = "PLAY"

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
    score_shown.goto(width - 150, height + 50)
    score_shown.pencolor('white')
    start = time.time()
    time_elapsed = 0.0

    turt = Turtle()
    turt.speed('fastest')
    turt.penup()
    turt.resizemode("user")
    turt.shapesize(coin_width, coin_length, coin_outline)
    turt.shape("player.gif") 

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

def start_about():
    global FONT, wn, width, height, gamestate
    FONT = ("Arial", 18, "normal")
    FONT_LG = ("Arial", 36, "normal")
    wn = Screen()
    wn.clear()
    # hardcoded to fix certain scaling issues
    wn.setup(960,810)
    wn.bgpic('dungeon_blank.gif')
    wn.bgcolor('black')
    wn.colormode(255)
    wn.listen()
    gamestate = "ABOUT"
    # 960x810 (default)
    width = wn.screensize()[0]
    height = wn.screensize()[1]
    final_score = Turtle(visible=False)
    final_score.penup()
    final_score.pencolor('white')
    final_score.goto(-100, 250)
    final_score.write(f"Instructions\n", font=FONT_LG)
    try:
        with open("instructions.txt", 'r') as instructions:
            final_score.goto(-400, 125)
            final_score.write(f"{instructions.read()}", font=FONT)
    except FileNotFoundError:
        print("Missing file: 'instructions.txt'")
    final_score.goto(-100, -125)
    final_score.write(f"Rules\n", font=FONT_LG)
    try:
        with open("rules.txt", 'r') as instructions:
            final_score.goto(-400, -275)
            final_score.write(f"{instructions.read()}", font=FONT)
    except FileNotFoundError:
        print("Missing file: 'rules.txt'")
    # only one button here to go back to the main menu "Back"
    btn = create_button(-80, -350, 130, 30, "Back")
    btn.onclick(register_click)
    update()
start_menu()