import pygame
import os
import time
import math
import json
import random

# initialisieren von pygame
pygame.init()

# Spielkonfiguration
SCALING = 1.4
Loudnes = 0.2
WIDTH, HEIGHT = 560*SCALING, 600*SCALING
TILE_SIZE = 20*SCALING
COLORS = {
    "background": (0, 0, 20),
    "coin": (255, 244, 79),
    "pacman": (255, 255, 0),
    "geist1": (255, 0, 0),
    "geist2": (0, 255, 255)
}

# Initialisierung
def screen_draw(WIDTH, HEIGHT):
    HEIGHT += HEIGHT * .15
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    return screen

clock = pygame.time.Clock()

# Musik/Soundeffekte einrichten
def essen_sound():
    pygame.mixer.music.load('Musik/Pacman_Main_Theme.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(Loudnes)
    essen = pygame.mixer.Sound('Musik/Pacman_Eat.wav')
    return essen

# Bilder Einlesen
def Pacman_Ghost_Image_Load():
    STRETCH_FACTOR_PACMAN = 3
    STRETCH_FACTOR_PINKY = 2.0
    STRETCH_FACTOR_BLINKY = 1.65

    Pacman = ["", "", "", ""]
    Pacman[0] = pygame.transform.scale(pygame.image.load("Animationen/pacman01_03.png"), (TILE_SIZE * STRETCH_FACTOR_PACMAN, TILE_SIZE * STRETCH_FACTOR_PACMAN))
    Pacman[1] = pygame.transform.scale(pygame.image.load("Animationen/pacman02.png"), (TILE_SIZE * STRETCH_FACTOR_PACMAN, TILE_SIZE * STRETCH_FACTOR_PACMAN))
    Pacman[2] = pygame.transform.scale(pygame.image.load("Animationen/pacman01_03.png"), (TILE_SIZE * STRETCH_FACTOR_PACMAN, TILE_SIZE * STRETCH_FACTOR_PACMAN))
    Pacman[3] = pygame.transform.scale(pygame.image.load("Animationen/pacman04.png"), (TILE_SIZE * STRETCH_FACTOR_PACMAN, TILE_SIZE * STRETCH_FACTOR_PACMAN))
    Pinky =  pygame.transform.scale(pygame.image.load("Animationen/pinky.png"), (TILE_SIZE * STRETCH_FACTOR_PINKY , TILE_SIZE * STRETCH_FACTOR_PINKY))
    blinky = pygame.transform.scale(pygame.image.load("Animationen/blinky.png"), (TILE_SIZE * STRETCH_FACTOR_BLINKY , TILE_SIZE * STRETCH_FACTOR_BLINKY))
    return Pacman, Pinky, blinky

def map_einlesen():
    return pygame.transform.scale(pygame.image.load("Karte/Spielfeld.png"), (WIDTH, HEIGHT))

# Muenzen Zeichnen
def draw_grid(screen, level, tile_size, colors):
    # offest um münzen zu zentrieren von -8
    offset_y = -8
    rows, cols = len(level), len(level[0])
    for row in range(rows):
        for col in range(cols):
            x, y = col * tile_size, row * tile_size
            if level[row][col] == 2:
                pygame.draw.circle(screen, colors["coin"], (x + tile_size // 2, y + tile_size // 2 + offset_y), tile_size // 4)
            if level[row][col] == 3:
                pygame.draw.circle(screen, colors["coin"], (x + tile_size // 2, y + tile_size // 2 + offset_y), tile_size // 2)

#added updatet ganze funkion
def move_ghost(player_pos, ghost_direction, ghost_pos, level, chase_mode):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(level), len(level[0])
    possible_directions = []
    closest_direction = None
    min_distance = float('inf')

    # Aktuelle Richtung reversen
    reverse_direction = (-ghost_direction[0], -ghost_direction[1])

    for direction in directions:
        # Rückwärtsbewegung ausschließen
        if direction != reverse_direction:
            new_pos = [ghost_pos[0] + direction[0], ghost_pos[1] + direction[1]]
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] != 1:
                possible_directions.append(direction)

    if chase_mode and possible_directions:
    # Richtung die einen am nächsten an Pac-Man aktuell bringt
        for direction in possible_directions:
            new_pos = [ghost_pos[0] + direction[0], ghost_pos[1] + direction[1]]
            distance = math.dist(new_pos, player_pos)
            if distance < min_distance:
                min_distance = distance
                closest_direction = direction
        # Bewegung ausführen
        if closest_direction:
            ghost_pos[:] = [ghost_pos[0] + closest_direction[0], ghost_pos[1] + closest_direction[1]]
            ghost_direction[:] = closest_direction
    elif possible_directions:
        random_direction = random.choice(possible_directions)
        ghost_direction[:] = random_direction
        ghost_pos[:] = [ghost_pos[0] + random_direction[0], ghost_pos[1] + random_direction[1]]    
    else:
        #wenn sackgasse return(ausnahme)
        ghost_direction[:] = reverse_direction
        ghost_pos[:] = [ghost_pos[0] + reverse_direction[0], ghost_pos[1] + reverse_direction[1]]
    
def move_player(player_pos, direction, input_direction, level):
    rows, cols = len(level), len(level[0])
    new_pos = [player_pos[0] + input_direction[0], player_pos[1] + input_direction[1]]

    if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] != 1):
        player_pos[:] = new_pos
        direction[:] = input_direction
    else:
        # taking the old direction, because found a wall with the current
        new_pos = [player_pos[0] + direction[0], player_pos[1] + direction[1]]
        if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] != 1):
            player_pos[:] = new_pos

