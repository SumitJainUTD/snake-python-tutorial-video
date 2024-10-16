import json
import os
import random

import pygame
from pygame import KEYDOWN, K_UP, K_DOWN, K_RIGHT, K_LEFT, K_1, K_2, K_3, K_4, K_5, K_RETURN

SCREEN_SIZE = 800
BLOCK_WIDTH = 40


class Snake:
    def __init__(self, parent_screen, length=5):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg")
        self.x = [BLOCK_WIDTH] * self.length
        self.y = [BLOCK_WIDTH] * self.length
        self.direction = "right"

    def draw(self):
        self.parent_screen.fill((0, 0, 0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def increase(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'

    def move(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += BLOCK_WIDTH
        if self.direction == 'left':
            self.x[0] -= BLOCK_WIDTH
        if self.direction == 'up':
            self.y[0] -= BLOCK_WIDTH
        if self.direction == 'down':
            self.y[0] += BLOCK_WIDTH

        if self.x[0] >= SCREEN_SIZE:
            self.x[0] = 0

        if self.x[0] < 0:
            self.x[0] = SCREEN_SIZE

        if self.y[0] >= SCREEN_SIZE:
            self.y[0] = 0

        if self.y[0] < 0:
            self.y[0] = SCREEN_SIZE

        self.draw()


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple_img = pygame.image.load("resources/apple.jpg")
        self.x = BLOCK_WIDTH * 4
        self.y = BLOCK_WIDTH * 5

    def draw(self):
        self.parent_screen.blit(self.apple_img, (self.x, self.y))

    def move(self, snake):
        while True:  # make sure new food is not getting created over snake body
            x = random.randint(0, 19) * BLOCK_WIDTH
            y = random.randint(0, 19) * BLOCK_WIDTH
            clean = True
            for i in range(0, snake.length):
                if x == snake.x[i] and y == snake.y[i]:
                    clean = False
                    break
            if clean:
                self.x = x
                self.y = y
                return


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game - PyGame")
        self.SCREEN_UPDATE = pygame.USEREVENT
        self.timer = 150
        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)
        self.surface = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.snake = Snake(self.surface, length=56)
        self.snake.draw()
        self.apple = Apple(parent_screen=self.surface)
        self.score = 50
        self.record = 20
        self.retrieve_data()

    def play(self):
        pygame.time.set_timer(self.SCREEN_UPDATE, self.timer)
        self.snake.move()
        self.apple.draw()
        self.display_score()

        # if snake eats the apple
        if self.snake.x[0] == self.apple.x and self.snake.y[0] == self.apple.y:
            self.score += 1
            self.snake.increase()
            self.apple.move(self.snake)
            print(str(self.score))
            if self.record < self.score:
                self.record = self.score
                self.save_data()

        # if snake eats his body
        for i in range(1, self.snake.length):
            if self.snake.x[0] == self.snake.x[i] and self.snake.y[0] == self.snake.y[i]:
                print("snake will die")
                raise Exception("Collision Occurred")

    def save_data(self):
        data_folder_path = "./resources"
        file_name = "data.json"
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        complete_path = os.path.join(data_folder_path, file_name)
        data = {'record': self.record}
        with open(complete_path, 'w') as file:
            json.dump(data, file, indent=4)

    def retrieve_data(self):
        data_folder_path = os.path.join("./resources", "data.json")
        if os.path.exists(data_folder_path):
            with open(data_folder_path, 'r') as file:
                data = json.load(file)

            if data is not None:
                self.record = data['record']

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        msg = "Score: " + str(self.score) + " Record: " + str(self.record)
        scores = font.render(f"{msg}", True, (200, 200, 200))
        self.surface.blit(scores, (350, 10))

    def show_game_over(self):
        font = pygame.font.SysFont('arial', 30)
        line = font.render(f"Game over! score is {self.score}", True, (255, 255, 255))
        self.surface.blit(line, (200, 300))
        line1 = font.render(f"Press Enter to Restart", True, (255, 255, 255))
        self.surface.blit(line1, (200, 400))
        pygame.display.update()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.score = 0

    def run(self):
        running = True
        pause = False
        while running:
            # Handle Events
            for event in pygame.event.get():

                if event.type == KEYDOWN:

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_RIGHT:
                        self.snake.move_right()
                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_1:
                        self.timer = 10
                    if event.key == K_2:
                        self.timer = 50
                    if event.key == K_3:
                        self.timer = 100
                    if event.key == K_4:
                        self.timer = 150
                    if event.key == K_5:
                        self.timer = 200

                    if event.key == K_RETURN:
                        pause = False

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == self.SCREEN_UPDATE:
                    try:
                        if not pause:
                            self.play()
                    except Exception as e:
                        self.show_game_over()
                        pause = True
                        self.reset()

            # self.surface.fill((0, 0, 0))

            # update the display
            pygame.display.update()


game = Game()
game.run()
