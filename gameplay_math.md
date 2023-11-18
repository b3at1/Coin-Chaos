# Gameplay Math
### Scoring
score is derived from coins and survival time
each coin has a constant value of 100 points
each second you survive is worth 10 points (aka 1 point every 0.1 seconds)
### Difficulty
enemy.forward() value starts at 1 (this very, very slow)
forward value increased by 1 every 10 seconds.
 - more precisely, it is 1 + (truncated seconds)*0.2