from abc import abstractmethod

import pygame
import math
import pygame.gfxdraw as draw 
from pygame import Vector2, Surface, Color, Rect
import utils

PREVIEW_WIDTH = 3

class Tool:
    def __init__(self) -> None:
        self.in_preview = False
        self.ready = False
        self.color = Color(0,0,0)

    def set_in_preview(self, start_pos) -> None:
        self.in_preview = True
        self.ready = False
        self.on_start(Vector2(start_pos))

    def set_ready(self) -> None:
        self.in_preview = False
        self.ready = True
    
    def update(self, mouse_pos) -> None:
        if self.in_preview:
            self.on_update(Vector2(mouse_pos))

    def draw(self, screen: Surface) -> bool:
        if self.in_preview:
            self.on_preview(screen)
            return False
        
        if self.ready:
            self.on_draw(screen)
            self.ready = False

        return True
    
    @abstractmethod 
    def on_start(self, start_pos: Vector2) -> None:
        pass

    @abstractmethod 
    def on_update(self, mouse_pos: Vector2) -> None:
        pass
    
    @abstractmethod 
    def on_preview(self, screen: Surface) -> None:
        pass

    @abstractmethod 
    def on_draw(self, screen: Surface) -> None:
        pass

class Circle(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.center = Vector2(0,0)
        self.end_pos = Vector2(0,0)
        self.radius = 0
    
    def on_start(self, start_pos: Vector2) -> None:
        self.center = start_pos
        self.end_pos = start_pos
        self.radius = 0

    def on_update(self, mouse_pos: Vector2) -> None:
        self.radius = round(self.center.distance_to(mouse_pos))
        self.end_pos = mouse_pos
    
    def on_preview(self, screen: Surface):
        pygame.draw.line(screen, Color("red"), self.center, self.end_pos, PREVIEW_WIDTH)
        pygame.draw.circle(screen, self.color, self.center, self.radius, PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        draw.aacircle(screen, int(self.center.x), int(self.center.y), self.radius, self.color)
        draw.filled_circle(screen, int(self.center.x), int(self.center.y), self.radius, self.color)

class Square(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.center = Vector2(0,0)
        self.dist = 0
    
    def on_start(self, start_pos: Vector2) -> None:
        self.center = start_pos
        self.dist = 0

    def on_update(self, mouse_pos: Vector2) -> None:
        self.dist = round(self.center.distance_to(mouse_pos))
   
    def calc_rect(self) -> Rect:
        topleft = self.center - Vector2(self.dist) / math.sqrt(2) 
        size = Vector2(self.dist) * math.sqrt(2)
        return Rect(topleft, size)

    def on_preview(self, screen: Surface):
        pygame.draw.rect(screen, self.color, self.calc_rect(), PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        draw.box(screen, self.calc_rect(), self.color)

class Rectangle(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.start_vertex = Vector2(0,0)
        self.end_vertex = Vector2(0,0)
    
    def on_start(self, start_pos: Vector2) -> None:
        self.start_vertex = start_pos
        self.end_vertex = start_pos

    def on_update(self, mouse_pos: Vector2) -> None:
        self.end_vertex = mouse_pos
   
    def calc_rect(self) -> Rect:
        topleft = Vector2(
            min(self.start_vertex.x, self.end_vertex.x),
            min(self.start_vertex.y, self.end_vertex.y) 
        )
        size = Vector2(
            abs(self.start_vertex.x - self.end_vertex.x), 
            abs(self.start_vertex.y - self.end_vertex.y)
        )
        return Rect(topleft, size)

    def on_preview(self, screen: Surface):
        pygame.draw.rect(screen, self.color, self.calc_rect(), PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        draw.box(screen, self.calc_rect(), self.color)

class RightTriangle(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.start_vertex = Vector2(0,0)
        self.end_vertex = Vector2(0,0)
    
    def on_start(self, start_pos: Vector2) -> None:
        self.start_vertex = start_pos
        self.end_vertex = start_pos

    def on_update(self, mouse_pos: Vector2) -> None:
        self.end_vertex = mouse_pos
   
    def calc_verticies(self):
        vertex1 = Vector2(self.start_vertex.x, self.end_vertex.y)
        vertex2 = Vector2(self.end_vertex.x, self.start_vertex.y)
        return (self.start_vertex, vertex1, vertex2)

    def on_preview(self, screen: Surface):
        pygame.draw.lines(screen, self.color, True, self.calc_verticies(), PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        pygame.draw.aalines(screen, self.color, True, self.calc_verticies())
        draw.filled_polygon(screen, self.calc_verticies(), self.color)

class Rhombus(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.start_vertex = Vector2(0,0)
        self.end_vertex = Vector2(0,0)
    
    def on_start(self, start_pos: Vector2) -> None:
        self.start_vertex = start_pos
        self.end_vertex = start_pos

    def on_update(self, mouse_pos: Vector2) -> None:
        self.end_vertex = mouse_pos
   
    def calc_verticies(self):
        vertex1 = Vector2(self.end_vertex.x, self.start_vertex.y)
        vertex2 = Vector2(self.start_vertex.x, self.end_vertex.y)
        vertex3 = Vector2(2*self.start_vertex.x-self.end_vertex.x, self.start_vertex.y) 
        vertex4 = Vector2(self.start_vertex.x, 2*self.start_vertex.y-self.end_vertex.y) 
        return (vertex1, vertex2, vertex3, vertex4)

    def on_preview(self, screen: Surface):
        pygame.draw.lines(screen, self.color, True, self.calc_verticies(), PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        pygame.draw.aalines(screen, self.color, True, self.calc_verticies())
        draw.filled_polygon(screen, self.calc_verticies(), self.color)

class EquilateralTriangle(Tool):
    def __init__(self) -> None:
        super().__init__()
        self.center = Vector2(0,0)
        self.dist = 0
    
    def on_start(self, start_pos: Vector2) -> None:
        self.center = start_pos
        self.dist = 0

    def on_update(self, mouse_pos: Vector2) -> None:
        self.dist = self.center.distance_to(mouse_pos)
   
    def calc_verticies(self):
        vertex1 = Vector2(self.center.x, self.center.y - self.dist)
        vertex2 = Vector2(self.center.x - math.sqrt(3) * self.dist / 2, self.center.y + self.dist / 2)
        vertex3 = Vector2(self.center.x + math.sqrt(3) * self.dist / 2, self.center.y + self.dist / 2)
        return (vertex1, vertex2, vertex3)

    def on_preview(self, screen: Surface):
        pygame.draw.lines(screen, self.color, True, self.calc_verticies(), PREVIEW_WIDTH)

    def on_draw(self, screen: Surface):
        pygame.draw.aalines(screen, self.color, True, self.calc_verticies())
        draw.filled_polygon(screen, self.calc_verticies(), self.color)

class Eraser:
    def __init__(self) -> None:
        self.start_vertex = Vector2(0,0)
        self.end_vertex = Vector2(0,0)
        self.radius = 1
        self.color = Color(0,0,0)
        self.ready = True

    def on_start(self, start_pos: Vector2) -> None:
        self.start_vertex = start_pos
        self.end_vertex = start_pos
        self.ready = False

    def on_update(self, mouse_pos: Vector2) -> None:
        self.start_vertex = self.end_vertex
        self.end_vertex = mouse_pos

    def on_draw(self, screen: Surface):
        utils.draw_line(
            screen, 
            self.start_vertex, self.end_vertex, self.color,
            self.radius
        ) 
