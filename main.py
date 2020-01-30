import pygame
import os
import sys
import random

pygame.init()
screen = pygame.display.set_mode((700, 400))
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
shield_group = pygame.sprite.Group()
heat_remover_group = pygame.sprite.Group()
bonus_hp_group = pygame.sprite.Group()

a = pygame.time.Clock()

a.tick()


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


def random_bonus():
    bonuses = ['Shield()', 'HeatRemover()', 'Heart()']

    eval(bonuses[random.randrange(0, 3)])


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
                elif event.pos[0] in range(20, 220) and event.pos[1] in range(250, 350):
                    return False
            elif event.type == pygame.KEYDOWN and event.key == 27:
                return True


def game_over():
    pause_screen = pygame.display.set_mode((700, 400))
    fon = pygame.transform.scale(load_image('background.jpg'), (700, 400))
    pause_screen.blit(fon, (0, 0))
    button = pygame.transform.scale(load_image('restart.png'), (250, 100))
    button2 = pygame.transform.scale(load_image('exit.png'), (250, 100))
    logo = pygame.transform.scale(load_image('logo2.png'), (267, 141))
    pause_screen.blit(button, (50, 250))
    pause_screen.blit(button2, (400, 250))
    pause_screen.blit(logo, (20, 20))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(50, 300) and event.pos[1] in range(250, 350):
                    return True
                elif event.pos[0] in range(470, 670) and event.pos[1] in range(250, 350):
                    terminate()


