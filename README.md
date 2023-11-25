# Coin Chaos
### A small python game made for ENGR-102

Coin Chaos is a game about collecting coins, and dodging energy balls.
If you come into contact with a ball, you lose!
The controls are simple: Use the mouse to left click on options in the menus.
In the game: use the W, A, S, and D keys to move.
W moves up, A moves left, S moves down, and D moves right.
You can also hold the keys!
![](https://github.com/b3at1/Coin-Chaos/main/player.gif)
Each coin will increases your score by 100 points.
Each second you survive will grant you 10 additional points.
As time goes on, more and more balls spawn, going faster and faster!
See if you can beat our high scores!
Sam:   4169
Belle:  3828
Claire: 3514

## Running the program:
You can execute the program using the command 'python fun_game.py'
The program has been tested in Python 3.9, and may not work in other versions.
The program supports Windows, Mac, and Linux operating systems, but you may encounter performance issues on Mac and Linux systems.
Please make sure to install the following dependencies before running the program:
- Python 3.9
- turtle (and tkinter, if you get "No module named '_tkinter'")
- time (Python standard library)
- random (Python standard library)

## How the code works:
The functions are separated into a few categories:
GAME STATE LOGIC, TIME LOGIC, ENEMY LOGIC, COIN LOGIC, SCORING LOGIC, and PLAYER LOGIC.
Going in depth on how each of these works would take a very long time, but generally the game state dictates what is currently be drawn and how the user is able to interact with the game. Enemy/Coin/Scoring/Player logic is all used as a part of the main game to define the game world, and how the player can interact with it. Time logic is used to keep track of timings, events, and durations.