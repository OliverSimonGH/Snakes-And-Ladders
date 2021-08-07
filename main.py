import os
import sys
import turtle
import random

RUNNING = True
PLAYER_TURN = False
WIDTH = HEIGHT = 600
SQUARE_SIZE = WIDTH / 5
ANGLE = 90

stamp_id = {}

class Obstacles:
    SNAKE = 0
    LADDER = 1

rows = []
for i in range(5):
    if i % 2 == 0:
        for j in range(5):
            square_id = (j + 1) + (i * 5)
            square_x = (j * SQUARE_SIZE) - (WIDTH / 2)
            square_y = (i * SQUARE_SIZE) - (WIDTH / 2)

            rows.append([square_id, square_x, square_y])

    else: 
        for j in reversed(range(5)):
            square_id = (5 - j) + (i * 5)
            square_x = (j * SQUARE_SIZE) - (WIDTH / 2)
            square_y = (i * SQUARE_SIZE) - (WIDTH / 2)

            rows.append([square_id, square_x, square_y])

snakes_and_ladders = [
    [5, 15, Obstacles.LADDER, "ladder3.gif", 50],
    [9, 12, Obstacles.LADDER, "ladder2.gif", 0], 
    [18, 23, Obstacles.LADDER, "ladder.gif", 0], 
    [8, 3, Obstacles.SNAKE, "snake2.gif", 60], 
    [20, 1, Obstacles.SNAKE, "snake3.gif", -60],
    [24, 14, Obstacles.SNAKE, "snake.gif", 0]
]

#id,  img
players = [
    [0, 1, "bull.gif", "Big Bad Bull", 0],
    [1, 1, "cow.gif", "Fluffy Cow", 0]
]

def roll_dice(type):
    try:
        while True:
            new_dice_num = random.randint(1, 6)
            key_pressed = input(f"{type}: Press Enter to roll dice")
            if key_pressed == "":
                print(f"You rolled: {new_dice_num}")
                return new_dice_num
    except Exception:
        sys.exit(0)
       
def draw_square(x, y, index):
    board.penup()
    board.goto(x, y)
    board.pendown()

    for i in range(4):
        board.forward(SQUARE_SIZE)
        board.left(ANGLE)

    board.penup()
    board.goto(x + (SQUARE_SIZE * 0.05), y + (SQUARE_SIZE * 0.85))
    board.write(index)
    board.pendown()

    board.penup()
    board.goto(x + 10, y + 5)
    board.write(f"X: {x}, Y: {y}")
    board.pendown()

def draw_obstacle(x, y, name, type, size):
    board.hideturtle()
    board.penup()

    if type == Obstacles.SNAKE:
        board.goto(x + (SQUARE_SIZE / 2), y - (SQUARE_SIZE * 0.5) + size)
    else:
        board.goto(x + (SQUARE_SIZE / 2), y + SQUARE_SIZE + size)

    board.showturtle()
    board.pendown()

    board.shape(name)
    board.stamp()

def draw_player(player_id, square_id, img):
    if player_id in stamp_id:
        board.clearstamp(stamp_id[player_id])

    board.penup()
    board.hideturtle()

    for i in rows:
        if i[0] == square_id:
            if player_id == 0:
                board.goto(i[1] + (SQUARE_SIZE / 2), i[2] + (SQUARE_SIZE * 0.75))
            else: 
                board.goto(i[1] + (SQUARE_SIZE / 2), i[2] + (SQUARE_SIZE * 0.35))

    board.showturtle()
    board.pendown()

    board.shape(img)

    id = board.stamp()
    stamp_id[player_id] = id

def draw_highscores():
    eraser = turtle.Turtle()

    for x, i in enumerate(players):
        eraser.penup()
        eraser.goto(int((WIDTH / 2) - 80), int((WIDTH / 2) - (x * 15)) - 20)
        eraser.pencolor("red")
        eraser.write(f"{i[3]}: {i[4]}")
        eraser.pendown()

    return eraser

def calculate_position(current_num, dice_num):
    if current_num + dice_num == 25:
        # TODO game over, player has won
        return 25

    elif current_num + dice_num > 25:
        return 25 - ((current_num + dice_num) % 25)

    else:
        return current_num + dice_num

def check_if_obstacle(square_id):
    for i in snakes_and_ladders:
        if i[0] == square_id:
            return i[1]  

    return square_id 

board = turtle.Turtle()
board.speed(10)
board.color("black")

window = turtle.Screen()
window.setup(WIDTH, HEIGHT)
window.bgcolor("white")
window.tracer(False)

# Register Images
for i in range(len(snakes_and_ladders)):
    window.register_shape(snakes_and_ladders[i][3])

for i in range(len(players)):
    window.register_shape(players[i][2])

window.register_shape("win.gif")

# Draw Board
for i in range(len(rows)):
    draw_square(rows[i][1], rows[i][2], rows[i][0])

# Draw Snakes and Ladders
for i in range(len(snakes_and_ladders)):
    for j in range(len(rows)):
        if snakes_and_ladders[i][0] == rows[j][0]:
            draw_obstacle(rows[j][1], rows[j][2], snakes_and_ladders[i][3], snakes_and_ladders[i][2], snakes_and_ladders[i][4])

        
# Draw Players
for i in range(len(players)):
    draw_player(players[i][0], 1, players[i][2])

erasable_highscore = draw_highscores()
# window.update() 

print("New Game!\n")
while RUNNING:
    # Select Player Turn
    PLAYER_TURN = not int(PLAYER_TURN)
    selected_player = players[PLAYER_TURN]

    # Roll Dice
    dice_num = roll_dice(selected_player[3])
    current_square = selected_player[1]

    # Calculate Position
    new_pos = calculate_position(current_square, dice_num)

    # Check for an Obstacle
    obstacle_num = check_if_obstacle(new_pos)
    players[PLAYER_TURN][1] = obstacle_num
    print(f"You move from: {current_square} to {new_pos}\n")

    # Draw Player
    draw_player(PLAYER_TURN, obstacle_num, selected_player[2])

    # Win condition
    if obstacle_num == 25:
        print(f"{selected_player[3]} has won")
        selected_player[4] += 1
        
        board.penup()
        board.goto(0, 0)
        board.shape("win.gif")
        board.pendown()

        id = board.stamp()
        stamp_id["win"] = id

        RUNNING = False
            
        key_pressed = input(f"Press Enter to restart game")
        if key_pressed == "":
            RUNNING = True
            if "win" in stamp_id:
                board.clearstamp(stamp_id["win"])
                    
            os.system("cls")
            print("New Game!\n")

            # reset player positions
            for i in players:
                i[1] = 1
                draw_player(i[0], 1, i[2])

            erasable_highscore.clear()
            erasable_highscore = draw_highscores()
            
turtle.done()