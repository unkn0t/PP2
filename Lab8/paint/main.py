import os, sys
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import engine

import pygame
import pygame.gfxdraw
import pygame_widgets
import tools
import canvas

from pygame_widgets.button import ButtonArray, Button
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CANVAS_WIDTH = SCREEN_WIDTH
CANVAS_HEIGHT = int(0.85 * SCREEN_HEIGHT)
CONTROL_PANEL_WIDTH = SCREEN_WIDTH
CONTROL_PANEL_HEIGHT = SCREEN_HEIGHT - CANVAS_HEIGHT

BACKGROUND_COLOR = "#191919"
SEPARATOR_COLOR = "#3a3a3a"
INTERACTIVE_COLORS = ["#222222", "#2a2a2a", "#313131"]
TEXT_COLOR = "#eeeeee"

# Model: Tool, Color
# Presenter: Manager
# View: Canvas, ColorPicker, ToolButton(s), ControlPanel, RadiusPicker
# View -> Presenter -> Model (on event or on update)
# View <- Presenter <- Model (responce from model on update)
# View query -> Model responce
# Canvas must NOT know about Color, Tool or other UI, right now we transform coordinates 
# to local space inside tool, instead we must give info to the canvas what to do as a responce
# to the query DrawStart(pos), DrawEnd(pos), DrawContinue(pos) the responce would be Canvas.exec

from abc import abstractmethod

class DrawCommand:
    pass

class DrawContract:
    class View:
        @abstractmethod
        def draw(self, command: DrawCommand):
            pass

        @abstractmethod
        def displayToolSettings(self, settings):
            pass

    class Presenter:
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

    class Model:
        @abstractmethod
        def setStart(self, pos):
            pass

        @abstractmethod
        def setEnd(self, pos):
            pass

        @abstractmethod
        def getDrawCommand(self) -> DrawCommand:
            pass

        @abstractmethod
        def setColor(self, color: pygame.Color):
            pass
        
        @abstractmethod
        def setTool(self, tool_id: int):
            pass

class DrawModel(DrawContract.Model):
    def __init__(self):
        self.tools = (
            tools.LineTool(),
            tools.CircleTool(),
            tools.SquareTool(),
            tools.RectangleTool(),
            tools.RhombusTool(),
            tools.RightTriangleTool(),
            tools.EquilateralTriangleTool(),
            tools.EraserTool()
        )
        

class DrawPresenter(DrawContract.Presenter):
    def __init__(self, model: DrawContract.Model, view: DrawContract.View):
        self.model = model
        self.view = view

    def onMouseDown(self, pos):
        self.model.setStart(pos)

    def onMouseUp(self, pos):
        self.model.setEnd(pos)
     
    def onMouseMoved(self, pos):
        self.model.setEnd(pos)

    def onRedraw(self):
        command = self.model.getDrawCommand()
        self.view.draw(command)

    def onColorChanged(self, new_color: pygame.Color):
        self.model.setColor(new_color)

    def onToolChanged(self, new_tool_id: int):
        self.model.setTool(new_tool_id)

class DrawView(DrawContract.View):
    pass

