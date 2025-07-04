import pygame
from src.assetloader import assets
from src.cutter import *
import random
from src.bar import BloodBar,Blood

class selectdrop:
    def __init__(self,owner,colors):
        self.owner = owner
        self.colors = colors
        self.basec = colors[0]
        self.hoverc = colors[1]
        self.selectc = colors[2]
    def draw(self,pos):
        self.x, self.y = pos
        c = self.selectc if not self.owner.selected or self.owner.helped else self.basec
        if self.owner.selected:
            pygame.draw.line(self.owner.g.screen,c,(self.x+16,self.y+28),self.owner.g.mouse.pos,4)
        pygame.draw.ellipse(self.owner.g.screen,(0,0,0,0),pygame.Rect(self.x+4,self.y+20,24,16))
        pygame.draw.ellipse(self.owner.g.screen,c,pygame.Rect(self.x+4,self.y+20,24,16),2)


class Figurine:
    def __init__(self,game,i,r,blood,bloodtype):
        self.g = game
        self.i = i
        self.r = r
        self.load()
        self.pos = (0,0)
        self.rect = pygame.Rect(7,3,18,30)
        

        #animation control
        self.f = 0
        self.fps = 0.1
        self.timer = random.randint(3,5)*60
        self.t = 0

    def load(self):
        self.sprites = cut_all(assets.get(self.i))[self.r]
        self.sprites.append(self.sprites[1])

    def idle(self):
        self.t += 1
        if self.t >= self.timer:
            self.f += self.fps
            if int(self.f) >= len(self.sprites):
                self.f = 0
                self.t = 0
                self.timer = random.randint(3,5)*60

    def draw(self,pos):
        self.update(pos)
        sprite = self.sprites[int(self.f)]
        self.g.screen.blit(sprite, pos)
        self.bar.draw(pos)
        pygame.draw.rect(self.g.debuglayer, (255, 0, 0,50), self.rect)

    def update(self,pos):
        self.idle()
        self.rect.topleft = (pos[0]+7, pos[1]+3)

    def lose_blood(self, amount):
        """Reduce blood amount and update bar"""
        b = self.bar.blood[-1]
        b.amount -= amount
        if b.amount <= 0:
            self.bar.blood.pop()
    def gain_blood(self,type, amount):
        s = sum(b.amount for b in self.bar.blood)
        a = self.bar.maxb - s
        for b in self.bar.blood:
            if b.type == type:
                b.amount += amount if amount <= a else a
                return
        self.bar.blood.append(Blood(type, amount if amount <= a else a))

class Player(Figurine):
    def __init__(self, game, i, r, blood, bloodtype):
        super().__init__(game, i, r, blood, bloodtype)
        self.bar = BloodBar(self, bloodtype, blood, "blood")
        self.drop = selectdrop(self, [(57, 50, 128), (61, 59, 137), (78, 64, 189)])
        self.selected = False
        self.drop = selectdrop(self, [(57, 50, 128), (61, 59, 137), (78, 64, 189)])

    def update(self,pos):
        super().update(pos)
        if self.g.mouse.click:
            if self.g.mouse.hover(self.rect):
                if self.g.mouse.grab == None:
                    self.selected = True
                    self.g.mouse.grab = self
                    self.g.mouse.set_state('grab')
                else:
                    self.g.mouse.set_state('help')
                    self.helped = True
        else:
            self.selected = False
            self.helped = False
            self.g.mouse.grab = None
            self.g.mouse.set_state('select')
        
    def draw(self,pos):
        self.drop.draw(pos)
        super().draw(pos)


class Enemy(Figurine):
    def __init__(self, game, i, r, blood, bloodtype):
        super().__init__(game, i, r, blood, bloodtype)
        self.bar = BloodBar(self, bloodtype, blood, "enemy")

    def update(self, pos):
        super().update(pos)
        if self.g.mouse.grab:
            if self.g.mouse.hover(self.rect):
                self.g.mouse.set_state('attack')
            else:
                self.g.mouse.set_state('grab')
        
            
