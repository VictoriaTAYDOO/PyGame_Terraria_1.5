import os
import sys

import pygame

pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
FPS = 100
clock = pygame.time.Clock()


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


all_sprites = pygame.sprite.Group()


def load_level_1():
    pygame.mixer.music.load('data/boss1.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level1.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = fldown = False
    jump = False
    jumpCount = 0
    jumpMax = 15
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    fldown = True
                elif not jump and event.key == pygame.K_SPACE:
                    jump = True
                    jumpCount = jumpMax
                elif event.key == pygame.K_w:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    flLeft = flRight = flup = fldown = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and not jump:
            player.rect.y -= 10
        elif fldown:
            player.rect.y += 10
        if jump:
            player.rect.y -= jumpCount
            if jumpCount > -jumpMax:
                jumpCount -= 2
            else:
                jump = False

        screen.blit(level, (0, 0))
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
    flLeft = flRight = flup = fldown = False
    jump = False
    jumpCount = 0
    jumpMax = 15
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    fldown = True
                elif not jump and event.key == pygame.K_SPACE:
                    jump = True
                    jumpCount = jumpMax
                elif event.key == pygame.K_w:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    flLeft = flRight = flup = fldown = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and not jump:
            player.rect.y -= 10
        elif fldown:
                player.rect.y += 10
        if jump:
            player.rect.y -= jumpCount
            if jumpCount > -jumpMax:
                jumpCount -= 2
            else:
                jump = False
        screen.blit(level, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(10)
        pygame.display.flip()


def load_level_3():
    pygame.mixer.music.load('data/boss3.mp3')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level3.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = fldown = False
    jump = False
    jumpCount = 0
    jumpMax = 15
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    fldown = True
                elif not jump and event.key == pygame.K_SPACE:
                    jump = True
                    jumpCount = jumpMax
                elif event.key == pygame.K_w:
                    flup = True
                elif event.key == pygame.K_a:
                    flLeft = True
                elif event.key == pygame.K_d:
                    flRight = True
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    flLeft = flRight = flup = fldown = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and not jump:
            player.rect.y -= 10
        elif fldown:
                player.rect.y += 10
        if jump:
            player.rect.y -= jumpCount
            if jumpCount > -jumpMax:
                jumpCount -= 2
            else:
                jump = False
        screen.blit(level, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(10)
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