class ControlPanel:
    def __init__(self, rect, scene):
        self.rect = rect
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(BACKGROUND_COLOR)
        self.buttons = ButtonArray(
            self.image,
            20, 50, 440, 60, 
            (8, 1),
            border = 7,
            colour = SEPARATOR_COLOR,
            inactiveColours = [INTERACTIVE_COLORS[0]] * 8,  
            hoverColours = [INTERACTIVE_COLORS[2]] * 8,
            pressedColours = [INTERACTIVE_COLORS[1]] * 8,
            onClicks = (
                lambda: scene.set_tool(tools.LineTool(scene.canvas)),
                lambda: scene.set_tool(tools.CircleTool(scene.canvas)),
                lambda: scene.set_tool(tools.SquareTool(scene.canvas)),
                lambda: scene.set_tool(tools.RectangleTool(scene.canvas)),
                lambda: scene.set_tool(tools.RightTriangleTool(scene.canvas)),
                lambda: scene.set_tool(tools.RhombusTool(scene.canvas)),
                lambda: scene.set_tool(tools.EquilateralTriangleTool(scene.canvas)),
                lambda: scene.set_tool(tools.EraserTool(scene.canvas)),
            )
        )
        self.font = pygame.font.SysFont('Iosevka', 16, bold=True)
        self.tool_label = self.font.render('Tools', True, TEXT_COLOR) 

        self.red_slider = Slider(
            self.image, 
            1000, 30, 255, 10,
            colour = pygame.Color('red'),
            handleColour = pygame.Color(TEXT_COLOR),
            min=0, max=255, step=1)
        self.green_slider = Slider(
            self.image, 
            1000, 60, 255, 10,
            colour = pygame.Color('green'),
            handleColour = pygame.Color(TEXT_COLOR),
            min=0, max=255, step=1)
        self.blue_slider = Slider(
            self.image, 
            1000, 90, 255, 10,
            colour = pygame.Color('blue'),
            handleColour = pygame.Color(TEXT_COLOR),
            min=0, max=255, step=1)
        self.red_out = TextBox(self.image, self.red_slider.getX() - 40, self.red_slider.getY() - 17, 35, 35, 
                               fontSize=16,
                               borderThickness=0,
                               colour=SEPARATOR_COLOR, textColour=TEXT_COLOR,
                               font = self.font)
        self.green_out = TextBox(self.image, self.green_slider.getX() - 40, self.green_slider.getY() - 17, 35, 35, 
                               fontSize=16,
                               borderThickness=0,
                               colour=SEPARATOR_COLOR, textColour=TEXT_COLOR,
                               font = self.font)
        self.blue_out = TextBox(self.image, self.blue_slider.getX() - 40, self.blue_slider.getY() - 17, 35, 35, 
                               fontSize=16,
                               borderThickness=0,
                               colour=SEPARATOR_COLOR, textColour=TEXT_COLOR,
                               font = self.font)
        self.red_out.disable()
        self.green_out.disable()
        self.blue_out.disable()

        self.final_color = Button(
            self.image,
            1300, 20, 100, 100,
            inactiveColour=pygame.Color(self.red_slider.getValue(), self.green_slider.getValue(), self.blue_slider.getValue())
        )

    def process_event(self, event):
        pygame_widgets.update(event)
            
    def update(self, screen):
        self.red_out.setText(self.red_slider.getValue())
        self.green_out.setText(self.green_slider.getValue())
        self.blue_out.setText(self.blue_slider.getValue())
        self.final_color.setInactiveColour(pygame.Color(self.red_slider.getValue(), self.green_slider.getValue(), self.blue_slider.getValue()))
        self.image.fill(BACKGROUND_COLOR)
        self.image.blit(self.tool_label, 
                        (self.buttons.getWidth() // 2 + self.buttons.getX() - self.tool_label.get_width() // 2, 20))
        pygame_widgets.update([])
        screen.blit(self.image, self.rect)

class MainScene(engine.Scene):
    def _on_load(self):
        self.canvas = canvas.Canvas(pygame.Rect(0, SCREEN_HEIGHT - CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT))
        self.tool = tools.EraserTool(self.canvas)
        self.control_panel = ControlPanel(
            pygame.Rect(0, 0, CONTROL_PANEL_WIDTH, CONTROL_PANEL_HEIGHT), self)

    def set_tool(self, new_tool):
        self.tool = new_tool

    def _on_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.canvas.rect.collidepoint(event.pos):
                self.tool.on_mouse_down(event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.tool.on_mouse_up(event.button, event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                self.canvas.undo()
            elif event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                self.canvas.redo()
        self.control_panel.process_event(event)

    def _on_update(self):
        self.control_panel.update(self.app.screen)
        self.canvas.tool_color = self.control_panel.final_color.inactiveColour
        self.tool.update()
        self.canvas.update(self.app.screen)

def main():
    app = engine.Application((SCREEN_WIDTH, SCREEN_HEIGHT), 'Paint')
    app.scene_manager.add_scene(MainScene())
    app.scene_manager.switch_to(0)
    app.run()

main()
