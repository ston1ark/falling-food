import pygame as pg
import random
import sys
import os
pg.init()
pg.font.init()


WIDTH, HEIGHT = 1100, 800

WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Falling Foods!')

VEL = 2
BERRY_VEL = 1
BERRY_RADIUS = 15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 165

FOX_WIDTH, FOX_HEIGHT = 200, 200
BACKGROUND_IMAGE = pg.image.load(os.path.join('assets', 'forest.jpg'))

SPAWN_EVENT, DELAY = pg.USEREVENT + 1, 1000
COLLECTED = pg.USEREVENT + 2
DROPPED = pg.USEREVENT + 3
pg.time.set_timer(SPAWN_EVENT, DELAY)

FOX_IMAGE = pg.image.load(os.path.join('assets', 'fox.png'))
FOX = pg.transform.scale(FOX_IMAGE, (FOX_WIDTH, FOX_HEIGHT))
FOX_FLIPPED = pg.transform.flip(FOX, True, False)

MAIN_FONT = pg.font.SysFont('comicsans', 40)
WINNER_FONT = pg.font.SysFont('comicsans', 100)


class Berry:

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.y_vel = BERRY_VEL

    def draw(self, win):
        pg.draw.circle(win, RED, (self.x, self.y), self.radius)


def draw_window(fox_rect, berries, score, orientation):
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND_IMAGE, (0, 0))
    if orientation == 'LEFT':
        WIN.blit(FOX, fox_rect)
    elif orientation == 'RIGHT':
        WIN.blit(FOX_FLIPPED, fox_rect)

    draw_score(score)

    for berry in berries:
        # pg.draw.rect(WIN, RED, berry)
        pg.draw.circle(WIN, RED, berry.center, BERRY_RADIUS)


def handle_berries(berries, fox_rect):
    for berry in berries:
        berry.y += BERRY_VEL
        if berry.y + berry.height + VEL > HEIGHT:
            berries.remove(berry)
            pg.event.post(pg.event.Event(DROPPED))
        elif berry.colliderect(fox_rect):
            berries.remove(berry)
            pg.event.post(pg.event.Event(COLLECTED))


def draw_score(score):

    display_text = f'SCORE: {score}'
    score_text = MAIN_FONT.render(display_text, True, BLACK)
    WIN.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 10))

    if score >= 20:
        text = WINNER_FONT.render('You won!', True, BLACK)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pg.display.update()
        pg.time.delay(5000)
    if score <= -10:
        text = WINNER_FONT.render('You lost!', True, BLACK)
        WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pg.display.update()
        pg.time.delay(5000)


def main():
    clock = pg.time.Clock()

    fox_rect = pg.Rect(WIDTH//2 - FOX.get_width()//2, HEIGHT - FOX.get_height(), FOX_WIDTH, FOX_HEIGHT)

    berries = []

    orientation = 'LEFT'

    dropped = 0
    collected = 0

    running = True
    while running:
        clock.tick(FPS)

        berry = Berry(random.randint(0, WIDTH - BERRY_RADIUS), 10, BERRY_RADIUS)
        berry_rect = pg.Rect(berry.x, 10, BERRY_RADIUS, BERRY_RADIUS)

        score = collected - dropped

        draw_window(fox_rect, berries, score, orientation)
        keys = pg.key.get_pressed()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('Thanks for playing!')
                sys.exit()

            if event.type == SPAWN_EVENT:
                berries.append(berry_rect)

            if event.type == COLLECTED:
                collected += 1
            if event.type == DROPPED:
                dropped += 1

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            orientation = 'LEFT'
            if fox_rect.x > 0:
                fox_rect.x -= VEL
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            orientation = 'RIGHT'
            if fox_rect.x + fox_rect.width < WIDTH:
                fox_rect.x += VEL

        handle_berries(berries, fox_rect)
        pg.display.update()

    main()


if __name__ == '__main__':
    main()
