from abc import abstractmethod, ABC
import pygame
from draw.command import Command

class View(ABC):
    @abstractmethod
    def draw(self, command: Command):
        pass

    @abstractmethod
    def displayToolSettings(self, settings):
        pass

class Presenter(ABC):
    @abstractmethod
    def onMouseDown(self, pos):
        pass 

    @abstractmethod
    def onMouseUp(self, pos):
        pass
    
    @abstractmethod
    def onRedraw(self):
        pass

    @abstractmethod
    def onMouseMoved(self, pos):
        pass

    @abstractmethod
    def onColorChanged(self, new_color: pygame.Color):
        pass

    @abstractmethod
    def onToolChanged(self, new_tool_id: int):
        pass

class Model(ABC):
    @abstractmethod
    def activateTool(self, pos):
        pass

    @abstractmethod
    def finishTool(self, pos):
        pass
    
    @abstractmethod 
    def updateTool(self, pos):
        pass

    @abstractmethod
    def getCommand(self) -> Command:
        pass

    @abstractmethod
    def setColor(self, color: pygame.Color):
        pass
    
    @abstractmethod
    def setTool(self, tool_id: int):
        pass
