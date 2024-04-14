from abc import abstractmethod, ABC
import pygame
import pygame.gfxdraw

class Command(ABC):
    @abstractmethod
    def execute(self, image: pygame.Surface):
        pass

class OverlayCommand(Command):
    def __init__(self, command: Command):
        self.internal = command

    def execute(self, image: pygame.Surface):
        self.internal.execute(image)

class Empty(Command):
    def execute(self, image: pygame.Surface):
        pass

class DrawLine(Command):
    def __init__(self, start, end, color):
        self.start = start 
        self.end = end 
        self.color = color
    
    def execute(self, image: pygame.Surface):
        pygame.draw.aaline(image, self.color, self.start, self.end)

class DrawWideLine(Command):
    def __init__(self, start, end, width, color):
        self.start = start 
        self.end = end
        self.width = width
        self.color = color
        diff = start - end
        self.iterations = round(max(abs(diff.x), abs(diff.y)))
        
    def execute(self, image: pygame.Surface):
        for i in range(self.iterations):
            t = i / self.iterations
            coord = self.start.lerp(self.end, t)
            pygame.draw.circle(image, self.color, coord, self.width)

class DrawCircle(Command):
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def execute(self, image: pygame.Surface):
        pygame.gfxdraw.aacircle(image, int(self.center.x), int(self.center.y), round(self.radius), self.color)
        pygame.gfxdraw.filled_circle(image, int(self.center.x), int(self.center.y), 
                                     round(self.radius), self.color)

class DrawRect(Command):
    def __init__(self, rect, color):
        self.rect = rect 
        self.color = color

    def execute(self, image: pygame.Surface):
        pygame.draw.rect(image, self.color, self.rect)

class DrawPolygon(Command):
    def __init__(self, points, color):
        self.points = points 
        self.color = color

    def execute(self, image: pygame.Surface):
        pygame.gfxdraw.aapolygon(image, self.points, self.color)
        pygame.gfxdraw.filled_polygon(image, self.points, self.color)