class Player(pygame.sprite.Sprite):
    player_image = pygame.transform.scale(load_image('spaceship.png'), (50, 50))
    player_image2 = pygame.transform.scale(load_image('forward.png'), (50, 50))
    player_with_shield = pygame.transform.scale(load_image('shield_ship.png'), (70, 70))
    player_with_shield2 = pygame.transform.scale(load_image('forward_shield_ship.png'), (70, 70))

    def __init__(self):
        super().__init__(all_sprites, player_group)
        self.image = Player.player_image
        self.rect = self.image.get_rect().move(300, 300)
        self.clock = pygame.time.Clock()
        self.new_rect = [self.rect.x, self.rect.y]
        self.hp = 3
        self.heatTimer = pygame.time.Clock()
        self.heat = 0
        self.bullet_clock = pygame.time.Clock()
        self.has_shield = False
        self.shield_timer = pygame.time.Clock()
        self.shield_timer1 = 0
        pygame.mixer.pre_init(16500, -16, 2, 2048)
        self.sound = pygame.mixer.Sound(os.path.join('data', 'pew.wav'))

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, bonus_hp_group):
            self.hp += 1
            pygame.sprite.spritecollide(self, bonus_hp_group, True)
        if pygame.sprite.spritecollideany(self, heat_remover_group):
            self.heat = 0
            pygame.sprite.spritecollide(self, heat_remover_group, True)

        if self.heat > 0:
            self.heat -= self.heatTimer.tick() / 300
        else:
            self.heatTimer.tick()
        if pygame.sprite.spritecollideany(self, shield_group):
            pygame.sprite.spritecollide(self, shield_group, True)

            self.image = Player.player_with_shield
            self.has_shield = True
            self.shield_timer.tick()
            self.shield_timer1 = 0
        if self.has_shield:
            self.shield_timer1 += self.shield_timer.tick()
        if self.shield_timer1 > 10000:
            self.image = Player.player_image
            self.has_shield = False
        if not self.has_shield:
            self.image = Player.player_image
        else:
            self.image = Player.player_with_shield
        if pygame.sprite.spritecollideany(self, enemy_bullet_group) and not self.has_shield:
            pygame.sprite.spritecollide(self, enemy_bullet_group, True)
            self.hp -= 1
        if self.hp <= 0:
            self.kill()
        if len(args) != 0:
            event = args[0]
            if event.type == pygame.KEYDOWN and event.key == 32 and self.heat < 90:
                self.sound.stop()
                self.sound.play()
                if self.heat < 100:
                    self.heat += 10

                Bullet(self.rect.x + 20, self.rect.y, bullet_group, self.rect.x + 20, self.rect.y - 600)

        symbol = [None, None]
        time = self.clock.tick()

        if pygame.key.get_pressed()[276] == 1 and self.rect.x > 0:
            symbol[0] = '-'

        elif pygame.key.get_pressed()[275] == 1 and self.rect.x < 750:
            symbol[0] = '+'

        if pygame.key.get_pressed()[274] == 1 and self.rect.y < 520:
            symbol[1] = '+'

        elif pygame.key.get_pressed()[273] == 1 and self.rect.y > 0:
            if not self.has_shield:
                self.image = Player.player_image2
            else:
                self.image = Player.player_with_shield2

            symbol[1] = '-'

        if symbol[0] is not None or symbol[1] is not None:
            if symbol[0] is not None and symbol[1] is not None:
                self.new_rect = eval(
                    f'[self.new_rect[0] {symbol[0]} 200 * {time} / 1000, self.new_rect[1] {symbol[1]} 200 * time / 1000]')
            elif symbol[0] is not None:
                self.new_rect[0] = eval(f'self.new_rect[0] {symbol[0]} 200 * time / 1000')
            else:
                self.new_rect[1] = eval(f'self.new_rect[1] {symbol[1]} 200 * time / 1000')

        self.rect.x, self.rect.y = int(self.new_rect[0]), int(self.new_rect[1])

    def get_coords(self):
        return self.rect.x + 25, self.rect.y + 25

    def get_hp(self):
        return self.hp

    def collision(self):
        if not self.has_shield:
            self.hp -= 1

    def get_heat(self):
        return self.heat


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (4, 9))
    image2 = pygame.transform.scale(load_image('bullet2.png'), (4, 9))

    def __init__(self, x, y, group, x1, y1):
        super().__init__(all_sprites, group)
        if group == bullet_group:
            self.image = Bullet.image2
        else:
            self.image = Bullet.image
        self.group = group
        self.rect = self.image.get_rect().move(x, y)
        self.new_rect = [self.rect.x, self.rect.y]
        self.clock = pygame.time.Clock()
        self.x, self.y, self.new_x, self.new_y = self.rect.x, self.rect.y, x1, y1
        self.path = [abs(self.new_x - self.x), abs(self.new_y - self.y)]

        pygame.mixer.pre_init(16500, -16, 2, 2048)
        self.sound = pygame.mixer.Sound(os.path.join('data', 'pew.wav'))
        if self.path[0] == 0:
            self.path[0] = 1
        if self.path[1] == 0:
            self.path[1] = 1
        self.speed = [self.path[0] / self.path[1], self.path[1] / self.path[0]]

        if self.speed[0] > 2:
            self.speed[0] = 2

        elif self.speed[1] > 2:
            self.speed[1] = 2
        length_y = (self.new_y - self.y)
        if length_y == 0:
            length_y = 1
        if (self.new_x - self.x) / length_y > 0:
            angle = 45
        else:
            angle = -45
        self.image = pygame.transform.rotate(self.image, angle * (self.speed[0]))

        if self.new_x >= self.x:
            self.znak1 = '+'
        else:
            self.znak1 = '-'

        if self.new_y >= self.y:
            self.znak2 = '+'
        else:
            self.znak2 = '-'

    def update(self, *args):

        if self.group == bullet_group and pygame.sprite.spritecollideany(self, enemy_group):
            self.kill()
            pygame.sprite.spritecollide(self, enemy_group, True)
        if self.group == enemy_bullet_group and pygame.sprite.spritecollideany(self, player_group):
            self.kill()

        if len(args) != 0:
            self.clock.tick()
        time = self.clock.tick()

        self.new_rect = [eval(f'self.new_rect[0] {self.znak1} 250 * (self.speed[0]) * time / 1000'),
                         eval(f'self.new_rect[1] {self.znak2} 250 * (self.speed[1]) * time / 1000')]
        self.rect.y = int(self.new_rect[1])
        self.rect.x = int(self.new_rect[0])
        if self.rect.y > 600 or self.rect.y < 0 or self.rect.x < 0 or self.rect.x > 800:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('alien.png'), (50, 50))
    image = pygame.transform.rotate(image, 180)

    def __init__(self, player):
        super().__init__(all_sprites, enemy_group)
        self.player = player
        self.image = Enemy.image
        self.rect = self.image.get_rect().move(random.randrange(0, 700), 0)
        self.clock = pygame.time.Clock()
        self.new_coords = (random.randrange(0, 750), random.randrange(100, 300))
        length_x = abs(self.new_coords[0] - self.rect.x)
        length_y = abs(self.new_coords[1] - self.rect.y)
        if length_x == 0:
            length_x = 1
        if length_y == 0:
            length_y = 1
        self.speed = [length_x / length_y, length_y / length_x]
        if self.speed[0] > 2:
            self.speed[0] = 2
        elif self.speed[1] > 2:
            self.speed[1] = 2
        if self.new_coords[0] >= self.rect.x:
            self.znak = '+'
        else:
            self.znak = '-'
        self.new_rect = [self.rect.x, self.rect.y]

        self.clock = pygame.time.Clock()
        self.arriving_phase = True

        pygame.mixer.pre_init(16500, -16, 2, 2048)
        self.sound = pygame.mixer.Sound(os.path.join('data', 'pew.wav'))
        self.a = 0

    def update(self, *args):
        if pygame.sprite.spritecollideany(self, player_group):
            self.kill()
            self.player.collision()
        if self.arriving_phase:

            time = self.clock.tick()
            self.new_rect = [eval(f'self.new_rect[0] {self.znak} 250 * (self.speed[0]) * time / 1000'),
                             self.new_rect[1] + 250 * (self.speed[1]) * time / 1000]
            self.rect.x, self.rect.y = int(self.new_rect[0]), int(self.new_rect[1])
            if self.rect.y > self.new_coords[1]:
                self.arriving_phase = False
            if self.znak == '+' and self.rect.x > self.new_coords[0]:
                self.arriving_phase = False
            elif self.znak == '-' and self.rect.x < self.new_coords[0]:
                self.arriving_phase = False




        else:
            if pygame.sprite.spritecollideany(self, bullet_group):
                pygame.sprite.spritecollide(self, bullet_group, True)

            time = self.clock.tick()
            if self.a < 1000:
                self.a += time
            else:
                coords = self.player.get_coords()
                self.sound.play()
                Bullet(self.rect.x + 25, self.rect.y + 50, enemy_bullet_group, coords[0], coords[1])
                self.a = 0


