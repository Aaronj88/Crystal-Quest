import pygame
import random
import time
import sys

pygame.init()
pygame.font.init()

# screen
info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h
scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Walk Around')

# vars (p_speed is pixels per second now)
p_speed = 250.0
base_speed = 250.0
lives = 3
points = 0
level = 1
c_size = 50
base_size = 50
direction = "right"

# colors
w = (255,255,255)
b = (0,0,0)
r = (255,0,0)
g = (0,255,0)

# ui
font = pygame.font.SysFont('Arial', 35)
font_big = pygame.font.SysFont('msgothic', 120)

# game state
game_over_state = False
win_state = False

# player images (fix flip bug by storing originals)
plyr_orig = pygame.image.load("player.png").convert_alpha()
plyr_right = pygame.transform.scale(plyr_orig, (80, 80))
plyr_left = pygame.transform.flip(plyr_right, True, False)
plyr = plyr_right
plyr_rect = plyr.get_rect()
plyr_rect.center = (WIDTH//2, HEIGHT//2)

# coin
coin_img = pygame.image.load("coin.png").convert_alpha()
def respawn_coin():
    global coin_scaled, coin_rect
    size = max(5, int(c_size))
    coin_scaled = pygame.transform.scale(coin_img, (size, size))
    coin_rect = coin_scaled.get_rect()
    coin_rect.x = random.randint(10, WIDTH - size - 10)
    coin_rect.y = random.randint(10, HEIGHT - size - 10)
respawn_coin()

# crystal
crystal_img = pygame.image.load("crystal.png").convert_alpha()
crystal_active = False
crystal_time = 0

# walls
walls = []

# heart
heart = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart,(65,65))
heart_rect = heart.get_rect()

# bg
bg_r_val = 255
bg_g_val = 0
bg_b_val = 255
bg_col = (bg_r_val,bg_g_val,bg_b_val)
txt_c = (255,255,255)

# movement - dt-based, p_speed is pixels/sec
def handle_move(keys, dt):
    global direction, plyr, plyr_rect
    moved = False
    move_amount = p_speed * dt

    if keys[pygame.K_LEFT]:
        if direction != "left":
            direction = "left"
            plyr = plyr_left
        plyr_rect.x -= move_amount
        moved = True

    if keys[pygame.K_RIGHT]:
        if direction != "right":
            direction = "right"
            plyr = plyr_right
        plyr_rect.x += move_amount
        moved = True

    if keys[pygame.K_UP]:
        plyr_rect.y -= move_amount
        moved = True

    if keys[pygame.K_DOWN]:
        plyr_rect.y += move_amount
        moved = True

    # stay inside screen
    plyr_rect.x = max(0, min(plyr_rect.x, WIDTH - plyr_rect.width))
    plyr_rect.y = max(0, min(plyr_rect.y, HEIGHT - plyr_rect.height))


# touch border
def check_border_touch():
    if plyr_rect.left <= 0 or plyr_rect.top <= 0 or plyr_rect.right >= WIDTH or plyr_rect.bottom >= HEIGHT:
        lose_life("border")


