import pygame
import pygame.gfxdraw
import collections

CANVAS_DEFAULT_COLOR = (255, 255, 255)
HISTORY_LENGTH = 32

class History:
    def __init__(self):
        self.undo_stack = collections.deque(maxlen=HISTORY_LENGTH + 1)
        self.redo_stack = collections.deque(maxlen=HISTORY_LENGTH)
        # self.undo_stack.append(self.image.copy())
    
    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            # self.image = self.undo_stack[-1].copy()

    def redo(self):
        if len(self.redo_stack) > 0:
            self.undo_stack.append(self.redo_stack.pop())
            # self.image = self.undo_stack[-1].copy()

from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.button import ButtonArray
from pygame import Surface

class ToolPicker(ButtonArray):
    def __init__(self, win, x, y, width, height, onClicks):
        super().__init__(win, x, y, width, height, (8, 1), onClicks=onClicks)

class Canvas(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height)
    
        self.color = kwargs.get('color', CANVAS_DEFAULT_COLOR)

        self.onClick = kwargs.get('onClick', lambda pos: None)
        self.onRelease = kwargs.get('onRelease', lambda pos: None)
        self.onDrag = kwargs.get('onDrag', lambda pos: None)
        self.clicked = False
        
        self.image = Surface((self._width, self._height), pygame.SRCALPHA)
        self.frame_image = self.image.copy() 

        self.final_image = Surface((self._width, self._height))
        self.final_image.fill(self.color)

    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()

            if self.contains(x, y):
                if mouseState == MouseState.RELEASE and self.clicked:
                    self.clicked = False
                    self.onRelease(self.toLocalSpace(x, y))

                elif mouseState == MouseState.CLICK:
                    self.clicked = True
                    self.onClick(self.toLocalSpace(x, y))
                
                elif mouseState == MouseState.DRAG and self.clicked:
                    self.onDrag(self.toLocalSpace(x, y))

            else:
                if self.clicked:
                    self.onRelease(self.toLocalSpace(x, y))
                self.clicked = False

    def toLocalSpace(self, x: int, y: int) -> tuple[int, int]:
        return (x - self._x, y - self._y)

    def draw(self):
        if self._hidden:
            return

        self.final_image.blit(self.image, (0, 0))
        self.final_image.blit(self.frame_image, (0, 0))
        self.win.blit(self.final_image, (self._x, self._y))

        self.frame_image.fill((0, 0, 0, 0))
        self.final_image.fill(self.color)

