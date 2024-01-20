import os
import sys

import pygame
import math

pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
FPS = 100
clock = pygame.time.Clock()


def collideBullets(foe, bullets):
    center = (foe.rect.x + 74, foe.rect.y + 109)
    for bullet in bullets:
        if center[0] - 52 <= bullet.rect.x <= center[0] + 52 and center[1] - 52 <= bullet.rect.y <= center[1] + 52:
            foe.health -= bullet.damage
            bullet.kill()


def gradientRect_vertical(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (1, 0))
    pygame.draw.line(colour_rect, right_colour, (0, 1), (1, 1))
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))
    window.blit(colour_rect, target_rect)


def gradientRect_horizontal(window, left_colour, right_colour, target_rect):
    colour_rect = pygame.Surface((2, 2))
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))
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
    def __init__(self, image, coords, direction, speed, damage, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (coords[0], coords[1])
        self.direction = math.radians(direction)
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.center = calculate_new_xy(self.rect.center, self.speed, self.direction)


class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.fly_animation = []
        self.fly_animation_l = []
        self.fly_animation.append(pygame.transform.scale(load_image('fly/fly1.png'), (173, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('fly/fly2.png'), (173, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('fly/fly3.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly/fly1_l.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly/fly2_l.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('fly/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = pygame.transform.scale(load_image('fly/hero.png'), (173, 64))
        self.rect = self.image.get_rect()
        self.rect.y = 635
        self.fly = 50
        self.is_flying = False
        self.left = False
        self.choice = 0
        self.gun_is_ready = 15
        self.mgun_is_ready = 5

    def update(self):
        if self.left:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation_l):
                    self.current_im = 0
                self.image = self.fly_animation_l[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('fly/hero_l.png'), (173, 64))
        else:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation):
                    self.current_im = 0
                self.image = self.fly_animation[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('fly/hero.png'), (173, 64))


class Foe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.animation = []
        self.attack_animation = []
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_1.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_2.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_3.png'), (150, 166)))
        self.attack_animation.append(pygame.transform.scale(load_image('fly/fly1_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('fly/fly2_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('fly/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = pygame.transform.scale(load_image('eoc_anim/eoc1_1.png'), (150, 166))
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.rect.x = 400
        self.attack = False
        self.health = 70

    def update(self):
        if self.attack:
            pass
        else:
            self.current_im += 1
            if self.current_im >= len(self.animation):
                self.current_im = 0
            self.image = self.animation[int(self.current_im)]


bullets1 = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_level_1():
    pygame.mixer.music.load('data/boss1.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('level1.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = shoot = False
    boss = Foe()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.choice != 0:
                    shoot = True
            elif event.type == pygame.MOUSEBUTTONUP:
                shoot = False
        if flLeft:
            player.rect.x -= 10
        elif flRight:
            player.rect.x += 10
        if flup and player.fly > 0:
            player.rect.y -= 10
            player.fly -= 0.8
        elif flup and player.rect.y < 635 and player.fly <= 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 635 or player.fly <= 0:
            if player.rect.y + 10 < 635:
                player.rect.y += 10
            else:
                player.rect.y += 635 - player.rect.y

        if player.rect.y == 635:
            player.is_flying = False
            player.current_im = 0
            if player.left:
                player.image = pygame.transform.scale(load_image('fly/hero_l.png'), (173, 64))
            else:
                player.image = pygame.transform.scale(load_image('fly/hero.png'), (173, 64))
            player.fly = 50
        else:
            player.is_flying = True

        screen.blit(level, (0, 0))

        gradientRect_vertical(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('frame2.png'), (30, 90))

        if boss.health > 0:
            gradientRect_horizontal(screen, (255, 172, 93), (139, 0, 0),
                                    pygame.Rect(boss.rect.x + 74 - 35, boss.rect.y + 109 + 62, 70, 10))
            pygame.draw.rect(screen, (0, 0, 0), (boss.rect.x + 74 - 35, boss.rect.y + 109 + 62, int(70 - boss.health), 10))

        gun = pygame.transform.scale(load_image('the_undertaker.png'), (46, 24))
        gun_l = pygame.transform.scale(load_image('the_undertaker_l.png'), (46, 24))
        mgun = pygame.transform.scale(load_image('megashark.png'), (70, 28))
        mgun_l = pygame.transform.scale(load_image('megashark_l.png'), (70, 28))
        bullet_im = pygame.transform.scale(load_image('bullet.png'), (20, 2))
        screen.blit(frame, (30, 20))
        all_sprites.draw(screen)
        all_sprites.update()
        bullets1.draw(screen)
        bullets1.update()

        if player.choice == 1:
            if player.is_flying:
                if player.left:
                    pivot = [player.rect.x + 70, player.rect.y + 40]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.gun_is_ready >= 15:
                            player.gun_is_ready = 0
                            offset = pygame.math.Vector2(15, 5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 15, 3, bullets1)
                    else:
                        screen.blit(gun_l, (player.rect.x + 25, player.rect.y + 20))
                else:
                    pivot = [player.rect.x + 105, player.rect.y + 40]
                    offset = pygame.math.Vector2(15, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.gun_is_ready >= 15:
                            player.gun_is_ready = 0
                            offset = pygame.math.Vector2(15, -5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 3, bullets1)
                    else:
                        screen.blit(gun, (player.rect.x + 100, player.rect.y + 20))
            else:
                if player.left:
                    pivot = [player.rect.x + 70, player.rect.y + 45]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.gun_is_ready >= 15:
                            player.gun_is_ready = 0
                            offset = pygame.math.Vector2(15, 5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 15, 3, bullets1)
                    else:
                        screen.blit(gun_l, (player.rect.x + 27, player.rect.y + 25))
                else:
                    pivot = [player.rect.x + 105, player.rect.y + 45]
                    offset = pygame.math.Vector2(15, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(gun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.gun_is_ready >= 15:
                            player.gun_is_ready = 0
                            offset = pygame.math.Vector2(15, -5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 3, bullets1)
                    else:
                        screen.blit(gun, (player.rect.x + 100, player.rect.y + 25))

        if player.choice == 2:
            if player.is_flying:
                if player.left:
                    pivot = [player.rect.x + 70, player.rect.y + 40]
                    offset = pygame.math.Vector2(-20, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.mgun_is_ready >= 5:
                            player.mgun_is_ready = 0
                            offset = pygame.math.Vector2(20, 2)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 25, 0.7, bullets1)
                    else:
                        screen.blit(mgun_l, (player.rect.x + 15, player.rect.y + 20))
                else:
                    pivot = [player.rect.x + 100, player.rect.y + 40]
                    offset = pygame.math.Vector2(25, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.mgun_is_ready >= 5:
                            player.mgun_is_ready = 0
                            offset = pygame.math.Vector2(20, -5)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.7, bullets1)
                    else:
                        screen.blit(mgun, (player.rect.x + 90, player.rect.y + 20))
            else:
                if player.left:
                    pivot = [player.rect.x + 80, player.rect.y + 50]
                    offset = pygame.math.Vector2(-30, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x <= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun_l, angle + 180, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.mgun_is_ready >= 5:
                            player.mgun_is_ready = 0
                            offset = pygame.math.Vector2(20, 2)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                            angle, 25, 0.7, bullets1)
                    else:
                        screen.blit(mgun_l, (player.rect.x + 15, player.rect.y + 25))
                else:
                    pivot = [player.rect.x + 100, player.rect.y + 48]
                    offset = pygame.math.Vector2(25, -10)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= pivot[0]:
                        rel_x, rel_y = mouse_x - pivot[0], mouse_y - pivot[1]
                        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))
                        rotated_image, rect = rotate(mgun, angle, pivot, offset)
                        screen.blit(rotated_image, rect)
                        if shoot and player.mgun_is_ready >= 5:
                            player.mgun_is_ready = 0
                            offset = pygame.math.Vector2(20, -1)
                            rotated_image, a = rotate(bullet_im, angle, pivot, offset)
                            bullet = Bullet(rotated_image, (
                                int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.7, bullets1)
                    else:
                        screen.blit(mgun, (player.rect.x + 90, player.rect.y + 25))
        if boss.health <= 0:
            boss.kill()
        player.gun_is_ready += 1
        player.mgun_is_ready += 1
        clock.tick(15)
        collideBullets(boss, bullets1)
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
        gradientRect_horizontal(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
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
        gradientRect_horizontal(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
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
    screen.blit(play, (440, 300))
    pygame.mixer.music.load('data/title.ogg')
    pygame.mixer.music.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 440 < pygame.mouse.get_pos()[0] < 740 and 300 < pygame.mouse.get_pos()[1] < 400:
                    level_menu_screen()
        pygame.display.flip()


def level_menu_screen():
    easy = pygame.transform.scale(load_image('easy.png'), (150, 150))
    medium = pygame.transform.scale(load_image('medium.png'), (150, 150))
    hard = pygame.transform.scale(load_image('hard.png'), (150, 150))
    fon = pygame.transform.scale(load_image('fon.jpg'), (size))
    back = pygame.transform.scale(load_image('back.png'), (120, 60))
    screen.blit(fon, (0, 0))
    screen.blit(easy, (300, 300))
    screen.blit(medium, (525, 300))
    screen.blit(hard, (750, 300))
    screen.blit(back, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 300 < pygame.mouse.get_pos()[0] < 450 and 300 < pygame.mouse.get_pos()[1] < 450:
                    pygame.mixer.music.stop()
                    load_level_1()
                elif 525 < pygame.mouse.get_pos()[0] < 675 and 300 < pygame.mouse.get_pos()[1] < 450:
                    pygame.mixer.music.stop()
                    load_level_2()
                elif 750 < pygame.mouse.get_pos()[0] < 900 and 300 < pygame.mouse.get_pos()[1] < 450:
                    pygame.mixer.music.stop()
                    load_level_3()
                elif 0 < pygame.mouse.get_pos()[0] < 120 and 0 < pygame.mouse.get_pos()[1] < 60:
                    start_screen()
        pygame.display.flip()


start_screen()
level_menu_screen()
pygame.quit()