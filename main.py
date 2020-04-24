# Snake game with Pygame 1.9.6, March 2020 Kerman
# Game music: Snake charmer, Created by Erich Izdepski
# Menu music: Loading screen loop, by Brandon Morris
# Sound effects: bfxr.net
import pygame as pg
from os import path, environ
from settings import *
from sprites import *

environ['SDL_VIDEO_CENTERED'] = '1'


class Game():
    def __init__(self):
        self.playing = False
        self.running = True
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("SNAKE")
        self.font_name = pg.font.match_font("arial")
        self.clock = pg.time.Clock()
        self.score = 0
        self.dir = path.dirname(__file__)

        # see if highscore file exists, if not create it
        self.file_exist = "r+" if path.isfile(path.join(self.dir, HS_FILE)) else "w"
        with open(path.join(self.dir, HS_FILE), self.file_exist) as f:
            try:
                self.highscore = int(f.read())
            except (IOError, ValueError):
                self.highscore = 0

        # load the sounds and images
        self.snd_dir = path.join(self.dir, "snd")
        self.img_dir = path.join(self.dir, "img")
        self.icon = pg.image.load(path.join(self.img_dir, "icon.png")).convert_alpha()
        pg.display.set_icon(self.icon)
        self.eat_sound = pg.mixer.Sound(path.join(self.snd_dir, "Eat.wav"))
        self.eat_sound.set_volume(0.5)
        self.death_sound = pg.mixer.Sound(path.join(self.snd_dir, "Death.wav"))
        self.death_sound.set_volume(0.5)
        self.pause_font = path.join(self.img_dir, "Pause.ttf")

    def new(self):
        self.paused = False
        self.food = False
        self.food_timer = pg.time.get_ticks()
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.foods = pg.sprite.Group()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 120))
        Wall(self, 0, 0)
        Wall(self, 0, WIDTH - 10)
        self.snake = Player(self)
        pg.mixer.music.load(path.join(self.snd_dir, "snakecharmer.ogg"))
        self.run()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.15)
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()

        # check for collision of head with walls
        hit = pg.sprite.spritecollide(self.snake.parts[0], self.walls, False)
        if hit:
            self.death_sound.play()
            self.playing = False

        # check for collision of head with body
        hitb = pg.sprite.spritecollide(self.snake.parts[0], self.snake.parts[1:], False)
        if hitb:
            self.death_sound.play()
            self.playing = False

        # check for collision of head with food
        hitf = pg.sprite.spritecollide(self.snake.parts[0], self.foods, True)
        if hitf:
            self.eat_sound.play()
            self.food = False
            self.score += 10
            self.food_timer = pg.time.get_ticks()
            self.snake.add_part()

        self.snake.updatehead()

        # check if time to spawn new food
        if pg.time.get_ticks() - self.food_timer > 2000 and not self.food:
            self.food = True
            Food(self)

    def events(self):
        # game events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.paused = not self.paused
                # can quit game with Escape
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        # draw the score
        self.draw_text(str(self.score), 28, BRIGHT_RED, 40, 10)
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", 80, BRIGHT_RED, WIDTH / 2, HEIGHT / 2, self.pause_font)
        # flip the display
        pg.display.flip()

    def start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "TremLoadingloopl.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        self.screen.fill(MID_RED)
        if self.highscore > 0:
            self.draw_text("Current high score: {}".format(self.highscore), 25, BLACK, WIDTH / 2, HEIGHT / 4, TIMES)
        self.draw_text("The classical game of", 45, BLACK, WIDTH / 2, HEIGHT / 2 - 55, GABRIOLA)
        self.draw_text("SNAKE", 65, BLACK, WIDTH / 2, HEIGHT / 2 - 20, GABRIOLA)
        self.draw_text("Use arrow keys to move", 25, BLACK, WIDTH / 2, 3 * HEIGHT / 4)
        self.draw_text("Press any key to start!", 25, BLACK, WIDTH / 2, 4 * HEIGHT / 5)
        self.draw_text("Press 'P' to pause the game", 25, BLACK, WIDTH / 2, 6 * HEIGHT / 7)
        pg.display.flip()
        self.wait_for_key()

    def game_over_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, "TremLoadingloopl.ogg"))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.3)
        self.playing = False
        self.screen.fill(MID_RED)
        if not self.running:
            return None
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("New high score!", 25, BLACK, WIDTH / 2, HEIGHT / 4 + 25, TIMES)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("High score: {}".format(self.highscore), 25, BLACK, WIDTH / 2, HEIGHT / 4 + 25, TIMES)
        self.draw_text("Your score: {}".format(self.score), 25, BLACK, WIDTH / 2, HEIGHT / 4, TIMES)
        self.draw_text("GAME OVER", 65, BLACK, WIDTH / 2, HEIGHT / 2 - 25, GABRIOLA)
        self.draw_text("Press any key to play again!", 25, BLACK, WIDTH / 2, 4 * HEIGHT / 5)
        pg.display.flip()
        self.wait_for_key()

    def draw_text(self, text, size, color, x, y, font=None):
        if font == None:
            font = self.font_name
        font = pg.font.Font(font, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        pause_time = pg.time.get_ticks()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN and pg.time.get_ticks() - pause_time > 500:
                    waiting = False
                    pg.mixer.music.fadeout(500)


g = Game()
g.start_screen()
while g.running:
    g.new()
    g.game_over_screen()

pg.quit()
