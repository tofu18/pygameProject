import pygame
import os
import sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((700, 400))
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

a = pygame.time.Clock()
print(a.get_time())

a.tick()

print(a.get_time())

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if colorkey is not None:
        image = pygame.image.load(fullname).convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = pygame.image.load(fullname).convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    logo = pygame.transform.scale(load_image('logo.png'), (600, 200))
    fon = pygame.transform.scale(load_image('background.jpg'), (700, 400))
    button = pygame.transform.scale(load_image('button.png'), (250, 100))
    button1 = pygame.transform.scale(load_image('button1.png'), (250, 100))

    screen.blit(fon, (0, 0))
    screen.blit(logo, (10, 0))
    screen.blit(button, (50, 250))
    screen.blit(button1, (400, 250))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(50, 300) and event.pos[1] in range(250, 350):
                    return True
                elif event.pos[0] in range(400, 650) and event.pos[1] in range(250, 350):
                    terminate()
        pygame.display.flip()


def pause_screen():
    pause_screen = pygame.display.set_mode((700, 400))
    fon = pygame.transform.scale(load_image('background.jpg'), (700, 400))
    pause_screen.blit(fon, (0, 0))
    button = pygame.transform.scale(load_image('restart.png'), (200, 100))
    button1 = pygame.transform.scale(load_image('resume.png'), (200, 100))
    button2 = pygame.transform.scale(load_image('exit.png'), (200, 100))
    logo = pygame.transform.scale(load_image('logo1.png'), (600, 200))
    pause_screen.blit(button, (20, 250))
    pause_screen.blit(button1, (250, 250))
    pause_screen.blit(button2, (470, 250))
    pause_screen.blit(logo, (20, 20))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(250, 450) and event.pos[1] in range(250, 350):
                    return True
                elif event.pos[0] in range(470, 670) and event.pos[1] in range(250, 350):
                    terminate()
            elif event.type == pygame.KEYDOWN and event.key == 27:
                return True


class Player(pygame.sprite.Sprite):
    player_image = pygame.transform.scale(load_image('spaceship.png'), (50, 100))
    player_image2 = pygame.transform.scale(load_image('forward.png'), (50, 100))

    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.image = Player.player_image
        self.rect = self.image.get_rect()
        self.clock = pygame.time.Clock()
        self.new_rect = [self.rect.x, self.rect.y]
        self.hp = 3
        self.bullet_clock = pygame.time.Clock()
        pygame.mixer.pre_init(16500, -16, 2, 2048)
        self.sound = pygame.mixer.Sound(os.path.join('data', 'pew.wav'))

    def update(self, *args):

        self.image = Player.player_image
        if len(args) != 0:
            event = args[0]
            if event.type == pygame.KEYDOWN and event.key == 32:
                self.sound.stop()
                self.sound.play()
                Bullet(self.rect.x + 20, self.rect.y, bullet_group)

        symbol = [None, None]
        time = self.clock.tick()

        if pygame.key.get_pressed()[276] == 1 and self.rect.x > 0:
            symbol[0] = '-'

        elif pygame.key.get_pressed()[275] == 1 and self.rect.x < 750:
            symbol[0] = '+'

        if pygame.key.get_pressed()[274] == 1 and self.rect.y < 520:
            symbol[1] = '+'

        elif pygame.key.get_pressed()[273] == 1 and self.rect.y > 0:
            self.image = Player.player_image2
            symbol[1] = '-'

        if symbol[0] is not None or symbol[1] is not None:
            if symbol[0] is not None and symbol[1] is not None:
                self.new_rect = eval(
                    f'[self.new_rect[0] {symbol[0]} 100 * {time} / 1000, self.new_rect[1] {symbol[1]} 100 * time / 1000]')
            elif symbol[0] is not None:
                self.new_rect[0] = eval(f'self.new_rect[0] {symbol[0]} 200 * time / 1000')
            else:
                self.new_rect[1] = eval(f'self.new_rect[1] {symbol[1]} 200 * time / 1000')

        self.rect.x, self.rect.y = int(self.new_rect[0]), int(self.new_rect[1])

    def get_coords(self):
        return self.rect.x + 20, self.rect.y + 20


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (10, 10))

    def __init__(self, x, y, group, x1, y1):
        super().__init__(all_sprites, group)
        self.image = Bullet.image
        self.rect = self.image.get_rect().move(x, y)
        self.new_rect = [self.rect.x, self.rect.y]
        self.clock = pygame.time.Clock()
        self.coords = (x, y, x1, y1)
        self.path = abs(self.coords[2] - self.coords[0]), (self.coords[3] - self.coords[1])
        if x1 > x:
            self.symbol1 = '+'
        else:
            self.symbol1 = '-'
        if y1 > y:
            self.symbol2 = '+'
        else:
            self.symbol2 = '+'
        print(self.path)


    def update(self, *args):
        if len(args) != 0:
            self.clock.tick()
        time = self.clock.tick()
        if self.path[0] >= self.path[1]:
            self.new_rect = [eval(f'self.new_rect[0] {self.symbol1} 250 * time / 1000'), eval(
                f'self.new_rect[1] {self.symbol2} (250 * (self.path[1] / self.path[0])) * time / 1000')]
        else:
            self.new_rect = [eval(f'self.new_rect[0] {self.symbol1} 250 * (self.path[0] / self.path[1]) * time / 1000'), eval(
                f'self.new_rect[1] {self.symbol2} (250) * time / 1000')]
        self.rect.y = int(self.new_rect[1])
        self.rect.x = int(self.new_rect[0])
        if self.rect.y > 600:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('alien.png'), (50, 50))
    image = pygame.transform.rotate(image, 180)

    def __init__(self, player):
        super().__init__(all_sprites, enemy_group)
        self.player = player
        self.image = Enemy.image
        self.rect = self.image.get_rect().move(200, 200)
        self.clock = pygame.time.Clock()
        self.a = 0

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, bullet_group):
            self.kill()
        time = self.clock.tick()
        if self.a < 2000:
            self.a += time
        else:
            coords = self.player.get_coords()
            Bullet(self.rect.x + 25, self.rect.y + 50, enemy_bullet_group, coords[0], coords[1])
            self.a = 0





start_screen()
screen = pygame.display.set_mode((800, 600))
background = pygame.transform.scale(load_image('download.jpg'), (1920, 2500))
screen.blit(background, (0, -1250))
new_coord = -1250
player = Player()
Enemy(player)
all_sprites.draw(screen)
pygame.display.flip()
clock = pygame.time.Clock()
running = True
pygame.mixer.pre_init(16500, -16, 2, 2048)
music = pygame.mixer.Sound(os.path.join('data', 'back_music.wav'))
music.play(-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == 27:
            pause_screen()
            screen = pygame.display.set_mode((800, 600))
            bullet_group.update(True)
            clock.tick()


        player_group.update(event)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    if new_coord > 0:
        screen.blit(background, (0, -1250))
        new_coord = -1250
    new_coord += 30 * clock.tick() / 1000
    screen.blit(background, (0, int(new_coord)))
