# Version 2.2
# Read and render tilemaps

# Note:
# Tilemap file formating as per tilemap_editor v1.2

from config import panic
import pygame

# Stores tile data and sprites
class Tilemap:
    def __init__(self, map: str, tiles: list, size: tuple) -> None:
        """
        `map`: path to tilemap file
        `tiles`: list of `pygame.Surface`. Leave empty for collsion maps
        `size`: tilesize
        """
        raw = map
        if type(map) == str:
            raw = open(map, "r").read().split(".")
        self.rows = int(raw[0])
        self.cols = int(raw[1])
        self.data = [char for char in raw[2]]

        self.tiles    = tiles
        self.offset_x = 0
        self.offset_y = 0

        self.tile_w = size[0]
        self.tile_h = size[1]
        self.buffer = pygame.Surface((self.cols * self.tile_w, self.rows * self.tile_h), pygame.SRCALPHA)

        # List of all tiles that can be collided with
        # Stored as [tile_val, x, y]
        letters = "0123456789abcdefghijklmnopqrstuvwxyz"
        if len(self.tiles) >= len(letters):
            panic("Too many tiles for Tilemap. Update tile index list")

        if len(self.tiles) == 0:
            panic("No tiles in Tilemap tile list")

        self.valid_tiles = []
        for row in range(self.rows):
            for col in range(self.cols):
                i = letters.index(self.data[col + row * self.cols])
                if i >= len(tiles): continue
                self.valid_tiles.append([i, col * self.tile_w, row * self.tile_h])
                self.buffer.blit(self.tiles[i], (col * self.tile_w, row * self.tile_h))

    
    # Sets the drawing and collision offset for tilemap
    def _set_offset(self, x: int, y: int) -> None:
        self.offset_x = x
        self.offset_y = y


    # Draws tilemap from tilemap object
    def draw(self, win: object) -> tuple:
        """Draws tilemap. Returns map dimensions"""
        win.blit(self.buffer, (self.offset_x, self.offset_y))


    # Finds the side of collision between tile and object.
    # Returns None if there is no collision
    def check_tile_collision(self, x, y, w, h, vel) -> list:
        """
        Returns list of tuples with tile data:\n
        \t(side, tile value, x, y, w, h)
        """

        colliding_tiles = []

        for tile in self.valid_tiles:
            tile_x = tile[1] + self.offset_x
            tile_y = tile[2] + self.offset_y

            top    = tile_y > y + h
            left   = tile_x > x + w
            right  = tile_x + self.tile_w < x
            bottom = tile_y + self.tile_h < y

            if top or left or right or bottom:
                continue

            collision_threshold = 6
            tile_value = tile[0]
            side = ""

            if abs(tile_y - (y + h)) <= collision_threshold and vel.y >= 0:
                side = "top"

            elif abs((tile_x + self.tile_w) - x) <= collision_threshold and vel.x <= 0:
                side = "right"

            elif abs(tile_x - (x + w)) <= collision_threshold and vel.x >= 0:
                side = "left"

            elif abs((tile_y + self.tile_h) - y) <= collision_threshold and vel.y < 0:
                side = "bottom"

            colliding_tiles.append((side, tile_value, tile_x, tile_y, self.tile_w, self.tile_h))

        return colliding_tiles


    # Returns true if x and y is overlapping a tile in the map
    # Ignores tile values in ignore tuple
    def tile_at(self, x: int, y: int, ignore: tuple = ()) -> bool:
        "Returns true if a tile is at (x, y)"
        for tile in self.valid_tiles:
            tile_x = tile[1] + self.offset_x
            tile_y = tile[2] + self.offset_y
            if x == tile_x and y == tile_y and tile[0] not in ignore:
                return True
        
        return False


# Group of tilemaps for a level map
class TilemapGroup:
    def __init__(self, *args) -> None:
        self.tilemaps = [t for t in args]
        self.offset_x = 0

    
    def draw_tilemaps(self, player: object, win: object) -> None:
        "Handles rendering of tilemap based on pos of player given"
        # offset stops once tilemap end is in view
        width = win.get_width()

        player_offset = player.pos.x - width/2
        end_right = -width * (len(self.tilemaps) - 1)

        if player_offset > 0 and self.offset_x <= end_right: # at end right
            self.offset_x = end_right

        elif player_offset < 0 and self.offset_x >= 0: # at end left
            self.offset_x = 0

        else:
            self.offset_x -= player.vel.x
            player.pos.x = width/2

        for index, tilemap in enumerate(self.tilemaps):
            tilemap._set_offset(self.offset_x + width * index, 0)
            tilemap.draw(win)