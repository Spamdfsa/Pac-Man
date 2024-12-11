import pygame
import os
import time
import math
import json
import random

# initialisieren von pygame
pygame.init()

# Initialisierung
def screen_draw(WIDTH, HEIGHT):
    HEIGHT += HEIGHT * .15
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pac-Man")
    return screen

# Musik/Soundeffekte einrichten
def essen_sound():
    Loudnes = 0.2
    pygame.mixer.music.load('Musik/Pacman_Main_Theme.wav')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(Loudnes)
    essen = pygame.mixer.Sound('Musik/Pacman_Eat.wav')
    return essen

# Bilder Einlesen
def Pacman_Ghost_Image_Load(TILE_SIZE):
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

def map_einlesen(WIDTH,HEIGHT):
    return pygame.transform.scale(pygame.image.load("Karte/Spielfeld.png"), (WIDTH, HEIGHT))

def draw_text(text, font, color, screen, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))
def background_video_load(SCALING):
    HEIGHT = 600*SCALING
    WIDTH = 1066*SCALING
    frame_folder = "background_video"
    frame_files = sorted(os.listdir(frame_folder))
    frames = []
    for frame_file in frame_files:
        frame_path = os.path.join(frame_folder, frame_file)
        frame_image = pygame.image.load(frame_path)
        frame_image = pygame.transform.scale(frame_image, (WIDTH, HEIGHT))
        frames.append(frame_image)
    return frames

def picture_scaling(WIDTH, scale_factor, image):
    original_width, original_height = image.get_size()  # Originalgröße des Bildes
    target_width = int(WIDTH * scale_factor)  # 40% der Bildschirmbreite
    target_height = int(original_height * (target_width / original_width))  # Höhe wird proportional zur Breite angepasst

    # Bild skalieren
    return pygame.transform.scale(image, (target_width, target_height))
    
def menu(frames, clock, SCALING):
    HEIGHT = 600 * SCALING
    WIDTH = 1066 * SCALING
    running = True
    frame_index = 0
    font = pygame.font.SysFont("arial", 30)

    start_button = pygame.image.load("buttons/start_button.png")
    leave_button = pygame.image.load("buttons/leave_button.png")
    highscore_button = pygame.image.load("buttons/highscore.png")
    start_button_scaled = picture_scaling(WIDTH, 0.4, start_button)
    leave_button_scaled = picture_scaling(WIDTH, 0.4, leave_button)
    highscore_button_scaled = picture_scaling(WIDTH, 0.4, highscore_button)

    # Rechtecke für die Schaltflächen erstellen
    start_button_rect = start_button_scaled.get_rect(topleft=(WIDTH*0.5-WIDTH*0.2, HEIGHT*0.1))
    leave_button_rect = leave_button_scaled.get_rect(topleft=(WIDTH*0.5-WIDTH*0.2, HEIGHT*0.65))
    highscore_button_rect = highscore_button_scaled.get_rect(topleft=(WIDTH*0.5-WIDTH*0.2, HEIGHT*0.35))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menü")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                running = False
            #Stellt sicher, dass das gesammte spiel geschlossen wird
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

            # Überprüft, ob eine Schaltfläche angeklickt wurde
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):  # Prüft, ob die Klickposition im Startbutton-Rechteck ist
                    running = False
                elif leave_button_rect.collidepoint(event.pos):  # Prüft, ob die Klickposition im Leave-Button-Rechteck ist
                    return False
                elif highscore_button_rect.collidepoint(event.pos):  # Prüft, ob die Klickposition im Highscore-Button-Rechteck ist
                    #error = pygame.mixer.Sound('Musik/error.wav')
                    #pygame.mixer.Sound.play(error)
                    highscore_file = "highscore/highscores.json"
                    highscores = []
                    if os.path.exists(highscore_file):
                        with open(highscore_file, "r") as file:
                            highscores = json.load(file)
                    else:
                        with open(highscore_file, "w") as file:
                            json.dump([], file)
                    show_highscores(screen, highscores, font, WIDTH, HEIGHT,frames, clock,SCALING)
                    

        # Frame anzeigen
        if frame_index < len(frames):
            screen.blit(frames[frame_index], (0, 0))
            pygame.display.update()
            frame_index += 1
        else:
            frame_index = 0  # Wiederholung oder Beenden der Schleife

        # Schaltflächen anzeigen
        screen.blit(start_button_scaled, (WIDTH*0.5-WIDTH*0.2, HEIGHT*0.1))
        screen.blit(leave_button_scaled, (WIDTH*0.5-WIDTH*0.2, HEIGHT*0.65))
        screen.blit(highscore_button_scaled, (WIDTH*0.5-WIDTH*0.2, HEIGHT*0.35))
        pygame.display.flip()
        clock.tick(24)

    return True

