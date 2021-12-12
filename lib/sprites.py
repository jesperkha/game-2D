import pygame
import os

FPS = 60

# Shorthand for getting image
def get_image(filename: str, size: tuple = None) -> pygame.Surface:
    "Shorthand for getting image. Scaled if dimensions are given."
    img = pygame.image.load(filename).convert_alpha()
    if size: img = pygame.transform.scale(img, size)
    return img


# Creates copy of pygame surface at specified point
def clip_surface(surf, x, y, w, h) -> object:
    "Cuts out selected portion of a sprite."
    temp_surf = surf
    clip_rect = pygame.Rect(x, y, w, h)
    temp_surf.set_clip(clip_rect)
    return surf.subsurface(temp_surf.get_clip())


# Gets sprites from file by filename
def get_sprites(filename: str, size: tuple, scale: int = 1) -> list:
    "Returns a list of sprites from spritesheet"
    tilesheet = get_image(filename)
    return sget_sprites(tilesheet, size, scale)


# Gets sprites from given surface
def sget_sprites(sheet: pygame.Surface, size: tuple, scale: int = 1) -> list:
    "Returns a list of sprites from spritesheet"
    sprites = []

    # Cut out each tile from tilesheet
    sheet_cols = sheet.get_width() // size[0]
    sheet_rows = sheet.get_height() // size[1]
    # Prevent rounding error
    if sheet_rows == 0: sheet_rows = 1

    for r in range(sheet_rows):
        for c in range(sheet_cols):
            cut_tile = clip_surface(sheet, c * size[0], r * size[1], size[0], size[1])
            if scale != 1:
                transf = (int(cut_tile.get_width() * scale), int(cut_tile.get_height() * scale))
                cut_tile = pygame.transform.scale(cut_tile, transf)

            sprites.append(cut_tile)
    
    return sprites


# Gets each row in sprite sheet as a different sprite list. Used for animation grouping
def get_sprite_rows(filename: str, size: tuple, scale: int = 1) -> list[list]:
    "Returns a list of all sprites in each row. Removes blank frames"
    lists = []
    spritesheet = get_image(filename)
    rows = spritesheet.get_height() // size[1]
    w = spritesheet.get_width()
    for n in range(rows):
        row_surf = clip_surface(spritesheet, 0, size[1] * n, w, size[1])
        sprites  = sget_sprites(row_surf, size, scale)

        # Remove blank frames
        for frame in sprites:
            rect = frame.get_bounding_rect()
            if rect.width == rect.height == 0:
                sprites.remove(frame)
        
        lists.append(sprites)

    return lists


# Object for storing animation values
class Animation:
    def __init__(self, sprites: list, fps: int) -> None:
        "Animation player for rendering sprites with animations"
        self.ticks = 0
        self.fps = fps
        self.frame_swap = FPS // fps
        self.on_frame = 0
        self.sprites = sprites
        self.num_frames = len(sprites)
        self.running = False
        self.once = False
        self.keyframes = []
    

    # Runs through the frames and swaps frame when specified ticks have passed
    def draw(self, win: object, pos: tuple, dir: int = 1) -> bool:
        "Draw sprite to window. Renders first sprite in list if not playing an animation. Returns True if animation is done."
        if self.running:
            self.ticks += 1
            # Reset tick counter
            if self.ticks >= FPS:
                self.ticks = 0

            # Goto nest frame
            if self.ticks % self.frame_swap == 0:
                self.on_frame += 1
            
            # Reset animation
            if self.on_frame > len(self.sprites) - 1:
                if self.once:
                    self.running = False
                    return True

                self.on_frame = 0
            
            # Call keyframes
            for keyframe in self.keyframes:
                if self.on_frame == keyframe[0]: keyframe[1]()
        else:
            self.on_frame = 0
        
        flipped = pygame.transform.flip(self.sprites[self.on_frame], dir == -1, False)
        win.blit(flipped, pos)
        return False
    

    # Starts animation player
    def start(self, once: bool = False, jump_frame: int = 0) -> None:
        "Starts / resets animation. `jump_frame` specifies which frame to start on."
        self.on_frame = jump_frame
        self.running = True
        self.once = once
        self.ticks = 0


    # Stops animation
    def stop(self) -> None:
        "Stops running animation and returns to default."
        self.running = False

    
    # Keyframes makes it easy to time functions with animation steps
    # For example: footstep particles for each frame the foot hits the 
    # ground is super easy with keyframes.
    def keyframe(self, frames: tuple, method) -> None:
        "Adds keyframes to animation. Callback upon specified on_frame."
        for frame in frames: self.keyframes.append((frame, method))
    

    # Dynamically set fps for animation instead of using a fps list in
    # an AnimationGrouping
    def set_fps(self, new_fps) -> None:
        "Sets new fps for animation. Resets .frame_swap too"
        self.fps = new_fps
        self.frame_swap = FPS // self.fps



# Grouping of multiple animations from the same sprite sheet where
# each row represents a different animation. Animations can be named
# and played by calling .draw() with its respective name.
class AnimationGrouping:
    def __init__(self, sprites: list[list[pygame.Surface]], keys: list[dict]) -> None:
        self.animations = {}
        for idx, spr in enumerate(sprites):
            data = keys[idx]
            animation = Animation(spr, data["fps"])
            animation.start()
            self.animations[data["name"]] = animation

        self.num_animations = len(self.animations)
        self.last_animation = keys[0]["name"]

    
    # Draws the correct animation at pos
    def draw(self, win: pygame.Surface, animation: str, pos: tuple, dir: int = 1) -> int:
        "Calls Animation.draw() on selected animation, Returns current animation frame"
        anim = self.animations[animation]
        frame = anim.on_frame # is reset in line below
        if animation != self.last_animation:
            anim.start()
            self.last_animation = animation

        anim.draw(win, pos, dir)
        return frame

    
    # Resets all animations
    def reset(self) -> None:
        "Calls Animation.reset() on every animation in group"
        for key in self.animations:
            self.animations[key].start()


    # Keyframes the selected animation
    def keyframe(self, animation: str, frames: tuple, method) -> None:
        "Calls Animation.keyframe() on selected animation"
        self.animations[animation].keyframe(frames, method)



# Gets all animations from a folder containing multiple sprite sheets.
# Animations are named after their filenames
def load_animations(dirname: str, size: tuple, fpss: list[int] = [], scale: int = 1) -> AnimationGrouping:
    default_fps = 8
    if len(fpss) == 1: default_fps = fpss[0]
    
    animations = []
    names = []
    for idx, f in enumerate(os.listdir(dirname)):
        if not f.endswith(".png"):
            continue
        sprites = get_sprites(f"{dirname}/{f}", size, scale)
        animations.append(sprites)
        fps = default_fps
        if idx < len(fpss): fps = fpss[idx]
        names.append({
            "name": f.split(".png")[0],
            "fps": fps
        })

    return AnimationGrouping(animations, names)
    