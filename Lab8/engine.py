import pygame
from abc import abstractmethod

class Scene:
    def __init__(self) -> None:
        self.manager = None
        self.app = None

    def set_manager(self, manager) -> None:
        self.manager = manager
        self.app = self.manager.app
    
    @abstractmethod
    def _on_load(self):
        pass

    @abstractmethod
    def _on_unload(self):
        pass

    @abstractmethod
    def _on_event(self, event: pygame.Event):
        pass

    @abstractmethod
    def _on_update(self):
        pass

class SceneManager:
    def __init__(self, app) -> None:
        self._scenes = []
        self._current = -1
        self.app = app
        
    def get_current(self) -> Scene:
        return self._scenes[self._current]

    def switch_to(self, order: int):
        if self._current != -1:
            self.get_current()._on_unload()
        self._current = order
        self.get_current()._on_load()

    def add_scene(self, scene: Scene, order: int = -1) -> None:
        scene.set_manager(self)
        if order == -1:
            self._scenes.append(scene)
        else:
            self._scenes.insert(order, scene)

    def del_scene(self, scene: Scene) -> None:
        self._scenes.remove(scene)

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
                if event.type == pygame.QUIT:
                    self.is_running = False
                self._on_event(event)
            self._on_update()
            pygame.display.update()
            self.delta_time = self.clock.tick(fps) / 1000.0
    
    def _on_event(self, event: pygame.Event):
        current_scene = self.scene_manager.get_current()
        current_scene._on_event(event)

    def _on_update(self):
        current_scene = self.scene_manager.get_current()
        current_scene._on_update()

