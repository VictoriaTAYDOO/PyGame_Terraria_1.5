import os
import sys

import pygame

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
FPS = 100
clock = pygame.time.Clock()


def gradientRect(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.hero_im = load_image("hero.png")
        self.image = self.hero_im
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 550
        self.fly = 50


all_sprites = pygame.sprite.Group()


def load_level_1():
    pygame.mixer.music.load('data/boss1.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level1.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    flLeft = flRight = False
                if event.key == pygame.K_SPACE:
                    flup = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and player.fly > 0:
            player.rect.y -= 10
            player.fly -= 1
        elif flup and player.rect.y < 550 and player.fly == 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 550 or player.fly == 0:
            if player.rect.y + 10 < 550:
                player.rect.y += 10
            else:
                player.rect.y += 550 - player.rect.y

        if player.rect.y == 550:
            player.fly = 50

        screen.blit(level, (0, 0))
        gradientRect(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('frame2.png'), (30, 90))
        screen.blit(frame, (30, 20))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(15)
        pygame.display.flip()


def load_level_2():
    pygame.mixer.music.load('data/boss2.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level2.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    flLeft = flRight = False
                if event.key == pygame.K_SPACE:
                    flup = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and player.fly > 0:
            player.rect.y -= 10
            player.fly -= 1
        elif flup and player.rect.y < 550 and player.fly == 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 550 or player.fly == 0:
            if player.rect.y + 10 < 550:
                player.rect.y += 10
            else:
                player.rect.y += 550 - player.rect.y

        if player.rect.y == 550:
            player.fly = 50

        screen.blit(level, (0, 0))
        gradientRect(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('frame2.png'), (30, 90))
        screen.blit(frame, (30, 20))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(15)
        pygame.display.flip()


def load_level_3():
    pygame.mixer.music.load('data/boss3.mp3')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level3.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    flLeft = flRight = False
                if event.key == pygame.K_SPACE:
                    flup = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and player.fly > 0:
            player.rect.y -= 10
            player.fly -= 1
        elif flup and player.rect.y < 550 and player.fly == 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 550 or player.fly == 0:
            if player.rect.y + 10 < 550:
                player.rect.y += 10
            else:
                player.rect.y += 550 - player.rect.y

        if player.rect.y == 550:
            player.fly = 50

        screen.blit(level, (0, 0))
        gradientRect(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('frame2.png'), (30, 90))
        screen.blit(frame, (30, 20))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(15)
        pygame.display.flip()


def start_screen():
    play = pygame.transform.scale(load_image('play.png'), (300, 100))
    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    screen.blit(play, (350, 300))
    pygame.mixer.music.load('data/title.ogg')
    pygame.mixer.music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 350 < pygame.mouse.get_pos()[0] < 650 and 300 < pygame.mouse.get_pos()[1] < 400:
                    level_menu_screen()
        pygame.display.flip()


def level_menu_screen():
    easy = pygame.transform.scale(load_image('easy.png'), (150, 150))
    medium = pygame.transform.scale(load_image('medium.png'), (150, 150))
    hard = pygame.transform.scale(load_image('hard.png'), (150, 150))
    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    screen.blit(easy, (200, 250))
    screen.blit(medium, (425, 250))
    screen.blit(hard, (650, 250))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 200 < pygame.mouse.get_pos()[0] < 350 and 250 < pygame.mouse.get_pos()[1] < 400:
                    pygame.mixer.music.stop()
                    load_level_1()
                elif 425 < pygame.mouse.get_pos()[0] < 575 and 250 < pygame.mouse.get_pos()[1] < 400:
                    pygame.mixer.music.stop()
                    load_level_2()
                elif 650 < pygame.mouse.get_pos()[0] < 800 and 250 < pygame.mouse.get_pos()[1] < 400:
                    pygame.mixer.music.stop()
                    load_level_3()
        pygame.display.flip()


start_screen()
level_menu_screen()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color("white"))
    all_sprites.draw(screen)
    all_sprites.update()
    clock.tick(10)
    pygame.display.flip()

pygame.quit()