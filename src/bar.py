import pygame
from src.assetloader import assets

bloodcolors = {
    'n': (128, 36, 33),
    'r': (189, 57, 34),
    'c': (148, 30, 41),
    'm': (128, 28, 53)
}

class Blood:
    def __init__(self,type,amount):
        self.type = type
        self.amount = amount
        self.color = bloodcolors[type]

class BloodBar:
    def __init__(self,owner,bt,b,bartype="blood"):
        self.owner = owner
        self.image = assets.get(f"{bartype}bar")
        self.w = 24
        self.h = 8
        self.blood = [Blood(bt, b)]
        self.maxb = b
    def draw(self,pos):
        self.x, self.y = pos; self.y+=32
        cx = 0
        pygame.draw.rect(self.owner.g.screen, (50,60,57), pygame.Rect(self.x + 4, self.y + 4, self.w, self.h))
        for b in self.blood:
            pygame.draw.rect(self.owner.g.screen,b.color,pygame.Rect(self.x + cx+4, self.y + 4, self.w * b.amount / self.maxb, self.h))
            cx += self.w * b.amount / 100
            if len(self.blood) > 1 and b != self.blood[-1]:
                pygame.draw.rect(self.owner.g.screen, (227, 156, 64), pygame.Rect(self.x + cx+4-1, self.y + 4, 1, self.h-1))
        self.owner.g.screen.blit(self.image, (self.x, self.y))
        
