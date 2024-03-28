import pygame
from pygame.locals import *
from pygame_gui.elements import UIImage

import tools

class UICanvas(UIImage):
    def __init__(self, relative_rect: pygame.Rect, background_color: pygame.Color = Color(255, 255, 255), 
                 manager = None, anchors = None):
        self.surface = pygame.Surface(relative_rect.size, pygame.SRCALPHA)
        self.surface.fill(background_color)
        self.tool = tools.Circle()
        super().__init__(relative_rect, self.surface, manager=manager, anchors=anchors)   

    def process_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.Vector2(event.pos) - pygame.Vector2(self.get_abs_rect().topleft)
            self.tool.set_in_preview(pos)
            return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.hovered:
                self.tool.set_ready()
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.hovered:
                pos = pygame.Vector2(event.pos) - pygame.Vector2(self.get_abs_rect().topleft)
                self.tool.update(pos)
                return True
        
        return False

    def update(self, time_delta: float):
        super().update(time_delta)
        if self.tool.ready:
            self.tool.draw(self.surface)
        else:
            self.set_image(self.surface)
            self.tool.draw(self.image)