def update_game(player_pos, ghost1_pos, ghost2_pos, direction, ghost1_direction, ghost2_direction, input_direction, level, score, zeit, essen, chase_mode, wandering_count):
    move_player(player_pos, direction, input_direction, level)
    move_ghost(player_pos, ghost1_direction, ghost1_pos, level, chase_mode)
    move_ghost(player_pos, ghost2_direction, ghost2_pos, level, chase_mode)


    # added Teleportieren bei Tunnel 4
    if level[player_pos[0]][player_pos[1]] == 4:
        teleport_positions = []
        for row in range(len(level)):
            for col in range(len(level[row])):
                if level[row][col] == 4 and (row != player_pos[0] or col != player_pos[1]):
                    teleport_positions.append((row, col))
        
        if teleport_positions:
            # Zufällig eine neue Position wählen falls mehrer Tunnel
            new_pos = random.choice(teleport_positions)
            player_pos[:] = new_pos
            direction[:] = (-direction[0], -direction[1])

    #added
    if level[player_pos[0]][player_pos[1]] == 3:
        wandering_count = 0
        chase_mode = False
        ghost1_direction[:] =(-ghost1_direction[0], -ghost1_direction[1])
        ghost2_direction[:] =(-ghost2_direction[0], -ghost2_direction[1])

    if level[player_pos[0]][player_pos[1]] == 2 or level[player_pos[0]][player_pos[1]] == 3:
        level[player_pos[0]][player_pos[1]] = 0
        score += 10
        zeit_jetzt = time.time()
        if zeit_jetzt >= zeit + 0.717:
            pygame.mixer.Sound.play(essen)
            score += 1
            zeit = time.time()
    #added return
    return score, zeit, chase_mode, wandering_count

def rotate_Pacman(x, y, picture, direction, screen):
    Pacman_Orientation = 0
    if direction == [0, 1]:
        Pacman_Orientation = 0
    elif direction == [-1, 0]:
        Pacman_Orientation = 90
    elif direction == [0, -1]:
        Pacman_Orientation = 180
    elif direction == [1, 0]:
        Pacman_Orientation = 270
    # rotieren und in einem neuen "surface" speichern
    rotated = pygame.transform.rotate(picture, Pacman_Orientation)

    # Bestimmen der neuen Abmessungen (nach Rotation ändern sich diese!)
    size = rotated.get_rect()

    # Ausgabe
    screen.blit(rotated, (x - size.center[0], y - size.center[1]))

