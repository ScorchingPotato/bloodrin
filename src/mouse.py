import pygame
from src.assetloader import assets

class Mouse:
    def __init__(self, game):
        self.g = game
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.pos = (0, 0)
        self.click = False
        self.grab = None
        self.state = 0 #select
        pygame.mouse.set_visible(False)
        self.load()
        self.touch_id = None

    def update(self):
        # Handle mouse input
        m = pygame.mouse.get_pos()
        mouse_pressed = any(pygame.mouse.get_pressed())
        
        # Handle touch events
        for event in pygame.event.get():
            if event.type == pygame.FINGERDOWN and self.touch_id is None:
                # Convert touch coordinates (0-1) to screen coordinates
                x = event.x * self.g.window.get_width()
                y = event.y * self.g.window.get_height()
                self.touch_id = event.finger_id
                m = (x, y)
                mouse_pressed = True
            
            elif event.type == pygame.FINGERUP and event.finger_id == self.touch_id:
                self.touch_id = None
                mouse_pressed = False
            
            elif event.type == pygame.FINGERMOTION and event.finger_id == self.touch_id:
                # Convert touch coordinates to screen coordinates
                x = event.x * self.g.window.get_width()
                y = event.y * self.g.window.get_height()
                m = (x, y)

        # Update position and click state
        self.rect.topleft = (m[0]/4, m[1]/4)
        self.pos = (m[0]/4, m[1]/4)
        self.click = mouse_pressed

    def hover(self, rect):
        """Check if the mouse is hovering over a rectangle."""
        return self.rect.colliderect(rect)

    def set_state(self, state):
        for i,s in enumerate(['select', 'grab', 'block', 'attack', 'help']):
            if s == state:
                self.state = i
                break
    def load(self):
        self.sprites = [assets.get('mouse-'+i) for i in ['select','grab','block','attack','help']]
        

    def draw(self):
        self.g.uilayer.blit(self.sprites[self.state], self.rect.topleft)
        # Add touch debug visualization
        if self.touch_id is not None:
            pygame.draw.circle(self.g.debuglayer, (255, 0, 0), self.pos, 4, 1)
            # Draw touch info
            font = pygame.font.Font(None, 16)
            debug_text = f"Touch: ({int(self.pos[0])},{int(self.pos[1])})"
            text_surf = font.render(debug_text, True, (255, 0, 0))
            self.g.debuglayer.blit(text_surf, (4, 4))