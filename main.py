import math

import pygame

WIDTH, HEIGHT = 956, 546
DEFAULT_IMAGE_SIZE = (100, 100)

IMGS = [pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45)]

BG_IMG = pygame.image.load('kai-bg2.png')

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kai")



FPS = 120
PADDLE_HEIGHT = 40
PADDLE_WIDTH = 10
MAX_VEL = 5

class AbstractSeal:
    def __init__(self, max_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def draw(self, win):
        win.blit(self.img, (0,0))

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians)*self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

class PlayerSeal(AbstractSeal):
    IMG = IMGS[0]
    START_POS = (180, 200)

def draw(win, player_seal):
    win.blit(IMGS[0], (0,0))

    player_seal.draw(win)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    player_seal = PlayerSeal(4)

    run = True
    while run:
        win.blit(BG_IMG, (0,0))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_d]:
            moved = True
            player_seal.move_forward()

        draw(win, player_seal)

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

