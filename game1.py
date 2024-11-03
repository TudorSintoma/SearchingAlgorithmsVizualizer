import pygame, sys
from pygame.locals import *
import random

pygame.init()

# Set up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        newImage = pygame.image.load("Enemy.png")
        self.image = pygame.transform.scale(newImage, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        newImage = pygame.image.load("Player.png")
        self.image = pygame.transform.scale(newImage, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        if self.rect.bottom > 0:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)
        if self.rect.top < SCREEN_HEIGHT:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Initialize player and enemy
P1 = Player()
E1 = Enemy()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update player and enemy
    P1.update()
    E1.move()

    # Refresh screen
    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)
