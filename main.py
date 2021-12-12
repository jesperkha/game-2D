# Version 1.4
# Game and window handler

import pygame
pygame.init()

import imports

# Set path for imports (root)
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# PYGAME SETUP ----------------------------------------------------------------------
from config import *
clock = pygame.time.Clock()

# Display fps
font = pygame.font.SysFont("Cambria", 20)
show_fps = lambda: window.blit(font.render(f"{int(clock.get_fps())}", 0, "white"), (0, 0))

# Window and window buffer
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
window = pygame.display.set_mode((int(WIDTH * WINDOW_SCALE), int(HEIGHT * WINDOW_SCALE)))
pygame.display.set_caption(WINDOW_NAME)

buffer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
buffer_scale = [int(window.get_height() * ASPECT_RATIO), window.get_height()]
buffer_pos = [(window.get_width() - buffer.get_width()) / 2, 0]

# Window resize
def resize():
    if not FULLSCREEN:
        pygame.display.set_mode((int(WIDTH * WINDOW_SCALE), int(HEIGHT * WINDOW_SCALE)))
    else:
        pygame.display.set_mode(monitor_size, pygame.FULLSCREEN) # Fullscreen


# Game setup
setup()

# GAME LOOP --------------------------------------------------------------------------------------

fill1 = (50, 168, 82) # green
fill2 = (194, 27, 66) # red
fill3 = (99, 41, 207) # purple

# Gameloop
run = True
while run:
    clock.tick(FPS)
    buffer.fill(fill3)
    
    # True mouse pos
    x, y = pygame.mouse.get_pos()
    scale_adjustment = window.get_width() / WIDTH
    mouse.x = x / scale_adjustment
    mouse.y = y / scale_adjustment

    # Game loop function 
    loop(buffer, clock.get_time())

    # PYGAME EVENT HANDLERS ----------------------------------------------------------------------

    # Pygame events
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        
        # Toggle fullscreen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            FULLSCREEN = not FULLSCREEN
            resize()

        # Window resize
        if event.type == pygame.VIDEORESIZE:
            resize()


    # PYGAME WINDOW MANAGEMENT --------------------------------------------------------------------

    # Window resize and buffer drawing
    buffer_width = window.get_width()
    buffer_height = int(buffer_width / ASPECT_RATIO)

    if buffer_width > monitor_size[0]:
        buffer_width = monitor_size[0]
        buffer_height = int(monitor_size[0] / ASPECT_RATIO)

    # Render buffer in the right scale
    buffer_scale = [buffer_width, buffer_height]
    buffer_pos = [(window.get_width() - buffer_width) / 2, (window.get_height() - buffer_height) / 2]
    window.blit(pygame.transform.scale(buffer, buffer_scale), buffer_pos)
    
    show_fps()
    pygame.display.flip()


pygame.quit()