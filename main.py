import pygame
from modules import *
from enum import Enum

class State(Enum):
    
    MAIN_MENU = 0,
    LEVEL_MENU = 1,
    IN_GAME = 2,
    PAUSE = 3,
    WIN = 4,
    LOOSE = 5,

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
        
        self.state = State.MAIN_MENU
        self.master = Master()
        self.master.State = State
        self.master.app = self
        self.debug = Debug(self.screen, font=self.master.font_med, offset=4, surf_enabled=True)
        self.master.debug = self.debug
        self.game = Game(self.master)
        self.main_menu = MainMenu(self.master)
        self.level_menu = LevelMenu(self.master)
        self.pause_menu = PauseMenu(self.master)
        self.win_screen = WinScreen(self.master)
        self.loose_screen = LooseScreen(self.master)

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
                
            self.run_states()

            self.debug.draw()
            
    def run_states(self):
        
        self.master.debug("state", self.state)
        
        if self.state == State.MAIN_MENU:
            self.main_menu.run()
        elif self.state == State.LEVEL_MENU:
            self.level_menu.run()
        elif self.state == State.IN_GAME:
            self.game.run()
        elif self.state == State.PAUSE:
            self.pause_menu.run()
        elif self.state == State.WIN:
            self.win_screen.run()
        elif self.state == State.LOOSE:
            self.loose_screen.run()
            

if __name__ == "__main__":
    
    pygame.init()
    App().run()
