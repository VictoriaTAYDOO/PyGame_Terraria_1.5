import os
import sys
import random
import pygame
import math

pygame.init()
size = width, height = 1200, 700
screen = pygame.display.set_mode(size)
FPS = 100
clock = pygame.time.Clock()
with open('score.txt', 'w') as fil:
    fil.write('0')
with open('all_score.txt', 'w') as file:
    file.write('all score: 0')


def collideBullets(foe, bullets):
    center = (foe.rect.x + 74, foe.rect.y + 109)
    for bullet in bullets:
        if center[0] - 52 <= bullet.rect.x <= center[0] + 52 and center[1] - 52 <= bullet.rect.y <= center[1] + 52:
            foe.health -= bullet.damage
            bullet.kill()


def collideServants(hero_rect, servants):
    damage = 0
    for servant in servants:
        center = servant.rect.center
        if hero_rect.x + 75 <= center[0] <= hero_rect.x + 100 and hero_rect.y <= center[1] <= hero_rect.y + 60:
            servant.kill()
            damage = 1
    return damage


def collide(rect_x, rect_y, hero):
    center = (rect_x + 74, rect_y + 109)
    if center[0] - 52 <= hero.rect.x + 90 <= center[0] + 52 and center[1] - 52 <= hero.rect.y <= center[1] + 52:
        return True
    return False


def collidePoint(rect_x, rect_y, hero):
    center = (rect_x + 74, rect_y + 109)
    if center[0] - 52 <= hero.rect.x <= center[0] + 52 and center[1] - 52 <= hero.rect.y <= center[1] + 52:
        return True
    return False


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


