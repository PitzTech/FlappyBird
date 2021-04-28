import random
import pygame
from pygame.locals import *

SCREEN_SIZE = (400, 700)
PIPE_SIZE = (100, 400)
SPRITES = "assets/sprites/"
SPEED = 10
GRAVITY = 1
GAME_SPEED = 15
PIPE_GAP = 200

# __ = dunder
# __init__ = dunder init 

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(SPRITES+"yellowbird-upflap.png").convert_alpha(),
                      pygame.image.load(SPRITES+"yellowbird-midflap.png").convert_alpha(),
                      pygame.image.load(SPRITES+"yellowbird-downflap.png").convert_alpha()]
        self.current_image = 0

        self.image = self.images[0]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_SIZE[0] / 2 # LEFT POS
        self.rect[1] = SCREEN_SIZE[1] /2  # TOP POS

        self.speed = SPEED
    
    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        
        self.speed += GRAVITY
    
        # update height
        self.rect[1] += self.speed


    def bumb(self):
        self.speed = -SPEED
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(SPRITES + "pipe-green.png")
        self.image = pygame.transform.scale(self.image, PIPE_SIZE)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_SIZE[1] - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.height = 100
        self.width = SCREEN_SIZE[0] * 2
        
        self.image = pygame.image.load(SPRITES+"base.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_SIZE[1] - self.height

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_offscreen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_SIZE[1] - size - PIPE_GAP)

    return (pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)

BACKGROUND = pygame.image.load(SPRITES+"background-day.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, SCREEN_SIZE)

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(SCREEN_SIZE[0] * 2 * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_SIZE[0] * i + 1000)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(24)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bumb()
 
    screen.blit(BACKGROUND, (0,0))

    if is_offscreen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(2 * SCREEN_SIZE[0] - 20)
        ground_group.add(new_ground)
    
    if is_offscreen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        
        pipes = get_random_pipes(SCREEN_SIZE[0] * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or 
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        # Game Over
        break
