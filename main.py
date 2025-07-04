import pygame
import asyncio
from src.assetloader import assets
from src.figurines import *
from src.mouse import Mouse

class Game:
    def __init__(self):
        pygame.init()
        # Enable touch input events
        pygame.event.set_allowed([
            pygame.FINGERDOWN,
            pygame.FINGERUP,
            pygame.FINGERMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
            pygame.MOUSEMOTION,
            pygame.QUIT
        ])

        self.window = pygame.display.set_mode((1024, 768))
        assets.load_all()

        #Layers
        self.uilayer = pygame.Surface((256, 192), pygame.SRCALPHA)
        self.screen = pygame.Surface((256, 192), pygame.SRCALPHA)
        self.debuglayer = pygame.Surface((256, 192), pygame.SRCALPHA)
        self.background = pygame.Surface((256, 192), pygame.SRCALPHA)

        pygame.display.set_caption("Bloodrin")
        self.clock = pygame.time.Clock()
        self.running=True
        self.mouse = Mouse(self)

        self.f = Player(self,"figurines", 0, 100, "r")
        self.p = Player(self,"figurines", 1, 100, "n")
        self.e = Enemy(self,"enemies", 0, 100, "m")
        

    async def run(self):
        while self.running:
            self.update()
            self.draw()
            self.render()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False

            await asyncio.sleep(0)
        pygame.quit()

    def scale(self, surface):
        """Scale a surface to a new size"""
        return pygame.transform.scale(surface, (1024, 768))
    
    def draw(self):
        self.background.fill((25,20,40))
        self.f.draw((32,64))
        self.e.draw((128,64))
        self.p.draw((64,128))
        self.mouse.draw()

    def render(self):
        self.window.blit(self.scale(self.background), (0, 0))
        self.window.blit(self.scale(self.debuglayer), (0, 0))
        self.window.blit(self.scale(self.screen), (0, 0))
        self.window.blit(self.scale(self.uilayer), (0, 0))
        self.background.fill((0,0,0,0))
        self.debuglayer.fill((0,0,0,0))
        self.screen.fill((0,0,0,0))
        self.uilayer.fill((0,0,0,0))
        pygame.display.flip()

    def update(self):
        self.mouse.update()


g = Game()
if __name__ == "__main__":
    asyncio.run(g.run())

