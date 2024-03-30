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
    def _on_event(self):
        pass

    @abstractmethod
    def _on_update(self):
        pass

    @abstractmethod
    def _on_redraw(self):
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