class Servant(pygame.sprite.Sprite):
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
        self.fly_animation.append(pygame.transform.scale(load_image('player/fly1.png'), (173, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('player/fly2.png'), (173, 64)))
        self.fly_animation.append(pygame.transform.scale(load_image('player/fly3.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('player/fly1_l.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('player/fly2_l.png'), (173, 64)))
        self.fly_animation_l.append(pygame.transform.scale(load_image('player/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = pygame.transform.scale(load_image('player/hero.png'), (173, 64))
        self.rect = self.image.get_rect()
        self.rect.y = 635
        self.fly = 50
        self.is_flying = False
        self.left = False
        self.choice = 0
        self.gun_is_ready = 15
        self.mgun_is_ready = 5
        self.health = 100
        self.timer = 0

    def update(self):
        if self.left:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation_l):
                    self.current_im = 0
                self.image = self.fly_animation_l[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('player/hero_l.png'), (173, 64))
        else:
            if self.is_flying:
                self.current_im += 0.6
                if self.current_im >= len(self.fly_animation):
                    self.current_im = 0
                self.image = self.fly_animation[int(self.current_im)]
            else:
                self.image = pygame.transform.scale(load_image('player/hero.png'), (173, 64))


class InvisHero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('player/hero.png'), (1, 1))
        self.rect = self.image.get_rect()
        self.rect.y = 635
        self.fly = 50


class Foe(pygame.sprite.Sprite):
    def __init__(self, hero, speed, servants):
        super().__init__(all_sprites)
        self.animation = []
        self.attack_animation = []
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_1.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_2.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('eoc_anim/eoc1_3.png'), (150, 166)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly1_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly2_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = self.animation[int(self.current_im)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1300)
        self.rect.y = -200
        self.here = False
        self.attack = False
        self.health = 70
        self.hero = hero
        self.speed = speed
        self.ready = 0
        self.servant = 0
        self.ram = False
        self.servants = servants

    def update(self):
        cx, cy = (self.hero.rect.x + 30, self.hero.rect.y - 300)
        dx, dy = cx - self.rect.x, cy - self.rect.y
        dist1 = math.hypot(abs(self.hero.rect.x + 90 - self.rect.x - 74), abs(self.hero.rect.y + 5 - self.rect.y - 109))
        offset = pygame.math.Vector2(0, 0)
        pivot = [self.rect.x + 90, self.rect.y + 10]
        rel_x, rel_y = self.hero.rect.x - pivot[0], self.hero.rect.y - pivot[1]
        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if self.attack:
            pass
        else:
            self.current_im += 1
            if self.current_im >= len(self.animation):
                self.current_im = 0
            self.image = self.animation[int(self.current_im)]
        if dist1 <= 300:
            self.ready += 1
        if self.servant == 3 and self.ready >= 50 and dist1 <= 300:
            self.ram = True
            self.hx = self.hero.rect.x + 90
            self.hy = self.hero.rect.y + 10
            self.point = InvisHero()
            self.point.rect.x = self.hx
            self.point.rect.y = self.hy
            self.ready = -30
            self.servant = 0
        if self.ram:
            if abs(self.hx - self.rect.x - 74) > 0 or abs(self.hy - self.rect.y - 109) > 0:
                dist = math.hypot(self.hx - self.rect.x, self.hy - self.rect.y)
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
            if collidePoint(self.rect.x, self.rect.y, self.point) or collide(self.rect.x, self.rect.y, self.hero):
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
                self.ram = False
                self.point.kill()

        self.image, rect = rotate(self.image, angle - 100, pivot, offset)

        if self.ready >= 15 and dist1 <= 300:
            if self.servant < 3:
                pivot = [self.rect.x + 74, self.rect.y + 109]
                offset = pygame.math.Vector2(0, 15)
                self.servant += 1
                ser = pygame.transform.scale(load_image('eoc_anim/ser_of_ct.png'), (20, 30))
                ser_img, rect = rotate(ser, angle - 100, pivot, offset)
                servant = Servant(ser_img, (
                    int(pivot[0] + offset.rotate(angle - 100)[0] * 3.7),
                    int(pivot[1] + offset.rotate(angle - 100)[1] * 3.7)),
                                  angle - 20, 10, 2, self.servants)
                self.ready = 0

        if self.rect.x != self.hero.rect.x + 30 or self.rect.y != self.hero.rect.y - 300:
            self.here = False

        if not self.here:
            if abs(dx) > 0 or abs(dy) > 0:
                dist = math.hypot(dx, dy)
                self.rect.x += min(dist, self.speed) * dx / dist
                self.rect.y += min(dist, self.speed) * dy / dist
            if self.rect.x == self.hero.rect.x + 30 and self.rect.y == self.hero.rect.y - 300:
                self.here = True


class TwinsRet(pygame.sprite.Sprite):
    def __init__(self, hero, speed, servants):
        super().__init__(all_sprites)
        self.animation = []
        self.attack_animation = []
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_ret1_1.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_ret1_2.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_ret1_3.png'), (150, 166)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly1_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly2_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = self.animation[int(self.current_im)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1300)
        self.rect.y = -200
        self.here = False
        self.attack = False
        self.killed = False
        self.health = 70
        self.hero = hero
        self.speed = speed
        self.ready = 0
        self.servant = 0
        self.ram = False
        self.servants = servants

    def update(self):
        if self.killed:
            self.rect.y = 10000
        cx, cy = (self.hero.rect.x - 30, self.hero.rect.y - 300)
        dx, dy = cx - self.rect.x, cy - self.rect.y
        dist1 = math.hypot(abs(self.hero.rect.x + 90 - self.rect.x - 74), abs(self.hero.rect.y + 5 - self.rect.y - 109))
        offset = pygame.math.Vector2(0, 100)
        pivot = [self.rect.x + 90, self.rect.y + 10]
        rel_x, rel_y = self.hero.rect.x - pivot[0], self.hero.rect.y - pivot[1]
        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if self.attack:
            pass
        else:
            self.current_im += 1
            if self.current_im >= len(self.animation):
                self.current_im = 0
            self.image = self.animation[int(self.current_im)]
        if dist1 <= 300:
            self.ready += 1
        if self.servant == 3 and self.ready >= 50 and dist1 <= 300:
            self.ram = True
            self.hx = self.hero.rect.x + 90
            self.hy = self.hero.rect.y + 10
            self.point = InvisHero()
            self.point.rect.x = self.hx
            self.point.rect.y = self.hy
            self.ready = -30
            self.servant = 0
        if self.ram:
            if abs(self.hx - self.rect.x - 74) > 0 or abs(self.hy - self.rect.y - 109) > 0:
                dist = math.hypot(self.hx - self.rect.x, self.hy - self.rect.y)
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
            if collidePoint(self.rect.x, self.rect.y, self.point) or collide(self.rect.x, self.rect.y, self.hero):
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
                self.ram = False
                self.point.kill()

        self.image, rect = rotate(self.image, angle - 100, pivot, offset)

        if self.ready >= 15:
            if self.servant < 3:
                pivot = [self.rect.x + 74, self.rect.y + 109]
                offset = pygame.math.Vector2(30, -10)
                self.servant += 1
                ser = pygame.transform.scale(load_image('tw_anim/lazer.png'), (32, 1))
                ser_img, rect = rotate(ser, angle - 20, pivot, offset)
                servant = Servant(ser_img, (
                    int(pivot[0] + offset.rotate(angle)[0] * 3.7),
                    int(pivot[1] + offset.rotate(angle)[1] * 3.7)),
                                  angle - 20, 10, 2, self.servants)
                self.ready = 0

        if self.rect.x != self.hero.rect.x + 30 or self.rect.y != self.hero.rect.y - 300:
            self.here = False

        if not self.here:
            if abs(dx) > 0 or abs(dy) > 0:
                dist = math.hypot(dx, dy)
                self.rect.x += min(dist, self.speed) * dx / dist
                self.rect.y += min(dist, self.speed) * dy / dist
            if self.rect.x == self.hero.rect.x + 30 and self.rect.y == self.hero.rect.y - 300:
                self.here = True


class TwinsSpaz(pygame.sprite.Sprite):
    def __init__(self, hero, speed, servants):
        super().__init__(all_sprites)
        self.animation = []
        self.attack_animation = []
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_spaz1_1.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_spaz1_2.png'), (150, 166)))
        self.animation.append(pygame.transform.scale(load_image('tw_anim/tw_spaz1_3.png'), (150, 166)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly1_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly2_l.png'), (173, 64)))
        self.attack_animation.append(pygame.transform.scale(load_image('player/fly3_l.png'), (173, 64)))
        self.current_im = 0
        self.image = self.animation[int(self.current_im)]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1300)
        self.rect.y = -200
        self.here = False
        self.attack = False
        self.killed = False
        self.health = 70
        self.hero = hero
        self.speed = speed
        self.ready = 0
        self.servant = 0
        self.ram = False
        self.servants = servants

    def update(self):
        if self.killed:
            self.rect.y = 10000
        cx, cy = (self.hero.rect.x + 150, self.hero.rect.y - 300)
        dx, dy = cx - self.rect.x, cy - self.rect.y
        dist1 = math.hypot(abs(self.hero.rect.x + 90 - self.rect.x - 74), abs(self.hero.rect.y + 5 - self.rect.y - 109))
        offset = pygame.math.Vector2(0, 0)
        pivot = [self.rect.x + 90, self.rect.y + 10]
        rel_x, rel_y = self.hero.rect.x - pivot[0], self.hero.rect.y - pivot[1]
        angle = -int((180 / math.pi) * -math.atan2(rel_y, rel_x))

        if self.attack:
            pass
        else:
            self.current_im += 1
            if self.current_im >= len(self.animation):
                self.current_im = 0
            self.image = self.animation[int(self.current_im)]
        if dist1 <= 300:
            self.ready += 1
        if self.servant == 3 and self.ready >= 50 and dist1 <= 300:
            self.ram = True
            self.hx = self.hero.rect.x + 90
            self.hy = self.hero.rect.y + 10
            self.point = InvisHero()
            self.point.rect.x = self.hx
            self.point.rect.y = self.hy
            self.ready = -30
            self.servant = 0
        if self.ram:
            if abs(self.hx - self.rect.x - 74) > 0 or abs(self.hy - self.rect.y - 109) > 0:
                dist = math.hypot(self.hx - self.rect.x, self.hy - self.rect.y)
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
            if collidePoint(self.rect.x, self.rect.y, self.point) or collide(self.rect.x, self.rect.y, self.hero):
                self.rect.x += min(dist, self.speed + 40) * (self.hx - self.rect.x - 74) / dist
                self.rect.y += min(dist, self.speed + 40) * (self.hy - self.rect.y - 109) / dist
                self.ram = False
                self.point.kill()

        self.image, rect = rotate(self.image, angle - 100, pivot, offset)

        if self.ready >= 15:
            if self.servant < 3:
                pivot = [self.rect.x + 74, self.rect.y + 109]
                offset = pygame.math.Vector2(0, 15)
                self.servant += 1
                ser = pygame.transform.scale(load_image('tw_anim/cursed_flame.png'), (14, 16))
                ser_img, rect = rotate(ser, angle - 100, pivot, offset)
                servant = Servant(ser_img, (
                    int(pivot[0] + offset.rotate(angle - 100)[0] * 3.7),
                    int(pivot[1] + offset.rotate(angle - 100)[1] * 3.7)),
                                  angle - 20, 10, 2, self.servants)
                self.ready = 0

        if self.rect.x != self.hero.rect.x + 30 or self.rect.y != self.hero.rect.y - 300:
            self.here = False

        if not self.here:
            if abs(dx) > 0 or abs(dy) > 0:
                dist = math.hypot(dx, dy)
                self.rect.x += min(dist, self.speed) * dx / dist
                self.rect.y += min(dist, self.speed) * dy / dist
            if self.rect.x == self.hero.rect.x + 30 and self.rect.y == self.hero.rect.y - 300:
                self.here = True


bullets1 = pygame.sprite.Group()
bullets2 = pygame.sprite.Group()
bullets3 = pygame.sprite.Group()
servants1 = pygame.sprite.Group()
servants2 = pygame.sprite.Group()
servants3 = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


def load_level_1(sc):
    pygame.mixer.music.load('data/music/boss1.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('levels/level1.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = shoot = False
    boss = Foe(player, 7, servants1)

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
        if flLeft and player.rect.x >= -50:
            player.rect.x -= 13
        elif flRight and player.rect.x <= 1080:
            player.rect.x += 13
        if flup and player.fly > 0:
            player.rect.y -= 13
            player.fly -= 0.8
        elif flup and player.rect.y < 635 and player.fly <= 0:
            player.rect.y += 5
        elif not flup and player.rect.y < 635 or player.fly <= 0:
            if player.rect.y + 13 < 635:
                player.rect.y += 13
            else:
                player.rect.y += 635 - player.rect.y

        if player.rect.y == 635:
            player.is_flying = False
            player.current_im = 0
            if player.left:
                player.image = pygame.transform.scale(load_image('player/hero_l.png'), (173, 64))
            else:
                player.image = pygame.transform.scale(load_image('player/hero.png'), (173, 64))
            player.fly = 40
        else:
            player.is_flying = True

        a = collideServants(player.rect, servants1)
        if (collide(boss.rect.x, boss.rect.y, player) or a > 0) and player.timer > 15:
            if collide(boss.rect.x, boss.rect.y, player):
                player.health -= 20
                sc -= 200
            else:
                player.health -= 10
                sc -= 100
            player.timer = 0
        else:
            player.timer += 1

        screen.blit(level, (0, 0))

        if boss.health > 0:
            gradientRect_horizontal(screen, (255, 172, 93), (139, 0, 0),
                                    pygame.Rect(boss.rect.x + 74 - 35, boss.rect.y + 109 + 72, 70, 10))
            pygame.draw.rect(screen, (0, 0, 0),
                             (boss.rect.x + 74 - 35, boss.rect.y + 109 + 72, int(70 - boss.health), 10))

        gun = pygame.transform.scale(load_image('player/the_undertaker.png'), (46, 24))
        gun_l = pygame.transform.scale(load_image('player/the_undertaker_l.png'), (46, 24))
        mgun = pygame.transform.scale(load_image('player/megashark.png'), (70, 28))
        mgun_l = pygame.transform.scale(load_image('player/megashark_l.png'), (70, 28))
        bullet_im = pygame.transform.scale(load_image('player/bullet.png'), (20, 2))

        all_sprites.draw(screen)
        all_sprites.update()
        bullets1.draw(screen)
        bullets1.update()
        servants1.draw(screen)
        servants1.update()

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
                                            angle, 15, 2, bullets1)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 2, bullets1)
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
                                            angle, 15, 2, bullets1)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 2, bullets1)
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
                                            angle, 25, 0.6, bullets1)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.6, bullets1)
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
                                            angle, 25, 0.6, bullets1)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.6, bullets1)
                    else:
                        screen.blit(mgun, (player.rect.x + 90, player.rect.y + 25))

        gradientRect_vertical(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('levels/frame2.png'), (30, 90))
        screen.blit(frame, (30, 20))

        pygame.draw.rect(screen, (138, 9, 9),
                         (100, 50, 200, 20))
        pygame.draw.rect(screen, (0, 0, 0),
                         (100, 50, int(200 - player.health * 2), 20))

        if boss.health <= 0:
            boss.kill()
            player.kill()
            f = open('all_score.txt', 'r')
            s = int(f.readline().split()[2])
            with open('all_score.txt', 'w') as file:
                file.write(f'all score: {sc + s}')
            with open('score.txt', 'w') as fil:
                fil.write('')
                fil.write(str(sc))

            all_sprites.empty()
            all_sprites.update()
            bullets1.empty()
            bullets1.update()
            servants1.empty()
            servants1.update()
            return True
        if player.health <= 0:
            boss.kill()
            player.kill()

            all_sprites.empty()
            all_sprites.update()
            bullets1.empty()
            bullets1.update()
            servants1.empty()
            servants1.update()
            return False

        player.gun_is_ready += 1
        player.mgun_is_ready += 1
        clock.tick(15)
        collideBullets(boss, bullets1)
        pygame.display.flip()


