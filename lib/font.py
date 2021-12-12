# Version 1.1
# Font render

from config import panic
from pygame import image, Rect, transform

class Font:
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789 ,.:;!?()'-"
    def __init__(self, filename, scale: int = 1) -> None:
        """
        Font class for displaying custom text in pygame.

        Values:\n
        \t.spacing - letter spacing
        \t.typespeed - speed of typewriter
        \t.scale - font size
        \t.line_height\n

        Methods:\n
        \t.load() - loads the individual images of the letters
        \t.render() - draws text, returns text rect tuple
        \t.typewrite() - writes a sentence letter by letter
        \t.reset() - reset typewriter"""
        
        self.filename = filename
        self.chars = {}
        self.counter = 0
        self.frames = 0

        self.spacing = 1
        self.scale = scale
        self.typespeed = 5
        self.line_height = 3
        self.char_height = 0

        self.loaded = False

    
    @staticmethod
    def clip_surface(surf, x, y, w, h) -> object:
        temp_surf = surf.copy()
        clip_rect = Rect(x, y, w, h)
        temp_surf.set_clip(clip_rect)
        new_image = surf.subsurface(temp_surf.get_clip())
        return new_image.copy()
    

    def load(self):
        font_image = image.load(self.filename).convert_alpha()
        self.char_height = font_image.get_height() * self.scale

        current_width = 0
        current_char = 0
        for x in range(font_image.get_width()):
            if font_image.get_at((x, 0)) == (255, 0, 0):
                self.chars[Font.letters[current_char]] = Font.clip_surface(font_image, x - current_width, 0, current_width, font_image.get_height())
                current_width = 0
                current_char += 1
            else:
                current_width += 1
        
        self.loaded = True

    
    def render(self, win: object, pos: tuple, text: str, max_width: int = None, num_chars: int = None) -> tuple:
        "Returns `(x, y, w, h)`"
        if not self.loaded:
            panic("Font used before loading")

        x_offset = 0
        x = pos[0]
        y = pos[1]

        width = 0
        height = 0

        max_chars = num_chars if num_chars != None else len(text)

        letters = []
        breakpoint_index_list = []
        current_line_width = 0
        current_word_width = 0
        last_space_index = 0

        # Places all the letter surfaces in the letters[] list
        for index, letter in enumerate(text):
            pre_char = self.chars[letter]
            scale = (pre_char.get_width() * self.scale, pre_char.get_height() * self.scale)
            char = transform.scale(pre_char, scale)
            letters.append(char)

            char_width = char.get_width() + (self.spacing * self.scale)
            current_line_width += char_width
            current_word_width += char_width

            height = char.get_height()

            if letter == " ":
                last_space_index = index
                current_word_width = 0

            elif max_width and current_line_width >= max_width:
                breakpoint_index_list.append(last_space_index)
                current_line_width = current_word_width # new line begins with last word added

                # find width of entire textbox
                if current_line_width - current_word_width > width:
                    width = current_line_width - current_word_width

        # Draws the letters and adds new lines
        for index, char in enumerate(letters):
            if index >= max_chars:
                break

            if index in breakpoint_index_list:
                y += char.get_height() + (self.line_height * self.scale)
                height = y # 
                x_offset = 0
            
            else: # skips space characters when rendering new lines
                win.blit(char, (x + x_offset, y))
                x_offset += char.get_width() + (self.spacing * self.scale)
                height = char.get_height()

        # returns size of string
        return (x, y, x_offset, height)


    def typewrite(self, win: object, pos: tuple, text: str, width: int = None, callback = None) -> tuple:
        self.frames += 1

        if self.counter == len(text) and callback:
            callback()
            self.counter += 1 # call only once
        elif self.frames % self.typespeed == 0:
            self.counter += 1

        return self.render(win, pos, text, width, self.counter)


    def reset(self) -> None:
        self.counter = 0
        self.frames = 0