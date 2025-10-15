import os
import random
import time
import pygame
import sys

pygame.font.init()
pygame.display.init()  # Initialize the display to get the default information
InfoObject = pygame.display.Info()  # Get the information about the display

HEIGHT = InfoObject.current_h
WIDTH = InfoObject.current_w

scr = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Walk Around')

v = 1
size = 50
coin_posx = random.randint(10, WIDTH - size)
coin_posy = random.randint(10, HEIGHT - size)
points = 0
timer = 0
FONT = pygame.font.SysFont('Arial', 35)
FONT_go = pygame.font.SysFont("msgothic",300) #msgothic
direction = ""
r_prop = random.randint(0, 255)

w = (255, 255, 255)
b = (000, 000, 000)
r = (255, 000, 000)
g = (000, 255, 000)
bl = (000, 000, 255)
r_color = (r_prop, r_prop, r_prop)
r_col_fn = (255, 255, 255)
txt_color = (b)
#making the coin/player
plyr = pygame.image.load('player.png')
plyr_scaled = pygame.transform.scale(plyr, (100, 100))
plyr_rect = plyr_scaled.get_rect()
plyr_rect.center = (400, 300)
scr.blit(plyr_scaled, plyr_rect)
showplayer = True

coin = pygame.image.load('coin.png')
coin_scaled = pygame.transform.scale(coin, (size, size))
coin_rect = coin_scaled.get_rect()
coin_rect.center = (coin_posx, coin_posy)
scr.blit(coin_scaled, coin_rect)
showcoin = True

crystal = pygame.image.load('crystal.png')
crystal = pygame.transform.scale(crystal, (size,size*2))
crystal = 

#movement of player
def handle_movement(keys_pressed):
  global plyr, plyr_scaled, plyr_rect, direction
  if keys_pressed[pygame.K_LEFT]:  # LEFT
    if direction == 'left':
      pass
    else:
      plyr_scaled = pygame.transform.flip(plyr_scaled, True,False)  # Flip the image horizontally
    plyr_rect.x -= v
    direction = 'left'

  if keys_pressed[pygame.K_RIGHT]:  # RIGHT
    if direction == 'right':
      pass
    else:
      plyr_scaled = pygame.transform.flip(
          plyr_scaled, True, False)  # Reset the image to how it was
    direction = 'right'
    plyr_rect.x += v

  if keys_pressed[pygame.K_UP]:  # UP
    plyr_rect.y -= v

  elif keys_pressed[pygame.K_DOWN]:  # DOWN
    plyr_rect.y += v


def stay_in():
  global HEIGHT, WIDTH, plyr_rect
  if plyr_rect.top < 0 or plyr_rect.bottom > HEIGHT or plyr_rect.left < 0 or plyr_rect.right > WIDTH:
    game_over()


def add_points():
  global points, size, v, coin_scaled, WIDTH, HEIGHT, coin, r_col_fn, r_color, txt_color
  if pygame.Rect.colliderect(plyr_rect, coin_rect):
    points += 1
    coin_rect.x = random.randint(10, WIDTH - size)
    coin_rect.y = random.randint(10, HEIGHT - size)
    v += 0.1
    size -= 1
    coin_scaled = pygame.transform.scale(coin, (size, size))
    if size <= 5:
      size = 45
    if points%10 == 0:
      r_col_fn = r_color
      r_prop1 = random.randint(0, 255)
      r_prop2 = random.randint(0, 255)
      r_prop3 = random.randint(0, 255)
      r_color = (r_prop1, r_prop2, r_prop3)
      txt_c_prop1 = random.randint(0, 255)
      txt_c_prop2 = random.randint(0, 255)
      txt_c_prop3 = random.randint(0, 255)
      txt_color = (txt_c_prop1, txt_c_prop2, txt_c_prop3)
  
def game_over():
  global showplayer, showcoin, HEIGHT, WIDTH
  showcoin = False
  showplayer = False
  scr.fill(b)
  g_o = FONT_go.render("Game Over.",1,r)
  scr.blit(g_o,(WIDTH//3-300,HEIGHT//3))



def main():
  global plyr_scaled, coin_scaled, v, size, direction, r_col_fn, txt_color
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()

    keys_pressed = pygame.key.get_pressed()

    handle_movement(keys_pressed)

    scr.fill(r_col_fn)

    if showplayer and showcoin:
      scr.blit(plyr_scaled, plyr_rect)
      scr.blit(coin_scaled, coin_rect)

    point = FONT.render(str(points), 1, txt_color)
    scr.blit(point, (WIDTH // 2, 10))

    stay_in()
    add_points(
    )  # Call the add_points function to handle point increment, coin movement, and character speed/size changes

    pygame.display.update()


main()
