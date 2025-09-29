import pygame
from modules import *

class App:

    def __init__(self):

        # self.window = pygame.Window(GAME_NAME, (W, H))
        # self.screen = self.window.get_surface()
        self.screen = pygame.display.set_mode((W, H), flags=pygame.SCALED )
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.Clock()
        
        pygame.event.set_blocked(None)
        pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                pygame.KEYDOWN, pygame.KEYUP))
        
        self.master = Master()
        self.master.app = self
        self.debug = Debug(self.screen, font=self.master.font_med, offset=4, surf_enabled=True)
        self.master.debug = self.debug
        self.game = Game(self.master)

    def run(self):

        while True:
            
            # self.window.flip()
            pygame.display.flip()

            self.master.dt = self.clock.tick(FPS) / 16.66667
            self.debug("FPS:", round(self.clock.get_fps(), 2))
            self.debug("Mouse:", pygame.mouse.get_pos())

            for event in pygame.event.get((pygame.QUIT)):
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

            self.screen.fill("beige")
            self.game.run()
            self.debug.draw()


if __name__ == "__main__":
    
    pygame.init()
    App().run()
