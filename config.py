# GLOBAL CONSTANTS
# ---------------------------------------------------------

WINDOW_NAME  = "Santarun"
ASPECT_RATIO = 16 / 9
FULLSCREEN   = False
WINDOW_SCALE = 4
FPS          = 60

TILESIZE = 16
HEIGHT   = 9 * TILESIZE
WIDTH    = 16 * TILESIZE

# FLOW CONTROL
# ---------------------------------------------------------

# pygame.mouse.set_visible(False)
import json

class mouse:
    x = 0
    y = 0
    @staticmethod
    def tup(): return (mouse.x, mouse.y)


def load_json(filename: str) -> dict:
    return json.load(open(filename))

_setups = []
def append_setup(func) -> None:
    _setups.append(func)

def setup():
    _loops.sort(key=lambda f: f[0])
    for f in _setups: f()

_loops = []
def append_loop(func, layer: int = 0) -> None:
    _loops.append([layer, func, False])

def loop(win: object, dt: int):
    global cols
    cols = pad*2 # account for fps
    for f in _loops:
        if not f[2]: f[1](win, dt)
    
    for l in log_queue:
        win.blit(l[0], l[1])

    log_queue.clear()

def lock_layer(layer: int) -> None:
    for f in _loops:
        if f[0] == layer: f[2] = True

def unlock_layer(layer: int) -> None:
    for f in _loops:
        if f[0] == layer: f[2] = False


# DEBUG
# ---------------------------------------------------------

import pygame

def panic(msg: str) -> None:
    print(msg)
    pygame.quit()
    quit()


pad = 20
cols = pad
f = pygame.font.SysFont("Tahoma", 10)

log_queue = []
def log(msg: any) -> None:
    global cols
    font_surf = f.render(f"{msg}", 0, "white")
    log_queue.append((font_surf, (cols, 0)))
    cols += font_surf.get_width() + pad
