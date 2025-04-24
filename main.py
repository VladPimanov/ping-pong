import pygame
import random
import time

pygame.init()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE )
pygame.display.set_caption("ping pong")

HEIGHT = surface.get_height()
WIDTH = surface.get_width()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

players_HEIGHT = 80
players_WIDTH = 10
ball_radius = 15

x_first_start_position = 0
y_first_start_position = HEIGHT // 2 - players_HEIGHT

x_second_start_position = WIDTH - players_WIDTH
y_second_start_position = HEIGHT // 2 - players_HEIGHT

x_ball_start_position = WIDTH // 2
y_ball_start_position = HEIGHT // 2 - ball_radius * 2

x_first_position = 0
y_first_position = HEIGHT // 2 - players_HEIGHT

x_second_position = WIDTH - players_WIDTH
y_second_position = HEIGHT // 2 - players_HEIGHT

x_ball_position = WIDTH // 2
y_ball_position = HEIGHT // 2 - ball_radius * 2

clock = pygame.time.Clock()
FPS = 60

players_speed = 5
tangle = random.random()
ball_speed = 3


class Ball:
    def __init__(self, start_position, ball_radius=ball_radius):
        self.ball_radius = ball_radius
        self.start_position = start_position

    def draw_ball(self, new_position=None):
        pygame.draw.circle(surface, BLUE, new_position, self.ball_radius)

    def move_to_start_position(self, start_position):
        pygame.draw.circle(surface, BLUE, start_position, self.ball_radius)


class Player:
    def __init__(self, start_position, players_size=(players_WIDTH, players_HEIGHT)):
        self.players_size = players_size
        self.start_position = start_position

    def draw_player(self, new_position=None):
        pygame.draw.rect(surface, BLACK, (new_position, self.players_size))

    def move_to_start_position(self, start_position):
        pygame.draw.rect(surface, BLACK, (start_position, self.players_size))


first_player = Player((x_first_position, y_first_position), (players_WIDTH, players_HEIGHT))
second_player = Player((x_second_position, y_second_position), (players_WIDTH, players_HEIGHT))
ball = Ball((x_ball_position, y_ball_position), ball_radius)

flagRunning = True
surface.fill(WHITE)

pygame.display.flip()

ball_right = True
ball_left = False

StartGameFlag = False


def get_start_position():
    global x_first_position, y_first_position,x_second_position,y_second_position, x_ball_position,y_ball_position,ball_speed,StartGameFlag
    first_player.move_to_start_position((x_first_start_position, y_first_start_position))
    second_player.move_to_start_position((x_second_start_position, y_second_start_position))
    ball.move_to_start_position((x_ball_start_position, y_ball_start_position))
    x_first_position, y_first_position = x_first_start_position, y_first_start_position
    x_second_position, y_second_position = x_second_start_position, y_second_start_position
    x_ball_position, y_ball_position = x_ball_start_position, y_ball_start_position
    ball_speed = 3
    StartGameFlag = False
    time.sleep(0.4)


while flagRunning:
    current_width = surface.get_width()
    current_height = surface.get_height()
    if current_width != WIDTH or current_height != HEIGHT:
        width_cef = current_width / WIDTH
        height_cef = current_height / HEIGHT

        HEIGHT = surface.get_height()
        WIDTH = surface.get_width()

        players_WIDTH *= width_cef
        players_HEIGHT *= height_cef
        x_first_start_position = x_first_position = 0
        y_first_start_position = y_first_position = HEIGHT // 2 - players_HEIGHT

        x_second_start_position = x_second_position = WIDTH - players_WIDTH
        y_second_start_position = y_second_position = HEIGHT // 2 - players_HEIGHT

        x_ball_start_position = x_ball_position = WIDTH // 2
        y_ball_start_position = y_ball_position = HEIGHT // 2 - ball_radius * 2

        players_speed *= height_cef
        ball_speed *= width_cef


        first_player.players_size = ((players_WIDTH, players_HEIGHT))
        second_player.players_size = ((players_WIDTH, players_HEIGHT))





    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            flagRunning = False

    keys = pygame.key.get_pressed()

    if any(keys):
        StartGameFlag = True
    if StartGameFlag:
        if keys[pygame.K_w] and y_first_position >= 0:
            y_first_position -= players_speed

        elif keys[pygame.K_s] and y_first_position + players_HEIGHT <= HEIGHT:
            y_first_position += players_speed

        if keys[pygame.K_UP] and y_second_position >= 0:
            y_second_position -= players_speed

        elif keys[pygame.K_DOWN] and y_second_position + players_HEIGHT <= HEIGHT:
            y_second_position += players_speed
        if y_ball_position >= HEIGHT - ball_radius or y_ball_position < 0 + ball_radius:
            tangle = -tangle
        if ball_right:

            y_ball_position += tangle
            if x_ball_position + ball_radius >= x_second_position:
                ball_speed += 0.25
                tangle = random.randint(-3, 3)
                if y_second_position + players_HEIGHT + ball_radius < y_ball_position + ball_radius or y_ball_position + ball_radius < y_second_position:
                    print('second player is lose')
                    get_start_position()

                else:
                    ball_right = False
                    ball_left = True
            else:
                x_ball_position += ball_speed

        if ball_left:
            y_ball_position += tangle
            if x_ball_position - ball_radius <= x_first_position + players_WIDTH:
                tangle = random.randint(-3, 3)
                ball_speed += 0.25
                if y_first_position + players_HEIGHT + ball_radius < y_ball_position or y_ball_position + ball_radius < y_first_position:
                    print('first player is lose')
                    get_start_position()
                else:
                    ball_right = True
                    ball_left = False

            else:
                x_ball_position -= ball_speed

    surface.fill(WHITE)
    first_player.draw_player(new_position=(x_first_position, y_first_position))
    second_player.draw_player(new_position=(x_second_position, y_second_position))
    ball.draw_ball(new_position=(x_ball_position, y_ball_position))
    pygame.display.update()

    clock.tick(FPS)

print('continue')
