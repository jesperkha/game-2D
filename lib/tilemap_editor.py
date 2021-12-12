# Version 1.2
# Tilemap editor

# EDITOR CONFIG ------------------------------------------------

FILENAME = "./assets/tilemap.png"
DEST     = "./data/" # with trailing /
TILESIZE = 16
COLS     = 16
ROWS     = 9
SCALE    = 4

# Extra
buffer_size = 100

def on_save_extra(data: list) -> None:
    pass

# --------------------------------------------------------------

import pygame
import math

clock = pygame.time.Clock()

letters = "0123456789abcdefghijklmnopqrstuvwxyz"
nil_tile = len(letters) - 1

rows   = ROWS
cols   = COLS
width  = TILESIZE * cols
height = TILESIZE * rows
scale  = SCALE
window = pygame.display.set_mode((width * scale, height * scale), pygame.RESIZABLE)
grid   = [[nil_tile for _ in range(rows)] for _ in range(cols)]

tiles = []
tilesheet = pygame.image.load(FILENAME).convert_alpha()
sheet_rows = tilesheet.get_height() // TILESIZE
sheet_cols = tilesheet.get_width() // TILESIZE
print(sheet_cols, sheet_rows)
if sheet_cols * sheet_rows >= len(letters):
    print("Too many tiles. Update tile index list.")
    exit()

pygame.display.set_caption("Tilemap Editor v1.2")

def clip_surface(surf, x, y, w, h):
    temp_surf = surf
    clip_rect = pygame.Rect(x, y, w, h)
    temp_surf.set_clip(clip_rect)
    new_image = surf.subsurface(temp_surf.get_clip())
    return pygame.transform.scale(new_image, (TILESIZE * scale, TILESIZE * scale))


# Cut out each tile from tilesheet
for r in range(sheet_rows):
    for c in range(sheet_cols):
        tiles.append(clip_surface(tilesheet, c * TILESIZE, r * TILESIZE, TILESIZE, TILESIZE))    

# Buffer for when loading maps with more tiles than selected sheet
nil_surface = pygame.Surface((TILESIZE, TILESIZE)).convert_alpha()
nil_surface.fill((0, 0, 0,0))
for _ in range(buffer_size): tiles.append(nil_surface)

num_sprites = len(tiles)
current_tile_select = 1

def get_grid_pos(x, y):
    grid_x = math.floor(x / TILESIZE / scale)
    grid_y = math.floor(y / TILESIZE / scale)
    return grid_x, grid_y


def get_tile_value(x, y):
    gx, gy = get_grid_pos(x, y)
    return grid[gx][gy]


def change_tile(btn):
    global current_tile_select
    x, y = pygame.mouse.get_pos()
    grid_x, grid_y = get_grid_pos(x, y)

    if btn == 0:
        grid[grid_x][grid_y] = current_tile_select
    if btn == 2:
        grid[grid_x][grid_y] = nil_tile
    if btn == 1:
        current_tile_select = grid[grid_x][grid_y]
    

def swap_tile_select(key):
    global current_tile_select
    if key == pygame.K_a:
        current_tile_select -= 1
    if key == pygame.K_d:
        current_tile_select += 1

    if current_tile_select == num_sprites:
        current_tile_select = 0
    if current_tile_select < 0:
        current_tile_select = num_sprites - 1


def open_file():
    filename = input("Open file: ") + ".map"
    f = open(filename, "r").read().split(".")[2]
    newgrid = [[nil_tile for _ in range(rows)] for _ in range(cols)]
    for row in range(rows):
        for col in range(cols):
            newgrid[col][row] = letters.index(f[row * cols + col])

    global grid
    grid = newgrid


def save_file():
    t = []
    for row in range(rows):
        for col in range(cols):
            t.append(letters[grid[col][row]])

    t = "".join(t)
    on_save_extra(t)
    # Save to file
    filename = input("Enter filename: ")
    if filename == "": exit()
    filename = DEST + filename
    f = open(filename + ".map", "w")
    f.write(f"{rows}.{cols}.{t}")
    f.close()
    pygame.quit()
    quit()


print("""
Left click: place tile
Right click: remove tile
Scroll click: pick tile

O: Open file
S: Save file
W: Toggle grid
A and D: swap between tiles
""")

show_grid = True
run = True
while run:
    clock.tick(30)

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            swap_tile_select(event.key)
            if event.key == pygame.K_w:
                show_grid = not show_grid
            
            if event.key == pygame.K_s:
                save_file()
            
            if event.key == pygame.K_o:
                open_file()
            
            if event.key == pygame.K_ESCAPE:
                run = False

    for index, btn in enumerate(pygame.mouse.get_pressed()):
        if btn: change_tile(index)

    window.fill((0, 0, 0))
    if show_grid:
        for r in range(rows):
            pygame.draw.line(window, (20, 100, 20), (0, r * TILESIZE * scale), (width * scale, r * TILESIZE * scale))
        for r in range(cols):
            pygame.draw.line(window, (20, 100, 20), (r * TILESIZE * scale, 0), (r * TILESIZE * scale, height * scale))

    # Render
    for row, arr in enumerate(grid):
        for col, val in enumerate(arr):
            x = row * TILESIZE * scale
            y = col * TILESIZE * scale
            window.blit(tiles[val], (x, y))

    pos = pygame.mouse.get_pos()
    x, y = get_grid_pos(pos[0], pos[1])
    sprite = tiles[current_tile_select].copy()
    sprite.set_alpha(140)
    window.blit(sprite, (x * TILESIZE * scale, y * TILESIZE * scale))
    
    pygame.display.update()


pygame.quit()