def load_level_2(sc):
    pygame.mixer.music.load('data/music/boss2.ogg')
    pygame.mixer.music.play()
    level = pygame.transform.scale(load_image('levels/level2.png'), size)
    screen.blit(level, (0, 0))
    player = Hero()
    flLeft = flRight = flup = shoot = False
    boss1 = TwinsRet(player, 4, servants2)
    boss2 = TwinsSpaz(player, 4, servants2)
    boss2.rect.x = boss1.rect.x + 120

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
        if flLeft and player.rect.x >= -50:
            player.rect.x -= 10
        elif flRight and player.rect.x <= 1080:
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
                player.image = pygame.transform.scale(load_image('player/hero_l.png'), (173, 64))
            else:
                player.image = pygame.transform.scale(load_image('player/hero.png'), (173, 64))
            player.fly = 50
        else:
            player.is_flying = True

        a = collideServants(player.rect, servants2)
        if (collide(boss1.rect.x, boss1.rect.y, player) or collide(boss2.rect.x, boss2.rect.y,
                                                                   player) or a > 0) and player.timer > 15:
            if collide(boss1.rect.x, boss1.rect.y, player) or collide(boss2.rect.x, boss2.rect.y, player):
                player.health -= 25
                sc -= 250
            else:
                player.health -= 10
                sc -= 100
            player.timer = 0
        else:
            player.timer += 1

        screen.blit(level, (0, 0))

        if boss1.health > 0:
            gradientRect_horizontal(screen, (255, 172, 93), (139, 0, 0),
                                    pygame.Rect(boss1.rect.x + 74 - 35, boss1.rect.y + 109 + 72, 70, 10))
            pygame.draw.rect(screen, (0, 0, 0),
                             (boss1.rect.x + 74 - 35, boss1.rect.y + 109 + 72, int(70 - boss1.health), 10))

        if boss2.health > 0:
            gradientRect_horizontal(screen, (255, 172, 93), (139, 0, 0),
                                    pygame.Rect(boss2.rect.x + 74 - 35, boss2.rect.y + 109 + 72, 70, 10))
            pygame.draw.rect(screen, (0, 0, 0),
                             (boss2.rect.x + 74 - 35, boss2.rect.y + 109 + 72, int(70 - boss2.health), 10))

        gun = pygame.transform.scale(load_image('player/the_undertaker.png'), (46, 24))
        gun_l = pygame.transform.scale(load_image('player/the_undertaker_l.png'), (46, 24))
        mgun = pygame.transform.scale(load_image('player/megashark.png'), (70, 28))
        mgun_l = pygame.transform.scale(load_image('player/megashark_l.png'), (70, 28))
        bullet_im = pygame.transform.scale(load_image('player/bullet.png'), (20, 2))

        all_sprites.draw(screen)
        all_sprites.update()
        bullets2.draw(screen)
        bullets2.update()
        servants2.draw(screen)
        servants2.update()

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
                                            angle, 15, 2, bullets2)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 2, bullets2)
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
                                            angle, 15, 2, bullets2)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 15, 2, bullets2)
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
                                            angle, 25, 0.6, bullets2)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.6, bullets2)
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
                                            angle, 25, 0.6, bullets2)
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
                                int(pivot[1] + offset.rotate(angle)[1] * 3.7)), angle, 25, 0.6, bullets2)
                    else:
                        screen.blit(mgun, (player.rect.x + 90, player.rect.y + 25))

        gradientRect_vertical(screen, (141, 175, 254), (173, 103, 255), pygame.Rect(40, 45, 10, 50))
        pygame.draw.rect(screen, (0, 0, 0), (40, 45, 10, 50 - player.fly))
        frame = pygame.transform.scale(load_image('levels/frame2.png'), (30, 90))
        screen.blit(frame, (30, 20))

        pygame.draw.rect(screen, (138, 9, 9),
                         (100, 50, 200, 20))
        pygame.draw.rect(screen, (0, 0, 0),
                         (100, 50, int(200 - player.health * 2), 20))

        if boss1.health <= 0:
            boss1.killed = True
        if boss2.health <= 0:
            boss2.killed = True
        if boss1.health <= 0 and boss2.health <= 0:
            player.kill()
            boss1.kill()
            boss2.kill()
            f = open('all_score.txt', 'r')
            s = int(f.readline().split()[2])
            with open('all_score.txt', 'w') as file:
                file.write(f'all score: {sc + s}')
            with open('score.txt', 'w') as file:
                file.write(str(sc))

            all_sprites.empty()
            all_sprites.update()
            bullets2.empty()
            bullets2.update()
            servants2.empty()
            servants2.update()
            return True
        if player.health <= 0:
            boss1.kill()
            boss2.kill()
            player.kill()

            all_sprites.empty()
            all_sprites.update()
            bullets2.empty()
            bullets2.update()
            servants2.empty()
            servants2.update()
            return False

        player.gun_is_ready += 1
        player.mgun_is_ready += 1
        clock.tick(15)
        collideBullets(boss1, bullets2)
        collideBullets(boss2, bullets2)
        pygame.display.flip()


