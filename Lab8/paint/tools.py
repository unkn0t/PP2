import pygame
import pygame.gfxdraw
import math
import canvas

M_ROOT2 = math.sqrt(2)
M_ROOT3 = math.sqrt(3)

class ToolBase:
    def __init__(self, canvas):
        self.canvas = canvas
        self.active = False
        self.start = pygame.Vector2(0)
    
    def on_mouse_down(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            self.start = pygame.Vector2(pos)
            self.active = True

class LineTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            self.canvas.exec(canvas.DrawLine(self.start, pos, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        self.canvas.exec(canvas.DrawLine(self.start, pos, self.canvas), frame_only=True)

class CircleTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            radius = self.start.distance_to(pos)
            self.canvas.exec(canvas.DrawCircle(self.start, radius, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        radius = self.start.distance_to(pos)
        self.canvas.exec(canvas.DrawCircle(self.start, radius, self.canvas), frame_only=True)

class RectangleTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            rect = self.calc_rect(pygame.Vector2(pos))
            self.canvas.exec(canvas.DrawRect(rect, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        rect = self.calc_rect(pygame.Vector2(pos))
        self.canvas.exec(canvas.DrawRect(rect, self.canvas), frame_only=True)

    def calc_rect(self, end) -> pygame.Rect:
        topleft = (min(self.start.x, end.x), min(self.start.y, end.y))
        size = abs((self.start - end).elementwise())
        return pygame.Rect(topleft, size)

class SquareTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            rect = self.calc_rect(pygame.Vector2(pos))
            self.canvas.exec(canvas.DrawRect(rect, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        rect = self.calc_rect(pygame.Vector2(pos))
        self.canvas.exec(canvas.DrawRect(rect, self.canvas), frame_only=True)

    def calc_rect(self, end) -> pygame.Rect:
        dist = pygame.Vector2(self.start.distance_to(end))
        topleft = self.start - dist / M_ROOT2 
        size = dist * M_ROOT2
        return pygame.Rect(topleft, size)

class RightTriangleTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            verticies = self.calc_verticies(pygame.Vector2(pos))
            self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        verticies = self.calc_verticies(pygame.Vector2(pos))
        self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas), frame_only=True)

    def calc_verticies(self, end):
        vertex1 = pygame.Vector2(self.start.x, end.y)
        vertex2 = pygame.Vector2(end.x, self.start.y)
        return (self.start, vertex1, vertex2)

class RhombusTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            verticies = self.calc_verticies(pygame.Vector2(pos))
            self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        verticies = self.calc_verticies(pygame.Vector2(pos))
        self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas), frame_only=True)

    def calc_verticies(self, end):
        vertex1 = pygame.Vector2(end.x, self.start.y)
        vertex2 = pygame.Vector2(self.start.x, end.y)
        vertex3 = pygame.Vector2(2 * self.start.x - end.x, self.start.y) 
        vertex4 = pygame.Vector2(self.start.x, 2 * self.start.y - end.y) 
        return (vertex1, vertex2, vertex3, vertex4)

class EquilateralTriangleTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            verticies = self.calc_verticies(pygame.Vector2(pos))
            self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        verticies = self.calc_verticies(pygame.Vector2(pos))
        self.canvas.exec(canvas.DrawPolygon(verticies, self.canvas), frame_only=True)

    def calc_verticies(self, end):
        dist = self.start.distance_to(end)
        vertex1 = self.start - pygame.Vector2(0, dist)
        vertex2 = self.start + pygame.Vector2(-M_ROOT3, 1) * dist / 2
        vertex3 = self.start + pygame.Vector2(M_ROOT3, 1) * dist / 2
        return (round(vertex1), round(vertex2), round(vertex3))

class EraserTool(ToolBase):
    def on_mouse_up(self, button, pos):
        if button == pygame.BUTTON_LEFT:
            self.canvas.exec(canvas.DrawWideLine(self.start, pos, 1, self.canvas))
            self.active = False

    def update(self):
        if not self.active:
            return

        pos = pygame.mouse.get_pos()
        self.canvas.exec(canvas.DrawWideLine(self.start, pos, 1, self.canvas))
        self.start = pygame.Vector2(pos)
