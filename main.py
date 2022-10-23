import pygame

WIDTH, HEIGHT = 1920, 1080
DEFAULT_IMAGE_SIZE = (100, 100)

IMGS = [pygame.image.load('seal.png')]
BG_IMG = pygame.image.load('kai-final.png')

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kai")



FPS = 120

class Seal:
    VEL = 5

    def __init__(self, x, y, width, height, color):
        self.img = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, win):
        #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        self.img = pygame.transform.rotate(pygame.transform.scale(IMGS[0], DEFAULT_IMAGE_SIZE), 45)
        win.blit(self.img, (WIDTH/2-50, HEIGHT-200))

def draw(win, paddle):
    paddle.draw(win)
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    seal = Seal(WIDTH / 2, HEIGHT / 2, 10, 10, 'black')

    i = 0
    run = True
    while run:
        win.fill((0,0,0))
        win.blit(BG_IMG, (i,0))
        win.blit(BG_IMG, (WIDTH+i, 0))

        if i == -WIDTH:
            win.blit(BG_IMG, (WIDTH+i, 0))
            i = 0
        i -= 10

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(win, seal)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()

