import pygame
import pygame.gfxdraw
import collections

CANVAS_COLOR = (255, 255, 255)
DEFAULT_TOOL_COLOR = (0, 0, 0)
HISTORY_LENGTH = 32

class DrawLine:
    def __init__(self, start, end, canvas):
        self.start = canvas.rel_coord(start)
        self.end = canvas.rel_coord(end)
    
    def __call__(self, image, color):
        pygame.draw.aaline(image, color, self.start, self.end)

class DrawWideLine:
    def __init__(self, start, end, width, canvas):
        self.start = canvas.rel_coord(start)
        self.end = canvas.rel_coord(end)
        self.width = width
        diff = start - end
        self.iterations = round(max(abs(diff.x), abs(diff.y)))
        
    def __call__(self, image, color):
        for i in range(self.iterations):
            t = i / self.iterations
            coord = self.start.lerp(self.end, t)
            pygame.gfxdraw.aacircle(image, round(coord.x), round(coord.y), self.width, color) 
            pygame.gfxdraw.filled_circle(image, round(coord.x), round(coord.y), self.width, color)
  
class DrawCircle:
    def __init__(self, center, radius, canvas):
        self.center = canvas.rel_coord(center)
        self.radius = radius

    def __call__(self, image, color):
        pygame.gfxdraw.aacircle(image, int(self.center.x), int(self.center.y), round(self.radius), color)
        pygame.gfxdraw.filled_circle(image, int(self.center.x), int(self.center.y), round(self.radius), color)

class DrawRect:
    def __init__(self, rect, canvas):
        self.rect = pygame.Rect(canvas.rel_coord(rect.topleft), rect.size)

    def __call__(self, image, color):
        pygame.draw.rect(image, color, self.rect)

class DrawPolygon:
    def __init__(self, points, canvas):
        self.points = tuple(map(canvas.rel_coord, points))

    def __call__(self, image, color):
        pygame.gfxdraw.aapolygon(image, self.points, color)
        pygame.gfxdraw.filled_polygon(image, self.points, color)

class Canvas:
    def __init__(self, rect):
        self.rect = rect
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(CANVAS_COLOR)
        self.frame_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.final_image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.tool_color = DEFAULT_TOOL_COLOR
        self.undo_stack = collections.deque(maxlen=HISTORY_LENGTH + 1)
        self.redo_stack = collections.deque(maxlen=HISTORY_LENGTH)
        self.undo_stack.append(self.image.copy())
        
    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.image = self.undo_stack[-1].copy()

    def redo(self):
        if len(self.redo_stack) > 0:
            self.undo_stack.append(self.redo_stack.pop())
            self.image = self.undo_stack[-1].copy()

    def exec(self, command, frame_only = False):
        image = self.frame_image if frame_only else self.image
        command(image, self.tool_color)
        if not frame_only:
            self.redo_stack.clear()
            self.undo_stack.append(self.image.copy())    

    def update(self, screen):
        self.final_image.blit(self.image, (0, 0))
        self.final_image.blit(self.frame_image, (0, 0))
        self.frame_image.fill((0, 0, 0, 0))
        screen.blit(self.final_image, self.rect)

    def rel_coord(self, coord):
        offset = pygame.Vector2(self.rect.topleft) 
        return pygame.Vector2(coord) - offset 