def start_screen():
    play = pygame.transform.scale(load_image('levels/play.png'), (300, 100))
    fon = pygame.transform.scale(load_image('levels/fon.jpg'), (size))
    screen.blit(fon, (0, 0))
    screen.blit(play, (440, 300))
    pygame.mixer.music.load('data/music/title.ogg')
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


def win_screen():
    im = pygame.transform.scale(load_image('levels/win.png'), (size))
    screen.blit(im, (0, 0))
    pygame.mixer.music.load('data/music/yippee-tbh.mp3')
    pygame.mixer.music.play()
    with open('score.txt', 'r') as f:
        line = f.readline()
        font = pygame.font.Font(None, 70)
        text_coord = 590
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 600
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    pygame.display.flip()
    t = pygame.time.get_ticks()
    while True:
        if pygame.time.get_ticks() - t >= 5000:
            start_screen()
            return


def lose_screen():
    im = pygame.transform.scale(load_image('levels/lose.png'), (size))
    screen.blit(im, (0, 0))
    pygame.display.flip()
    pygame.mixer.music.load('data/music/fail.mp3')
    pygame.mixer.music.play()
    t = pygame.time.get_ticks()
    while True:
        if pygame.time.get_ticks() - t >= 5000:
            start_screen()
            return


def level_menu_screen():
    easy = pygame.transform.scale(load_image('levels/easy.png'), (150, 150))
    medium = pygame.transform.scale(load_image('levels/medium.png'), (150, 150))
    fon = pygame.transform.scale(load_image('levels/fon.jpg'), (size))
    back = pygame.transform.scale(load_image('levels/back.png'), (120, 60))
    screen.blit(fon, (0, 0))
    screen.blit(easy, (400, 300))
    screen.blit(medium, (625, 300))
    screen.blit(back, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 400 < pygame.mouse.get_pos()[0] < 550 and 300 < pygame.mouse.get_pos()[1] < 450:
                    pygame.mixer.music.stop()
                    l1 = load_level_1(1000)
                    if l1:
                        win_screen()
                    else:
                        lose_screen()
                elif 625 < pygame.mouse.get_pos()[0] < 775 and 300 < pygame.mouse.get_pos()[1] < 450:
                    pygame.mixer.music.stop()
                    l2 = load_level_2(1000)
                    if l2:
                        win_screen()
                    else:
                        lose_screen()
                elif 0 < pygame.mouse.get_pos()[0] < 120 and 0 < pygame.mouse.get_pos()[1] < 60:
                    start_screen()
        pygame.display.flip()


start_screen()
level_menu_screen()
pygame.quit()
