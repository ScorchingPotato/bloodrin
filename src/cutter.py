# sprite_cutter.py - Simple 32x32 sprite sheet cutter

import pygame

class SpriteCutter:
    def __init__(self, sprite_size=32):
        self.sprite_size = sprite_size
        self.sprite_cache = {}
    
    def cut_sprite(self, sheet, row, col):
        """Cut a single sprite from sheet at row, col position"""
        x = col * self.sprite_size
        y = row * self.sprite_size
        
        sprite = pygame.Surface((self.sprite_size, self.sprite_size), pygame.SRCALPHA)
        sprite.blit(sheet, (0, 0), (x, y, self.sprite_size, self.sprite_size))
        return sprite
    
    def cut_row(self, sheet, row, count=None):
        """Cut entire row of sprites"""
        if count is None:
            count = sheet.get_width() // self.sprite_size
        
        sprites = []
        for col in range(count):
            sprite = self.cut_sprite(sheet, row, col)
            sprites.append(sprite)
        return sprites
    
    def cut_all(self, sheet):
        """Cut all sprites from sheet into 2D array"""
        rows = sheet.get_height() // self.sprite_size
        cols = sheet.get_width() // self.sprite_size
        
        sprites = []
        for row in range(rows):
            sprite_row = []
            for col in range(cols):
                sprite = self.cut_sprite(sheet, row, col)
                sprite_row.append(sprite)
            sprites.append(sprite_row)
        return sprites
    
    def get_sprite(self, sheet, row, col):
        """Get sprite with caching"""
        cache_key = (id(sheet), row, col)
        
        if cache_key not in self.sprite_cache:
            self.sprite_cache[cache_key] = self.cut_sprite(sheet, row, col)
        
        return self.sprite_cache[cache_key]

# Global cutter instance
cutter = SpriteCutter()

# Convenience functions
def cut_sprite(sheet, row, col):
    """Cut single sprite at row, col"""
    return cutter.cut_sprite(sheet, row, col)

def cut_row(sheet, row, count=None):
    """Cut entire row"""
    return cutter.cut_row(sheet, row, count)

def cut_all(sheet):
    """Cut all sprites"""
    return cutter.cut_all(sheet)

def get_sprite(sheet, row, col):
    """Get sprite with caching"""
    return cutter.get_sprite(sheet, row, col)