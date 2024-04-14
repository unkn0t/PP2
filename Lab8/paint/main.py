import os, sys
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import engine

from typing import List
import draw, draw.contract, draw.ui
from pygame.event import Event
from pygame import Color
import pygame_widgets
import tool

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

class DrawModel(draw.contract.Model):
    def __init__(self):
        self.tools = (
            tool.Line(),
            tool.Circle(),
            tool.Square(),
            tool.Rectangle(),
            tool.Rhombus(),
            tool.RightTriangle(),
            tool.EquilTriangle(),
            tool.Eraser()
        )
        self.tool_id = 0
        self.color = Color('black')

    def currentTool(self) -> tool.ToolBase:
        return self.tools[self.tool_id]
        
    def activateTool(self, pos):
        self.currentTool().activate(pos)

    def finishTool(self, pos):
        self.currentTool().finish(pos)

    def updateTool(self, pos):
        self.currentTool().update(pos)

    def getCommand(self) -> draw.Command:
        current_tool = self.currentTool()
        if type(current_tool) is tool.Eraser:
            return current_tool.getCommand(Color('white'))
        return current_tool.getCommand(self.color)

    def setColor(self, color: Color):
        self.color = color
    
    def setTool(self, tool_id: int):
        self.tool_id = tool_id

class DrawPresenter(draw.contract.Presenter):
    def __init__(self, model: draw.contract.Model, view: draw.contract.View):
        self.model = model
        self.view = view

    def onMouseDown(self, pos):
        self.model.activateTool(pos)

    def onMouseUp(self, pos):
        self.model.finishTool(pos)
     
    def onMouseMoved(self, pos):
        self.model.updateTool(pos)

    def onRedraw(self):
        command = self.model.getCommand()
        self.view.draw(command)

    def onColorChanged(self, new_color: Color):
        self.model.setColor(new_color)

    def onToolChanged(self, new_tool_id: int):
        self.model.setTool(new_tool_id)

class DrawView(draw.contract.View):
    def __init__(self, model: draw.contract.Model, screen):
        self.presenter = DrawPresenter(model, self)
        
        self.canvas = draw.ui.Canvas(
            screen, 
            0, 150, SCREEN_WIDTH, SCREEN_HEIGHT,
            onClick = lambda pos: self.presenter.onMouseDown(pos),
            onRelease = lambda pos: self.presenter.onMouseUp(pos),
            onDrag = lambda pos: self.presenter.onMouseMoved(pos),
        )
        self.control_panel = draw.ui.Canvas(
            screen,
            0, 0, SCREEN_WIDTH, 150,
            color = (150, 150, 150)
        )

        self.tool_picker = draw.ui.ToolPicker(
            screen,
            0, 0, SCREEN_WIDTH // 3, 70,
            onClicks = [lambda i=i: self.presenter.onToolChanged(i) for i in range(8)]
        )

    def update(self, events: List[Event]):
        pygame_widgets.update(events)
        self.presenter.onRedraw()

    def draw(self, command: draw.Command):
        if isinstance(command, draw.OverlayCommand):
            command.execute(self.canvas.frame_image)
        else:
            command.execute(self.canvas.image)

    def displayToolSettings(self, settings):
        pass

class MainScene(engine.Scene):
    def _on_load(self):
        self.model = DrawModel() 
        self.model.setTool(-1)
        self.view = DrawView(self.model, self.app.screen)
        self.events = []

    def _on_event(self, event: Event):
        self.events.append(event)

    def _on_update(self):
        self.app.screen.fill('black')
        self.view.update(self.events)

def main():
    app = engine.Application((SCREEN_WIDTH, SCREEN_HEIGHT), 'Paint')
    app.scene_manager.add_scene(MainScene())
    app.scene_manager.switch_to(0)
    app.run()

main()
