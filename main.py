import os
import sys

import pygame
import math

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


def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def terminate():
    pygame.quit()
    sys.exit()


def calculate_new_xy(old_xy, speed, angle_in_radians):
    new_x = old_xy[0] + (speed * math.cos(angle_in_radians))
    new_y = old_xy[1] + (speed * math.sin(angle_in_radians))
    return new_x, new_y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, coords, direction, speed):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (coords[0], coords[1])
        self.direction = math.radians(direction)
        self.speed = speed

    def update(self):
        self.rect.center = calculate_new_xy(self.rect.center, self.speed, self.direction)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.fly_animation = []
        self.fly_animation_l = []
        self.fly_animation.append(pygame.transform.scale(load_image('fly1.png'), (107, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('fly2.png'), (107, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('fly3.png'), (107, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly1_l.png'), (107, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly2_l.png'), (107, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly3_l.png'), (107, 64)))
        self.current_im = 0
        self.image = pygame.transform.scale(load_image('hero.png'), (107, 64))
        self.rect = self.image.get_rect()
        self.rect.y = 535
        self.fly = 50
        self.is_flying = False
        self.left = False
        self.choice = 0

    def update(self):
        if self.left:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation_l):
                    self.current_im = 0
                self.image = self.fly_animation_l[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('hero_l.png'), (107, 64))
        else:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation):
                    self.current_im = 0
                self.image = self.fly_animation[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('hero.png'), (107, 64))


all_sprites = pygame.sprite.Group()


def load_level_1():
    pygame.mixer.music.load('data/boss1.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level1.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = shoot = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flup = player.is_flying = True
                elif event.key == pygame.K_a:
                    flLeft = True
                    player.left = True
                elif event.key == pygame.K_d:
                    flRight = True
                    player.left = False
                elif event.key == pygame.K_e:
                    player.choice += 1
                    if player.choice >= 3:
                        player.choice = 0
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    flLeft = flRight = False
                if event.key == pygame.K_SPACE:
                    flup = False
            if event.type == pygame.MOUSEBUTTONUP:
                if player.choice != 0:
                    shoot = True
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and player.fly > 0:
            player.rect.y -= 10
            player.fly -= 1
        elif flup and player.rect.y < 535 and player.fly == 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 535 or player.fly == 0:
            if player.rect.y + 10 < 535:
                player.rect.y += 10
            else:
                player.rect.y += 535 - player.rect.y

        if player.rect.y == 535:
            player.is_flying = False
            player.current_im = 0
            if player.left:
                player.image = pygame.transform.scale(load_image('hero_l.png'), (107, 64))
            else:
                player.image = pygame.transform.scale(load_image('hero.png'), (107, 64))
            player.fly = 50
        else:
            player.is_flying = True

        screen.blit(level, (0, 0))
        gradientRect(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('frame2.png'), (30, 90))
        gun = pygame.transform.scale(load_image('the_undertaker.png'), (46, 24))
        gun_l = pygame.transform.scale(load_image('the_undertaker_l.png'), (46, 24))
        mgun = pygame.transform.scale(load_image('megashark.png'), (70, 28))
        mgun_l = pygame.transform.scale(load_image('megashark_l.png'), (70, 28))
        bullet_im = pygame.transform.scale(load_image('bullet.png'), (20, 2))

        screen.blit(frame, (30, 20))

        all_sprites.draw(screen)
        all_sprites.update()

        if player.choice == 1:
            if player.is_flying:
                if player.left:
                    pivot = [player.rect.x + 5, player.rect.y + 40]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot:
                            offset = pygame.math.Vector2(15, 5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                            int(pivot[0] + offset.rotate(angle)[0] * 3.7), int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 20)
                            shoot = False
                    else:
                        screen.blit(gun_l, (player.rect.x - 35, player.rect.y + 20))
                        if shoot:
                            shoot = False
                else:
                    pivot = [player.rect.x + 105, player.rect.y + 40]
                    offset = pygame.math.Vector2(15, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot:
                            offset = pygame.math.Vector2(15, -5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                                            int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 20)
                            shoot = False
                    else:
                        screen.blit(gun, (player.rect.x + 100, player.rect.y + 20))
                        if shoot:
                            shoot = False
            else:
                if player.left:
                    pivot = [player.rect.x + 40, player.rect.y + 45]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot:
                            offset = pygame.math.Vector2(15, 5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                            int(pivot[0] + offset.rotate(angle)[0] * 3.7), int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 20)
                            shoot = False
                    else:
                        screen.blit(gun_l, (player.rect.x - 5, player.rect.y + 25))
                        if shoot:
                            shoot = False
                else:
                    pivot = [player.rect.x + 75, player.rect.y + 45]
                    offset = pygame.math.Vector2(15, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot:
                            offset = pygame.math.Vector2(15, -5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                                            int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 20)
                            shoot = False
                    else:
                        screen.blit(gun, (player.rect.x + 65, player.rect.y + 25))
                        if shoot:
                            shoot = False

        if player.choice == 2:
            if player.is_flying:
                if player.left:
                    pivot = [player.rect.x + 5, player.rect.y + 40]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                    else:
                        screen.blit(mgun_l, (player.rect.x - 55, player.rect.y + 20))
                else:
                    pivot = [player.rect.x + 100, player.rect.y + 40]
                    offset = pygame.math.Vector2(25, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                    else:
                        screen.blit(mgun, (player.rect.x + 90, player.rect.y + 20))
            else:
                if player.left:
                    pivot = [player.rect.x + 40, player.rect.y + 45]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                    else:
                        screen.blit(mgun_l, (player.rect.x - 5, player.rect.y + 25))
                else:
                    pivot = [player.rect.x + 75, player.rect.y + 45]
                    offset = pygame.math.Vector2(15, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                    else:
                        screen.blit(mgun, (player.rect.x + 65, player.rect.y + 25))

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