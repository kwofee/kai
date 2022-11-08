import math
import random

import pygame

WIDTH, HEIGHT = 956, 546
DEFAULT_IMAGE_SIZE = (100, 100)
NUM_OF_GULLS = 5

IMGS = [
    pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),
    pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))
]

BG_IMG = pygame.image.load('kai-bg2.png')

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kai")

def blit_rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)

FPS = 120
PADDLE_HEIGHT = 40
PADDLE_WIDTH = 10
MAX_VEL = 100

class AbstractSeal:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 0
        self.rotation_vel = rotation_vel
        self.x, self.y = self.START_POS
        self.acceleration = 20

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_left(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_right(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.x -= self.vel
    def move(self):
        self.x += self.vel
        self.collide_edge()

    def collide_edge(self):
        if self.x <= 0:
            self.x = WIDTH/2 - 50
        elif self.x + IMGS[0].get_width() >= WIDTH:
            self.x = WIDTH/2 - 50


class PlayerSeal(AbstractSeal):
    IMG = IMGS[0]
    START_POS = (WIDTH/2 - 50, HEIGHT-150)

class Gull:
    def __init__(self):
        self.img = IMGS[1]
        self.num = NUM_OF_GULLS
        # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())
        self.y = random.randrange(self.img.get_height(), HEIGHT-400)
        self.x = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Ball:
    def __init__(self):
        self.img = IMGS[2]
        self.x = 0
        self.y = 0

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

def draw(win, player_seal, gulls, ball):
    player_seal.draw(win)
    for i in gulls:
        i.draw(win)
    ball.draw(win)
    pygame.display.update()




def main():
    clock = pygame.time.Clock()
    player_seal = PlayerSeal(4,4)
    ball = Ball()
    gulls = []
    x = [0, 159, 318, 477, 636]
    y = [159, 318, 477, 636, 956]
    d = [(0, 159), (159, 318), (318, 477), (477, 636), (636,956)]

    for i,j in d:
        gull = Gull()
        gull.x = random.randrange(i, j)
        print(gull.x)
        gulls.append(gull)


    run = True
    while run:
        win.blit(BG_IMG, (0,0))
        clock.tick(FPS)
        draw(win, player_seal, gulls, ball)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_d]:
            moved = True
            player_seal.move_left()
        if keys[pygame.K_a]:
            moved = True
            player_seal.move_right()
        if keys[pygame.K_r]:
            player_seal.rotate(right=True)

        draw(win, player_seal, gulls, ball)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()


# class Seal:
#     VEL = 5
#
#     def __init__(self, x, y, width, height, color):
#         self.img = None
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.color = color
#         self.vel = 0
#         self.max_vel = MAX_VEL
#         self.acceleration = 0.1
#
#     def draw(self, win):
#         #self.img = pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
#         self.img = pygame.transform.rotate(pygame.transform.scale(IMGS[0], DEFAULT_IMAGE_SIZE), 45)
#         win.blit(self.img, (WIDTH/2-50, HEIGHT-200))
#
#     def move_forward(self):
#         self.vel = min(self.vel + self.acceleration, self.max_vel)
#         self.move()
#
#
#     def move(self):
#         self.x += self.vel

