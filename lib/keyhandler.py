# Version 1.0

import pygame

class KeyHandler:
    def __init__(self) -> None:
        """Handles keyboard inputs
        Methods:
        \t.add() - add new key listener
        \t.update() - update the KeyHandler"""
        self.keys = []
    

    def add(self, key, state: str, callback) -> dict:
        "Keystates: keydown, keyup, keypressed"
        new_key = {
            "key": key,
            "state": state,
            "callback": callback,
            "current_state": False
        }
        self.keys.append(new_key)
        return new_key


    def is_pressed(self, key: int) -> bool:
        "Gets the state of specified key"
        for k in self.keys:
            if k["key"] == key:
                return k["current_state"]
    

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        for key in self.keys:
            key_state = key["current_state"]
            is_pressed = keys[key["key"]]
            
            # Keydown
            if key["state"] == "keydown":
                if is_pressed:
                    key["callback"]()
            
            # Keypressed
            if key["state"] == "keypressed":
                if key_state == False and is_pressed:
                    key_state = True
                    key["callback"]()
                
                if not is_pressed:
                    key_state = False
            
            # Keyup
            if key["state"] == "keyup":
                if key_state == True and not is_pressed:
                    key["callback"]()
                    key_state = False
                
                if is_pressed:
                    key_state = True

            key["current_state"] = key_state