def read_level():
    with open('datei.json', 'r') as file:
        data = json.load(file)
    return data

def main():
    pygame.init()
    zeit = time.time()
    #added clock_ticks
    clock_ticks = 10
    # Screen definieren
    screen = screen_draw(WIDTH, HEIGHT)
    # Abspielen des Geistes
    Picture_Frame = 0
    # Verschieben des Geistbildes
    Pixel_movement_right = 10 * SCALING
    Pixel_movement_up = 0

    # Pacman und Geister einlesen
    pacman_idle, pinky, blinky = Pacman_Ghost_Image_Load()

    # Sounds einlesen
    essen = essen_sound()
    # Map
    map = map_einlesen()

    level = read_level()

    player_pos = [1, 1]
    ghost1_direction = [0, 0]
    ghost1_pos = [1, 1]
    ghost2_direction = [0, 0]
    ghost2_pos = [26, 1]
    direction = [0, 1]
    input_direction = [0, 0]
    score = 0
    #added frightened_mode
    chase_mode = True
    wandering_duration = 10 * clock_ticks
    wandering_count = 0
    #ghost start to wanderaround without a special coin collectet
    wandering_change_time = 15 * clock_ticks

    running = True
    while running:
        screen.fill(COLORS["background"])

        # Karte als Hintergrund Festlegen
        screen.blit(map, (0, 0))

        # Münzen Zeichnen
        draw_grid(screen, level, TILE_SIZE, COLORS)

        # Durch Pacman_Bilder Liste laufen
        Picture_Frame += 1
        if Picture_Frame > 3:
            Picture_Frame = 0

        # Pacman Orientierung
        rotate_Pacman(player_pos[1]*TILE_SIZE + Pixel_movement_right, player_pos[0]*TILE_SIZE - Pixel_movement_up, pacman_idle[Picture_Frame], direction, screen)

        #Geist 1 zeichnen
        blinky_image = blinky
        if ghost1_direction[1] > 0:  # Nach links
            blinky_image = pygame.transform.flip(blinky_image, True, False)
        screen.blit(blinky_image,
            (ghost1_pos[1] * TILE_SIZE - 4*SCALING, 
             ghost1_pos[0] * TILE_SIZE - 14*SCALING))
        #Geist 2 zeichnen
        pinky_image = pinky
        if ghost2_direction[1] < 0:  # Nach rechts
            pinky_image = pygame.transform.flip(pinky_image, True, False)
        screen.blit(pinky_image,
            (ghost2_pos[1] * TILE_SIZE - 8*SCALING, 
             ghost2_pos[0] * TILE_SIZE - 20*SCALING))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] | keys[pygame.K_w]:
            input_direction = [-1, 0]
        elif keys[pygame.K_DOWN] | keys[pygame.K_s]:
            input_direction = [1, 0]
        elif keys[pygame.K_LEFT] | keys[pygame.K_a]:
            input_direction = [0, -1]
        elif keys[pygame.K_RIGHT] | keys[pygame.K_d]:
            input_direction = [0, 1]

        #added chase_mode turn off and on
        if chase_mode:
            print("chase")
            if  wandering_count < wandering_change_time:
                wandering_count +=1
            else:
                chase_mode = False
                wandering_count = 0
        else:
            print("wandering")
            if wandering_count < wandering_duration:
                wandering_count +=1
            else:
                chase_mode = True
                wandering_count = 0

        #added chase and wandering_count zum reseten des cooldowns
        score, zeit, chase_mode, wandering_count  = update_game(
            player_pos, ghost1_pos, ghost2_pos, direction, ghost1_direction, ghost2_direction, input_direction, level, score, zeit, essen, chase_mode, wandering_count)
        #added clock_ticks
        pygame.display.flip()
        clock.tick(clock_ticks)

    pygame.quit()

if __name__ == "__main__":
    main()