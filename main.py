import pygame
import sys
import numpy as np
import math

# 1m = 10000 pixels
# 1 pixel = 0.1mm

g = 98000
FPS = 60

# initialize pygame
pygame.init()

# set up screen
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum")

# set up compile
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 1 pixel = 0.1mm
ARM_LEN = 100
ARM_WIDTH = 5


class PendulumArm(pygame.sprite.Sprite):

    def draw_line(self):
        start = (self.anchor_x, self.anchor_y)
        end_x = int(self.anchor_x + ARM_LEN * np.sin(self.angle * np.pi / 180))
        end_y = int(self.anchor_y + ARM_LEN * np.cos(self.angle * np.pi / 180))
        end = (end_x, end_y)

        pygame.draw.line(screen, self.color, start, end, ARM_WIDTH)

    def update_dynamics(self):
        accel_component = 0.5 * self.a_accel * (1/60)**2
        velo_component = self.a_velo * (1/60)
        self.last_angle = self.angle
        self.angle += accel_component + velo_component

    @property
    def a_accel(self):
        return (3 * (-1)*g * np.sin(self.angle * np.pi / 180)) / (2 * ARM_LEN)

    @property
    def a_velo(self):
        return (self.angle - self.last_angle) * FPS

    def __init__(self, x, y, angle, color=WHITE):
        super().__init__()
        self.original_image = pygame.Surface((ARM_WIDTH, ARM_LEN))
        self.original_image.fill(color)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.anchor_x = x
        self.anchor_y = y
        self.rect.top = self.anchor_y
        self.rect.centerx = self.anchor_x
        self.angle = angle
        self.last_angle = angle
        self.color = color

    def update(self):
        self.update_dynamics()
        self.draw_line()
        # self.angle += 1


all_sprites = pygame.sprite.Group()

test = PendulumArm(200, 200, 30)

all_sprites.add(test)


# Main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    all_sprites.update()

    # update the display
    pygame.display.flip()

    # cap the frame rate
    pygame.time.Clock().tick(FPS)

pygame.quit()
