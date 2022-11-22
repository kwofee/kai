import math
import random
import math
import pygame

from flap_bird_game import STAT_FONT

WIDTH, HEIGHT = 956, 546
DEFAULT_IMAGE_SIZE = (100, 100)
NUM_OF_GULLS = 5

IMGS = [
    pygame.transform.rotate(pygame.transform.scale(pygame.image.load('seal.png'), DEFAULT_IMAGE_SIZE), 45),
    pygame.transform.scale(pygame.image.load('seagull.png'), DEFAULT_IMAGE_SIZE),
    pygame.transform.scale(pygame.image.load('beach-ball.png'), (50, 50))
]

BG_IMG = pygame.image.load('kai-bg2.png')
BALL_WIDTH = IMGS[2].get_width()
BALL_HEIGHT = IMGS[2].get_height()

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
MAX_VEL = 200


class AbstractSeal:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.angle = 0
        self.rotation_vel = rotation_vel
        self.x, self.y = self.START_POS
        self.acceleration = 70
        self.width = IMGS[0].get_width()
        self.height = IMGS[0].get_height()
        self.mask = pygame.mask.from_surface(self.img)

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
            self.x = IMGS[0].get_width() + WIDTH
        if self.x + IMGS[0].get_width() >= WIDTH:
            self.x = 0


class PlayerSeal(AbstractSeal):
    IMG = IMGS[0]
    START_POS = (WIDTH / 2 - 50, HEIGHT - 150)


class Gull():
    def __init__(self):
        self.img = IMGS[1]
        self.num = NUM_OF_GULLS
        # self.x = random.randrange(self.img.get_width(), WIDTH-self.img.get_width())
        self.rect = self.img.get_rect()
        self.y = random.randrange(self.img.get_height(), HEIGHT - 400)
        self.x = 0
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Ball:
    VEL = 5

    def __init__(self):
        self.img = IMGS[2]
        self.x, self.y = WIDTH / 2, HEIGHT / 2
        self.angle = 0
        self.x_vel = 0
        self.y_vel = -5
        self.mask = pygame.mask.from_surface(self.img)
        self.score = 0

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        self.x += self.x_vel
        self.y += self.y_vel
        if self.x <= 0 or self.x >= WIDTH - self.img.get_width():
            self.x -= self.x_vel
        if self.y <= 0 or self.y >= HEIGHT - self.img.get_height():
            self.y -= self.y_vel

    def set_vel(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel


def gull_generator(gulls=[]):
    d = [(0, 159), (159, 318), (159, 318), (318, 477), (477, 636), (477, 636), (636, 956)]

    for i, j in d:
        gull = Gull()
        gull.x = random.randrange(i, j)
        gulls.append(gull)

    return gulls


def ball_collision(ball):
    if ball.x - BALL_WIDTH <= 0 or ball.x + BALL_WIDTH >= WIDTH:
        ball.set_vel(ball.x_vel * -1, ball.y_vel)
    if ball.y - BALL_HEIGHT / 2 <= 0 or ball.y + BALL_HEIGHT >= HEIGHT:
        ball.set_vel(ball.x_vel, ball.y_vel * -1)


def ball_seal_collision(ball, seal):
    if not (ball.x <= seal.x + seal.width and ball.x >= seal.x):
        return
    if not (ball.y + BALL_WIDTH >= seal.y):
        return

    seal_center = seal.x + seal.width / 2
    distance_to_center = ball.x - seal_center

    percent_width = distance_to_center / seal.width
    angle = percent_width * 90
    angle_radians = math.radians(angle)

    x_vel = math.sin(angle_radians) * ball.VEL
    y_vel = math.cos(angle_radians) * ball.VEL * -1

    ball.set_vel(x_vel, y_vel)


def ball_gull_collision(ball, gulls, x=0, y=0):
    gull_masks = {}
    ball_mask = ball.mask
    for i in gulls:
        gull_masks[i] = pygame.mask.from_surface(i.img)
    for k in gull_masks:
        offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))
        if ball_mask.overlap(gull_masks[k], offset) is not None:
            k.x = 10000
            ball.score += 100
        else:
            pass
    # for i in gulls:
    #     gull_masks.append(i.mask)a
    # for k in gull_masks:
    #     offset = (int(k.x) - int(ball.x), int(k.y) - int(ball.y))
    #     if ball_mask.overlap(k.mask, offset) != None:
    #         k.img.fill((0,0,0,0))
    #     else:
    #         pass


def draw(win, player_seal, gulls, ball, score):
    player_seal.draw(win)
    for i in gulls:
        i.draw(win)
    ball.draw(win)
    pygame.display.update()



def main():
    clock = pygame.time.Clock()
    player_seal = PlayerSeal(4, 4)
    ball = Ball()
    gulls = gull_generator()
    score = str(ball.score)
    run = True
    while run:
        win.blit(BG_IMG, (0, 0))
        clock.tick(FPS)
        draw(win, player_seal, gulls, ball, score)
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


        ball_collision(ball)
        ball_seal_collision(ball, player_seal)
        ball_gull_collision(ball, gulls)
        print(ball.score)
        if math.ceil(ball.y) in [490, 491, 492, 493, 494]:
            pygame.time.wait(1000)
            pygame.quit()
            quit()
        draw(win, player_seal, gulls, ball, score)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()