# lose life
def lose_life(reason=''):
    global lives, p_speed, walls, crystal_active, plyr_rect, game_over_state

    lives -= 1
    plyr_rect.center = (WIDTH//2, HEIGHT//2)
    p_speed = max(base_speed, p_speed - 20.0)  # speed units now px/sec
    walls.clear()
    crystal_active = False

    if lives <= 0:
        game_over_state = True


# gain life
def add_life():
    global lives, p_speed
    lives += 1
    p_speed = max(base_speed, p_speed - 20.0)


# walls
def spawn_wall():
    wmin, wmax = 60, 300
    hmin, hmax = 20, 150
    tries = 0

    while tries < 40:
        w_ = random.randint(wmin, wmax)
        h_ = random.randint(hmin, hmax)
        x = random.randint(0, WIDTH - w_)
        y = random.randint(0, HEIGHT - h_)

        rect = pygame.Rect(x, y, w_, h_)

        if not rect.colliderect(plyr_rect.inflate(120,120)) and not rect.colliderect(coin_rect.inflate(80,80)):
            color = (random.randint(50,200), random.randint(50,200), random.randint(50,200))
            walls.append({"rect": rect, "color": color, "time": time.time()})
            return
        tries += 1


def maybe_spawn_wall():
    chance = min(0.9, 0.05 + 0.07 * (level - 1))
    if random.random() < chance:
        spawn_wall()


# crystal
def spawn_crystal():
    global crystal_active, crystal_rect, crystal_scaled, crystal_time

    size = max(25, int(c_size * 1.4))
    crystal_scaled = pygame.transform.scale(crystal_img, (size, size * 2))
    crystal_rect = crystal_scaled.get_rect()
    crystal_rect.x = random.randint(10, WIDTH - crystal_rect.width - 10)
    crystal_rect.y = random.randint(10, HEIGHT - crystal_rect.height - 10)

    crystal_time = time.time()
    crystal_active = True


def maybe_spawn_crystal_on_collect():
    if not crystal_active:
        chance = 0.03 + 0.01 * (level - 1)
        if random.random() < chance:
            spawn_crystal()


# points / leveling
def add_points():
    global points, level, c_size, p_speed

    if plyr_rect.colliderect(coin_rect):
        points += 1
        c_size -= 1
        if c_size <= 5:
            c_size = int(base_size * 0.9)

        p_speed += 12.0  # small boost in px/sec
        respawn_coin()

        new_lvl = points // 10 + 1 # 10 + 1
        if new_lvl > level:
            level_up(new_lvl)

        maybe_spawn_wall()
        maybe_spawn_crystal_on_collect()


def level_up(n):
    global level, bg_col, txt_c, p_speed, win_state, bg_r_val, bg_g_val, bg_b_val
    level = n

    bg_g_val +=25
    bg_b_val -=25
    bg_col = (bg_r_val,bg_g_val,bg_b_val)
    txt_c = (255,255,255)

    p_speed += 20.0  # level speed boost
    if level > 10:
        win_state = True


# collisions
def handle_collisions():
    global crystal_active

    if crystal_active and plyr_rect.colliderect(crystal_rect):
        add_life()
        crystal_active = False

    for wdict in list(walls):
        if plyr_rect.colliderect(wdict["rect"]):
            try:
                walls.remove(wdict)
            except ValueError:
                pass
            lose_life("wall")
            break


def update_walls():
    now = time.time()
    life = 6 + level
    new = []
    for wdict in walls:
        if now - wdict["time"] < life:
            new.append(wdict)
    walls[:] = new


# drawing
def draw():
    scr.fill(bg_col)

    if not game_over_state:
        scr.blit(plyr, plyr_rect)
        scr.blit(coin_scaled, coin_rect)
        scr.blit(heart,heart_rect)

    if crystal_active and not game_over_state:
        scr.blit(crystal_scaled, crystal_rect)

    for wdict in walls:
        pygame.draw.rect(scr, wdict["color"], wdict["rect"])

    p = font.render(f"Points: {points}", 1, txt_c)
    l = font.render(f"Level: {level}/10", 1, txt_c)
    h = font.render(f"Lives: {lives}", 1, txt_c)
    scr.blit(p, (10,10))
    scr.blit(l, (10,50))
    scr.blit(h, (1800,10))


    if win_state:
        txt = font_big.render("You Win!", 1, g)
        scr.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))

    if game_over_state:
        txt = font_big.render("Game Over", 1, r)
        scr.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//3))


# main
def main():
    global crystal_active, win_state, game_over_state

    last_time = time.time()
    running = True
    while running:
        now = time.time()
        dt = now - last_time
        last_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if win_state or game_over_state:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart()
            draw()
            pygame.display.update()
            continue

        keys = pygame.key.get_pressed()
        handle_move(keys, dt)
        if keys[pygame.K_ESCAPE]:
            running = False

        check_border_touch()
        add_points()
        handle_collisions()
        update_walls()

        if not crystal_active and random.random() < 0.0008 * max(1, level):
            spawn_crystal()

        if crystal_active and time.time() - crystal_time > max(6, 12 - level):
            crystal_active = False

        draw()
        pygame.display.update()

    pygame.quit()


def restart():
    global p_speed, lives, points, level, c_size, win_state, game_over_state, walls, crystal_active
    p_speed = base_speed
    lives = 3
    points = 0
    level = 1
    c_size = base_size
    walls.clear()
    crystal_active = False
    win_state = False
    game_over_state = False
    plyr_rect.center = (WIDTH//2, HEIGHT//2)
    respawn_coin()


if __name__ == "__main__":
    main()
