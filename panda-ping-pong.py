# Panda ping pong via LLMs
# Note: Code does not run!
# 3 graphics files are needed: panda1.png, panda2.png, ball.png

import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Load assets
panda1_img = pygame.image.load('panda1.png')
panda2_img = pygame.image.load('panda2.png')
ball_img = pygame.image.load('ball.png')

class Paddle(pygame.sprite.Sprite):
  def __init__(self, x, y):
    super().__init__()
    self.image = panda1_img if x < 400 else panda2_img
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

  def update(self):
    keys = pygame.key.get_pressed()
    if self.rect.x < 400:
      self.rect.y += -5 if keys[pygame.K_w] else 5
    else:
      self.rect.y += -5 if keys[pygame.K_UP] else 5
    self.rect.clamp_ip(screen.get_rect())

class Ball(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = ball_img
    self.rect = self.image.get_rect(center=(400,300))
    self.dx = 5
    self.dy = 5

  def update(self):
    self.rect.x += self.dx
    self.rect.y += self.dy
    if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
      self.dy *= -1
    if self.rect.left < 0:
      self.winner = 2
      self.reset()
    if self.rect.right > SCREEN_WIDTH:
      self.winner = 1
      self.reset()

  def reset(self):
    self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    self.dx *= -1
    self.dy = 5

# Create sprite groups
all_sprites = pygame.sprite.Group()
paddles = pygame.sprite.Group()

paddle1 = Paddle(50, 250)
paddle2 = Paddle(750, 250)
ball = Ball()

all_sprites.add(paddle1, paddle2, ball)
paddles.add(paddle1, paddle2)

# Game loop
score1, score2 = 0, 0
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  all_sprites.update()

  if ball.winner:
    score1 += 1 if ball.winner == 1 else 0
    score2 += 1 if ball.winner == 2 else 0
    ball.reset()

  screen.fill('black')
  all_sprites.draw(screen)

  pygame.display.flip()
  clock.tick(60)
