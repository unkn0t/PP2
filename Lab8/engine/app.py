import pygame

from .scene import SceneManager

class Application:
    def __init__(self, mode, caption, *, fullscreen=False) -> None:
        pygame.init()
        
        if fullscreen:
            fullscreen_mode = pygame.display.get_desktop_sizes()[0]
            self.screen = pygame.display.set_mode(fullscreen_mode, pygame.FULLSCREEN | pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(mode)
        pygame.display.set_caption(caption)
        
        self.scene_manager = SceneManager(self)
        self.clock = pygame.Clock()
        self.is_running = False
        self.delta_time = 0
    
    def __del__(self):
        pygame.quit()

    def run(self, *, fps=0):
        self.is_running = True
        while self.is_running:
            for event in pygame.event.get():
                self._on_event(event)
            self._on_update()
            self._on_redraw()
            pygame.display.update()
            self.delta_time = self.clock.tick(fps) / 1000.0
    
    def _on_event(self, event: pygame.Event):
        current_scene = self.scene_manager.get_current()
        current_scene._on_event(event)

    def _on_update(self):
        current_scene = self.scene_manager.get_current()
        current_scene._on_update()

    def _on_redraw(self):
        current_scene = self.scene_manager.get_current()
        current_scene._on_redraw()