#highscore eingeben 
def highscore_menu(score,frames, clock,SCALING):
    HEIGHT = 600 * SCALING
    WIDTH = 1066 * SCALING
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("highscore_eingabe")
    font = pygame.font.SysFont("arial", 30)
    input_active = True
    user_name = ""

    highscore_file = "highscore/highscores.json"
    highscores = []

    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as file:
            highscores = json.load(file)
    else:
        with open(highscore_file, "w") as file:
            json.dump([], file)
    while input_active:
        screen.fill((0,0,20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Eingabe abgeschlossen
                    input_active = False
                elif event.key == pygame.K_BACKSPACE: #letzes zeichen löschen
                    user_name = user_name[:-1]
                else:
                    if len(user_name) < 10:  # Name begrenzen
                        user_name += event.unicode

        # Eingabetext anzeigen
        input_text = font.render(f"Enter your name: {user_name}", True, (255, 255, 255))
        screen.blit(input_text, (WIDTH*0.4, HEIGHT / 3))

        pygame.display.flip()

    # Highscore speichern
    highscores.append({"name": user_name, "score": score})
    highscores = sorted(highscores, key=lambda x: x["score"], reverse=True)  # Nach Score sortieren

    # Zurück in die JSON-Datei schreiben
    with open(highscore_file, "w") as file:
        json.dump(highscores, file, indent=4)

    # Highscore-Liste anzeigen
    show_highscores(screen, highscores, font, WIDTH, HEIGHT, frames,clock,SCALING)

#highscore anzeigen
def show_highscores(screen, highscores, font, WIDTH, HEIGHT,frames,clock,SCALING):
    running = True
    COLORS = {
    "background": (0, 0, 20),
    }
    pygame.display.set_caption("highscore")
    while running:
        screen.fill((COLORS["background"]))
        title = font.render("Highscores", True, (255, 255, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        for i, entry in enumerate(highscores[:10]):  # Zeige die Top 10
            text = font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
            screen.blit(text, (100, 150 + i * 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
               

        pygame.display.flip()
    menu(frames, clock, SCALING) 

    
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
#tint for firghtend mode
def tint_image_blue(image):
    tinted_image = image.copy()
    tinted_image.fill((100, 100, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted_image

def move_ghost(player_pos, ghost_direction, ghost_pos, level, frightened_mode):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(level), len(level[0])
    possible_directions = []
    closest_direction = None
    min_distance = float('inf')

    # Rückwärtsrichtung zum ausschließen bestimmen
    reverse_direction = (-ghost_direction[0], -ghost_direction[1])

    for direction in directions:
        # Rückwärtsbewegung ausschließen
        if direction != reverse_direction:
            new_pos = [ghost_pos[0] + direction[0], ghost_pos[1] + direction[1]]
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] != 1:
                possible_directions.append(direction)

    if (not frightened_mode) and possible_directions:
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
    #not in um 1 und 5 auszuschließen 1=wand, 5=geisterhaus
    if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] not in [1, 5]):
        player_pos[:] = new_pos
        direction[:] = input_direction
    else:
        # taking the old direction, because found a wall with the current
        new_pos = [player_pos[0] + direction[0], player_pos[1] + direction[1]]
        if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and level[new_pos[0]][new_pos[1]] not in [1, 5]):
            player_pos[:] = new_pos


def check_player_collision(ghost_positions, player_pos, frightened_mode, level, score):
    got_hit = False

    ghost_house = [(row, col) for row in range(len(level)) 
        for col in range(len(level[row])) 
        if level[row][col] == 5 and (row != player_pos[0] or col != player_pos[1])]

    if not ghost_house:
        print("No ghost_house (5) defined on map, nothing happens")
        return False

    for ghost_pos in ghost_positions:
        if abs(ghost_pos[0] - player_pos[0]) <= 1 and abs(ghost_pos[1] - player_pos[1]) <= 1:
            if frightened_mode:
                ghost_pos[:] = random.choice(ghost_house)
                score += 500
            else:
                frightened_mode = True
                got_hit = True

    if got_hit:
        for ghost_pos in ghost_positions:
            ghost_pos[:] = random.choice(ghost_house)

    return frightened_mode, got_hit, score



def update_game(player_pos, ghost1_pos, ghost2_pos, direction, ghost1_direction, ghost2_direction, input_direction, level, score, zeit, essen, frightened_mode, frightened_count):
    move_player(player_pos, direction, input_direction, level)
    move_ghost(player_pos, ghost1_direction, ghost1_pos, level, frightened_mode)
    move_ghost(player_pos, ghost2_direction, ghost2_pos, level, frightened_mode)

    # Teleportieren bei Tunnel 4
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
    
    #checks if player collects big coin
    if level[player_pos[0]][player_pos[1]] == 3:
        frightened_count = 0
        frightened_mode = True
        ghost1_direction[:] =(-ghost1_direction[0], -ghost1_direction[1])
        ghost2_direction[:] =(-ghost2_direction[0], -ghost2_direction[1])
    
    #checks for sound
    if level[player_pos[0]][player_pos[1]] == 2 or level[player_pos[0]][player_pos[1]] == 3:
        level[player_pos[0]][player_pos[1]] = 0
        score += 10
        zeit_jetzt = time.time()
        #sounds nicht überlagern
        if zeit_jetzt >= zeit + 0.717:
            pygame.mixer.Sound.play(essen)
            zeit = time.time()

    return score, zeit, frightened_mode, frightened_count

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

def start_ghost_pos(level):
    start_pos = []
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 0:
                start_pos.append([row, col])
    
    if start_pos:
        return random.choice(start_pos)
    else:
        print("Keine Startposition (0, da keine Münze) für die Geister gefunden")
        return [0, 0]

def check_for_w(level):
    win = True
    for row in range(len(level)):
        for col in range(len(level[row])):
            if level[row][col] == 2:
                win = False
    return win

def read_level():
    with open('Karte/map.json', 'r') as file:
        data = json.load(file)
    return data

def main():

    pygame.init()

    zeit = time.time()


    # Spielkonfiguration
    SCALING = 1

    TILE_SIZE = 20*SCALING
    WIDTH, HEIGHT = 560*SCALING, 600*SCALING
    running = True
    player_lives = 3
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("PACMAN")
    COLORS = {
        "background": (0, 0, 20),
        "coin": (255, 244, 79),
    }
    frames = background_video_load(SCALING)
    #Sounds einlesen
    essen = essen_sound()
    #Menu
    running = menu(frames, clock,SCALING)
    #clock_tick
    clock_ticks = 10
    font = pygame.font.SysFont("arial", 30)

    # Abspielen des Geistes
    Picture_Frame = 0

    # Verschieben des Geistbildes
    Pixel_movement_right = 10 * SCALING
    Pixel_movement_up = 0

    # Pacman und Geister einlesen
    pacman_idle, pinky, blinky = Pacman_Ghost_Image_Load(TILE_SIZE)

    # Sounds einlesen
    essen = essen_sound()
    # Map
    map = map_einlesen(WIDTH,HEIGHT)

    level = read_level()

    player_pos = [1, 1]
    ghost1_direction = [0, 0]
    ghost1_pos = start_ghost_pos(level)
    ghost2_direction = [0, 0]
    ghost2_pos = start_ghost_pos(level)
    direction = [0, 1]
    input_direction = [0, 0]
    score = 0
    #frightened_mode
    frightened_mode = False
    frightened_duration = 10 * clock_ticks
    frightened_count = 0
    #ghost start to wanderaround without a special coin collectet
    frightened_change_time = 15 * clock_ticks

    
    while running:
   
        # Screen definieren
        screen = screen_draw(WIDTH, HEIGHT)

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
        
        #Geist richtung und Farbe
        pinky_image = pinky
        blinky_image = blinky
        if ghost2_direction[1] < 0:  # Nach links
            pinky_image = pygame.transform.flip(pinky_image, True, False)
        if ghost1_direction[1] > 0:  # Nach links
            blinky_image = pygame.transform.flip(blinky_image, True, False)
        if frightened_mode: 
            pinky_image = tint_image_blue(pinky_image)
            blinky_image = tint_image_blue(blinky_image)
        #Geist 1 zeichnen
        screen.blit(blinky_image,
            (ghost1_pos[1] * TILE_SIZE - 4*SCALING, 
             ghost1_pos[0] * TILE_SIZE - 14*SCALING))
        #Geist 2 zeichnen
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

        #frightened_mode turn off and on
        if frightened_mode:
            if frightened_count < frightened_duration:
                frightened_count +=1
            else:
                frightened_mode = False
                frightened_count = 0
        else:
            if  frightened_count < frightened_change_time:
                frightened_count +=1
            else:
                frightened_mode = True
                frightened_count = 0
        #has a list of the ghost_pos
        frightened_mode, got_hit, score = check_player_collision([ghost1_pos, ghost2_pos], player_pos, frightened_mode, level, score)
        if got_hit:
            got_hit = False
            player_lives -= 1
            print("live lost")
            if 1 > player_lives:
                print("Game Over")
                player_lives = 3
                highscore_menu(score,frames, clock,SCALING)
                # Pacman und Geister einlesen
                pacman_idle, pinky, blinky = Pacman_Ghost_Image_Load(TILE_SIZE)
                # Map
                map = map_einlesen(WIDTH,HEIGHT)
                level = read_level()
                player_pos = [1, 1]
                ghost1_direction = [0, 0]
                ghost1_pos = start_ghost_pos(level)
                ghost2_direction = [0, 0]
                ghost2_pos = start_ghost_pos(level)
                direction = [0, 1]
                input_direction = [0, 0]
                score = 0
        win = check_for_w(level)

        if win or (event.type == pygame.KEYDOWN and event.key == pygame.K_HOME):
            # Pacman und Geister einlesen
            pacman_idle, pinky, blinky = Pacman_Ghost_Image_Load(TILE_SIZE)
            # Map
            map = map_einlesen(WIDTH,HEIGHT)
            level = read_level()
            player_pos = [1, 1]
            ghost1_direction = [0, 0]
            ghost1_pos = start_ghost_pos(level)
            ghost2_direction = [0, 0]
            ghost2_pos = start_ghost_pos(level)
            direction = [0, 1]
            input_direction = [0, 0]
            clock_ticks += 1

        score, zeit, frightened_mode, frightened_count  = update_game(
            player_pos, ghost1_pos, ghost2_pos, direction, ghost1_direction, ghost2_direction, input_direction, level, score, zeit, essen, frightened_mode, frightened_count)

        
        draw_text(str(score),font ,COLORS["coin"],screen, int(WIDTH - 100*SCALING),int(HEIGHT + 20*SCALING))
        draw_text(("Lifes " + str(player_lives)), font, COLORS["coin"], screen, int(60*SCALING), int(HEIGHT +20*SCALING))
        pygame.display.flip()
        clock.tick(clock_ticks)

    pygame.quit()

if __name__ == "__main__":
    main()
