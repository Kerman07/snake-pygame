# sprites for snake, walls and food
import pygame as pg
import random
from settings import *
from os import path
from itertools import chain


# class that represents a single part of the snake
class Part(pg.sprite.Sprite):
    def __init__(self, game, center):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(self.game.img_dir, "part.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.vx, self.vy = 0, 0


# class to organize and hold different parts of snake
class Player(Part):
    def __init__(self, game):
        self.game = game
        self.positions = [[60, HEIGHT / 2 - 10], [40, HEIGHT / 2 - 10], [20, HEIGHT / 2 - 10]]
        self.parts = []
        # initialize the snake with 3 parts, at the mid left corner of screen
        self.placx, self.placy = 50, HEIGHT / 2
        for pos in self.positions:
            self.parts.append(Part(self.game, pos))
        self.last_move = "right"
        self.tail_pos = None

    def updatehead(self):
        # moving the head, prevent head moving back onto body with last_move
        dirs = {"right": [1, 0], "left": [-1, 0], "up": [0, -1], "down": [0, 1]}
        head = self.parts[0]
        head.vx, head.vy = [5 * i for i in dirs[self.last_move]]
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and "left" != self.last_move:
            self.last_move = "right"
            head.vx = 5
        if keys[pg.K_LEFT] and "right" != self.last_move:
            self.last_move = "left"
            head.vx = -5
        if keys[pg.K_DOWN] and "up" != self.last_move:
            self.last_move = "down"
            head.vy = 5
        if keys[pg.K_UP] and "down" != self.last_move:
            self.last_move = "up"
            head.vy = -5
        self.placx += head.vx
        self.placy += head.vy

        # only move snake if the position has changed exactly the length of one part
        if abs(self.placx - self.positions[0][0]) >= 20 or abs(self.placy - self.positions[0][1]) >= 20:
            if abs(self.placx - self.positions[0][0]) == 20:
                head.rect.centerx += self.placx - self.positions[0][0]
                self.placx = head.rect.centerx
                self.placy = self.positions[0][1]
            elif abs(self.placy - self.positions[0][1]) == 20:
                head.rect.centery += self.placy - self.positions[0][1]
                self.placx = self.positions[0][0]
                self.placy = head.rect.centery
            # allow movement of snake across the screen on y-axis
            if head.rect.centery >= HEIGHT + 10:
                head.rect.centery = 10
                self.placy = 10
            if head.rect.centery <= -10:
                head.rect.centery = HEIGHT - 10
                self.placy = HEIGHT - 10
            # pop the tail of the snake, insert new head position to front
            self.tail_pos = self.positions.pop()
            self.positions.insert(0, [*head.rect.center])
            self.updatebody()

    def updatebody(self):
        # snake body just moves one position over
        for i, part in enumerate(self.parts[1:]):
            part.rect.center = self.positions[i + 1]

    def add_part(self):
        # add the part to the end of the snake
        self.parts.append(Part(self.game, self.tail_pos))
        self.positions.append(self.tail_pos)


class Wall(pg.sprite.Sprite):
    def __init__(self, game, top, left):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((10, HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left


class Food(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = FOOD_LAYER
        self.groups = game.all_sprites, game.foods
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()

        # make sure to not spawn food on top of snake
        snakexpos = set([arr[0] for arr in self.game.snake.positions])
        snakeypos = set([arr[1] for arr in self.game.snake.positions])
        x = random.randrange(20, WIDTH, 20)
        while x in snakexpos:
            x = random.randrange(20, WIDTH, 20)
        y = random.randrange(10, HEIGHT, 20)
        while y in snakeypos:
            y = random.randrange(10, HEIGHT, 20)
        self.rect.center = (x, y)
        self.timer = pg.time.get_ticks()
        self.blink = False
        self.blink_alpha = chain(BLINK_ALPHA * 2)

    def update(self):
        # periodically change the image of food 
        if pg.time.get_ticks() - self.timer > 100 and self.blink:
            self.timer = pg.time.get_ticks()
            self.image.fill(YELLOW)
            self.blink = False

        elif pg.time.get_ticks() - self.timer > 800 and not self.blink:
            try:
                self.image.fill((0, 0, 0, next(self.blink_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except StopIteration:
                self.timer = pg.time.get_ticks()
                self.blink = True
                self.blink_alpha = chain(BLINK_ALPHA * 2)
