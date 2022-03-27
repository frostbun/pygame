import pygame
from random import choice
from itertools import product

from color import *
from direction import Direction

class Snake():

    def __init__(self, surface, font, width=40, height=30, scale=20, snake_color=WHITE, food_color=RED, text_color=GREEN):
        self.surface = surface
        self.font = font
        self.width = width
        self.height = height
        self.scale = scale
        self.snake_color = snake_color
        self.food_color = food_color
        self.text_color = text_color
        self.reset()

    def reset(self):
        self.table = list(product(range(self.width), range(self.height)))
        self.x, self.y = choice(self.table)
        self.table.remove((self.x, self.y))
        self.body = [(self.x, self.y)]
        self.food_x, self.food_y = choice(self.table)
        self.table.remove((self.food_x, self.food_y))
        self.direction = choice(list(Direction)[:4])
        self.key_pressed = []
        self.speed = 20
        self.timer = 0

    def queue(self, key):
        if key == pygame.K_RIGHTBRACKET:
            if self.speed < 100: self.speed += 5
            return
        if key == pygame.K_LEFTBRACKET:
            if self.speed > 5: self.speed -= 5
            return
        if len(self.key_pressed) > 5: return
        self.key_pressed.append(key)

    def change_direction(self):
        if not self.key_pressed: return
        direction = Direction.from_key(self.key_pressed.pop(0))
        if not direction or direction == Direction.opposite(self.direction): return
        self.direction = direction

    def move(self, ms):
        self.timer += ms
        if self.timer < 1000/self.speed: return True
        self.timer = 0
        self.change_direction()
        match self.direction:
            case Direction.LEFT:  self.x = (self.x - 1) % self.width
            case Direction.RIGHT: self.x = (self.x + 1) % self.width
            case Direction.UP:    self.y = (self.y - 1) % self.height
            case Direction.DOWN:  self.y = (self.y + 1) % self.height
        if (self.x, self.y) in self.body: return False
        elif (self.x, self.y) == (self.food_x, self.food_y):
            self.body.append((self.x, self.y))
            self.food_x, self.food_y = choice(self.table)
            self.table.remove((self.food_x, self.food_y))
        else:
            self.table.remove((self.x, self.y))
            self.body.append((self.x, self.y))
            self.table.append(self.body.pop(0))
        return True

    def draw(self):
        for x, y in self.body: pygame.draw.rect(
            self.surface,
            self.snake_color,
            (x*self.scale, y*self.scale, self.scale, self.scale)
        )
        pygame.draw.rect(
            self.surface,
            self.food_color,
            (self.food_x*self.scale, self.food_y*self.scale, self.scale, self.scale)
        )
        point = self.font.render(f"Length: {len(self.body)}", True, self.text_color)
        speed = self.font.render(f"Speed: {self.speed}", True, self.text_color)
        self.surface.blit(point, (0, 0))
        self.surface.blit(speed, (self.width*self.scale-speed.get_width(), 0))

def game_loop():
    snake = Snake(DISPLAY, FONT, WIDTH, HEIGHT, SCALE)
    while True:
        DISPLAY.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN: snake.queue(event.key)
        snake.draw()
        fps = FONT.render(f"FPS: {CLOCK.get_fps():.0f}", True, GREEN)
        DISPLAY.blit(fps, ((WIDTH*SCALE-fps.get_width(), HEIGHT*SCALE-fps.get_height())))
        pygame.display.update()
        if not snake.move(CLOCK.tick(FPS)): snake.reset()

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Snake")
    pygame.key.set_repeat(500, 100)

    WIDTH = 40
    HEIGHT = 30
    SCALE = 20
    FPS = 60
    DISPLAY = pygame.display.set_mode((WIDTH*SCALE, HEIGHT*SCALE))
    FONT = pygame.font.SysFont("Arial", 20)
    CLOCK = pygame.time.Clock()

    game_loop()
    pygame.quit()
