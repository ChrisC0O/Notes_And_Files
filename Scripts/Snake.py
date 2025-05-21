import os
import random

GRID_HEIGHT, GRID_WIDTH = 20, 20
START_PLACEMENT_CORD = [GRID_HEIGHT // 2, GRID_WIDTH // 2]

BLACK_PIXEL = " "
WHITE_PIXEL = " "
PLAYER_PIXEL = "$"
FOOD_PIXEL = "*"

GAME_JUST_STARTED = True

game_map = []
move_dir = ""
player_pos = []
food_pos = []
amount_of_food_allowed = 1
player_score = 0
player_tale = []
player_tale_len = 1


def create_map():
    global game_map
    global player_pos

    game_map = []
    for h in range(GRID_HEIGHT):
        line = []
        for w in range(GRID_WIDTH):
            line.append(BLACK_PIXEL)  # Initialize with BLACK_PIXEL
        game_map.append(line)

    # Place player at starting position
    game_map[START_PLACEMENT_CORD[0]][START_PLACEMENT_CORD[1]] = PLAYER_PIXEL
    player_pos = [START_PLACEMENT_CORD[0], START_PLACEMENT_CORD[1]]

    return game_map


def screen_draw(matrix):
    for h in matrix:
        line = ""
        for pixel in h:
            line += pixel
        print(line)
    print(f"\n SCORE: {player_score}")


def move_player_pos_and_pixel(h, w, pixel_color):
    global game_map
    global player_pos

    # Clear current player position
    game_map[player_pos[0]][player_pos[1]] = BLACK_PIXEL
    # Update new position
    game_map[h][w] = pixel_color
    # Update player position
    player_pos = [h, w]


def change_one_pixel(h, w, pixel_color):
    global game_map
    game_map[h][w] = pixel_color


def place_food():
    global food_pos
    while True:
        h = random.choice(range(0, GRID_HEIGHT))
        w = random.choice(range(0, GRID_WIDTH))

        if [h, w] == player_pos:
            continue

        if [h, w] not in food_pos and [h, w] not in player_tale:
            food_pos.append([h, w])
            break


def display_module(move_dir):
    global GAME_JUST_STARTED
    global game_map
    global player_pos
    global player_score
    global player_tale_len

    if GAME_JUST_STARTED:
        game_map = create_map()
        screen_draw(game_map)
        GAME_JUST_STARTED = False
        return

    # Handle movement
    if move_dir.upper() == "W" and player_pos[0] - 1 >= 0:
        if [player_pos[0] - 1, player_pos[1]] == player_pos:
            print("GAME OVER")
            exit()
        move_player_pos_and_pixel(player_pos[0] - 1, player_pos[1], PLAYER_PIXEL)

    elif move_dir.upper() == "S" and player_pos[0] + 1 < GRID_HEIGHT:
        if [player_pos[0] + 1, player_pos[1]] == player_pos:
            print("GAME OVER")
            exit()
        move_player_pos_and_pixel(player_pos[0] + 1, player_pos[1], PLAYER_PIXEL)

    elif move_dir.upper() == "D" and player_pos[1] + 1 < GRID_WIDTH:
        if [player_pos[0], player_pos[1] + 1] == player_pos:
            print("GAME OVER")
            exit()
        move_player_pos_and_pixel(player_pos[0], player_pos[1] + 1, PLAYER_PIXEL)

    elif move_dir.upper() == "A" and player_pos[1] - 1 >= 0:
        if [player_pos[0], player_pos[1] - 1] == player_pos:
            print("GAME OVER")
            exit()
        move_player_pos_and_pixel(player_pos[0], player_pos[1] - 1, PLAYER_PIXEL)

    if player_pos in food_pos:
        player_score += 1
        food_pos.remove(player_pos)
        player_tale_len += 1

    if len(food_pos) < amount_of_food_allowed:
        place_food()

    for h, w in food_pos:
        change_one_pixel(h, w, FOOD_PIXEL)

    for h, w in player_tale:
        change_one_pixel(h, w, PLAYER_PIXEL)

    player_tale.insert(0, player_pos)

    if len(player_tale) > player_tale_len:
        change_one_pixel(player_tale[-1][0], player_tale[-1][1], BLACK_PIXEL)
        player_tale.pop(-1)

    print(player_tale)
    screen_draw(game_map)


def run_game():
    global move_dir

    while True:
        if move_dir == "":
            display_module(move_dir)

        move_dir = input("MOVE->")
        os.system("cls" if os.name == "nt" else "clear")  # Clear screen (Windows or Unix)
        display_module(move_dir)


if __name__ == "__main__":
    run_game()
