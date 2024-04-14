from abc import abstractmethod
import pygame
import pygame.gfxdraw
from pygame import Vector2, Rect
import math
import draw
import draw.command as command

M_ROOT2 = math.sqrt(2)
M_ROOT3 = math.sqrt(3)

from enum import Enum

class ToolState(Enum):
    INACTIVE = 0,
    IN_PROGRESS = 1,
    FINISHED = 2,

class ToolBase:
    def __init__(self):
        self.state = ToolState.INACTIVE
        self.start = Vector2(0)
        self.end = Vector2(0)

    def activate(self, pos):
        self.start = Vector2(pos)
        self.end = Vector2(pos)
        self.state = ToolState.IN_PROGRESS

    def update(self, pos):
        if self.state == ToolState.IN_PROGRESS:
            self.end = Vector2(pos)

    def finish(self, pos):
        if self.state == ToolState.IN_PROGRESS:
            self.end = Vector2(pos)
            self.state = ToolState.FINISHED
    
    @abstractmethod
    def getCommand(self, color: pygame.Color) -> draw.Command:
        pass

class Line(ToolBase):
    def getCommand(self, color: pygame.Color) -> draw.Command:
        res = command.DrawLine(self.start, self.end, color)
        if self.state == ToolState.INACTIVE:
            return command.Empty()
        elif self.state == ToolState.IN_PROGRESS:
            return command.OverlayCommand(res)
        else:
            self.state = ToolState.INACTIVE
            return res

class Circle(ToolBase):
    def getCommand(self, color: pygame.Color) -> draw.Command:
        radius = self.start.distance_to(self.end)
        res = command.DrawCircle(self.start, radius, color)
        if self.state == ToolState.INACTIVE:
            return command.Empty()
        elif self.state == ToolState.IN_PROGRESS:
            return command.OverlayCommand(res)
        else:
            self.state = ToolState.INACTIVE
            return res

class Rectangle(ToolBase):
    def getCommand(self, color: pygame.Color) -> draw.Command:
        rect = self.calculateRect()
        res = command.DrawRect(rect, color)
        if self.state == ToolState.INACTIVE:
            return command.Empty()
        elif self.state == ToolState.IN_PROGRESS:
            return command.OverlayCommand(res)
        else:
            self.state = ToolState.INACTIVE
            return res

    def calculateRect(self) -> Rect:
        topleft = (min(self.start.x, self.end.x), min(self.start.y, self.end.y))
        size = abs((self.start - self.end).elementwise())
        return Rect(topleft, size)

class Square(Rectangle):
    def calculateRect(self) -> Rect:
        topleft = (min(self.start.x, self.end.x), min(self.start.y, self.end.y))
        size = Vector2(max(abs(self.start.x - self.end.x), abs(self.start.y - self.end.y)))
        return Rect(topleft, size)

class RightTriangle(ToolBase):
    def getCommand(self, color: pygame.Color) -> draw.Command:
        points = self.calculatePoints()
        res = command.DrawPolygon(points, color)
        if self.state == ToolState.INACTIVE:
            return command.Empty()
        elif self.state == ToolState.IN_PROGRESS:
            return command.OverlayCommand(res)
        else:
            self.state = ToolState.INACTIVE
            return res

    def calculatePoints(self):
        vertex1 = Vector2(self.start.x, self.end.y)
        vertex2 = Vector2(self.end.x, self.start.y)
        return [self.start, vertex1, vertex2]

class Rhombus(RightTriangle):
    def calculatePoints(self):
        vertex1 = Vector2(self.end.x, self.start.y)
        vertex2 = Vector2(self.start.x, self.end.y)
        vertex3 = Vector2(2 * self.start.x - self.end.x, self.start.y) 
        vertex4 = Vector2(self.start.x, 2 * self.start.y - self.end.y) 
        return [vertex1, vertex2, vertex3, vertex4]

class EquilTriangle(RightTriangle):
    def calculatePoints(self):
        dist = self.start.distance_to(self.end)
        vertex1 = self.start - Vector2(0, dist)
        vertex2 = self.start + Vector2(-M_ROOT3, 1) * dist / 2
        vertex3 = self.start + Vector2(M_ROOT3, 1) * dist / 2
        return [vertex1, vertex2, vertex3]

class Eraser(ToolBase):
    def __init__(self):
        super().__init__()
        self.radius = 5
        
    def getCommand(self, color: pygame.Color) -> draw.Command:
        res = command.DrawWideLine(self.start, self.end, self.radius, color)
        if self.state == ToolState.INACTIVE:
            return command.Empty()
        elif self.state == ToolState.IN_PROGRESS:
            self.start = self.end
            return res
        else:
            self.state = ToolState.INACTIVE
            return res