class Shield(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('shield.png'), (30, 30))

    def __init__(self):
        super().__init__(all_sprites, shield_group)
        self.image = Shield.image
        self.rect = self.image.get_rect().move((random.randrange(30, 770), 0))
        self.timer = pygame.time.Clock()
        self.new_coord = self.rect.y

    def update(self, *args):
        time = self.timer.tick()
        if time > 1000:
            time = self.timer.tick()
        self.new_coord = self.new_coord + 100 * time / 1000
        self.rect.y = int(self.new_coord)
        if self.rect.y > 600:
            self.kill()


class HeatRemover(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('freeze.png'), (30, 30))

    def __init__(self):
        super().__init__(all_sprites, heat_remover_group)
        self.image = HeatRemover.image
        self.rect = self.image.get_rect().move((random.randrange(30, 770), 0))
        self.timer = pygame.time.Clock()

        self.new_coord = self.rect.y

    def update(self, *args):
        time = self.timer.tick()
        if time > 1000:
            time = self.timer.tick()
        self.new_coord = self.new_coord + 100 * time / 1000
        self.rect.y = int(self.new_coord)
        if self.rect.y > 600:
            self.kill()


class Heart(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('heart_bonus.png'), (30, 30))

    def __init__(self):
        super().__init__(all_sprites, bonus_hp_group)
        self.image = Heart.image
        self.rect = self.image.get_rect().move((random.randrange(30, 770), 0))
        self.timer = pygame.time.Clock()
        self.new_coord = self.rect.y

    def update(self, *args):
        time = self.timer.tick()
        if time > 1000:
            time = self.timer.tick()
        self.new_coord = self.new_coord + 100 * time / 1000
        self.rect.y = int(self.new_coord)
        if self.rect.y > 600:
            self.kill()


start_screen()
screen = pygame.display.set_mode((800, 600))
hp = pygame.transform.scale(load_image('hp.png'), (100, 100))
screen.blit(hp, (0, 600))
background = pygame.transform.scale(load_image('download.jpg'), (1920, 2500))
screen.blit(background, (0, -1250))
pygame.display.flip()

new_coord = -1250
player = Player()
Enemy(player)
all_sprites.draw(screen)
pygame.display.flip()
clock = pygame.time.Clock()
spawn_clock = pygame.time.Clock()
running = True
pygame.mixer.pre_init(16500, -16, 2, 2048)
music = pygame.mixer.Sound(os.path.join('data', 'back_music.wav'))
music.play(-1)
timer = 0
global_timer = 0
font = pygame.font.Font(None, 100)
bonus_timer = 0
while running:
    screen.blit(hp, (0, 600))
    if player not in all_sprites:
        game_over()
        all_sprites.empty()
        player_group.empty()
        enemy_group.empty()
        bullet_group.empty()
        enemy_bullet_group.empty()
        shield_group.empty()
        heat_remover_group.empty()
        bonus_hp_group.empty()
        player = Player()
        screen = pygame.display.set_mode((800, 600))
        timer = 0
        global_timer = 0
        spawn_clock.tick()
    time = spawn_clock.tick()
    timer += time
    global_timer += time
    bonus_timer += time
    if timer > 3000:
        timer = 0
        Enemy(player)
    if bonus_timer > 15000:
        bonus_timer = 0
        random_bonus()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == 27:
            if not pause_screen():
                all_sprites.empty()
                player_group.empty()
                enemy_group.empty()
                bullet_group.empty()
                enemy_bullet_group.empty()
                shield_group.empty()
                heat_remover_group.empty()
                bonus_hp_group.empty()
                player = Player()
                timer = 0
                global_timer = 0
            spawn_clock.tick()
            clock.tick()
            screen = pygame.display.set_mode((800, 600))
            bullet_group.update(True)
            clock.tick()

        player_group.update(event)
    all_sprites.draw(screen)
    all_sprites.update()
    for i in range(player.get_hp()):
        screen.blit(hp, (i * 60, 500))
    if player.get_heat() < 90:
        color = (255, 255, 255)

    else:
        color = (255, 0, 0)
    pygame.draw.rect(screen, color, (20, 490, int(player.get_heat()) * 1.6, 20))
    text = font.render(str(global_timer), 1, (74, 13, 78))
    screen.blit(text, (300, 10))
    pygame.display.flip()
    if new_coord > 0:
        screen.blit(background, (0, -1250))
        new_coord = -1250
    new_coord += 30 * clock.tick() / 1000
    screen.blit(background, (0, int(new_coord)))
