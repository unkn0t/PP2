import pygame.gfxdraw as draw
from pygame import Color, Surface, Vector2
import random

def draw_gradient_line(surface: Surface, 
        start_coord: Vector2, start_color: Color, 
        end_coord: Vector2, end_color: Color, width = 1):
    diff = start_coord - end_coord
    iterations = max(abs(diff.x), abs(diff.y))
    for i in range(int(iterations)):
        t = i / iterations
        coord = start_coord.lerp(end_coord, t)
        color = start_color.lerp(end_color, t)
        draw.aacircle(surface, round(coord.x), round(coord.y), width, color)
        draw.filled_circle(surface, round(coord.x), round(coord.y), width, color)

def draw_line(surface: Surface, 
        start_coord: Vector2, end_coord: Vector2, color: Color, width = 1):
    diff = start_coord - end_coord
    iterations = max(abs(diff.x), abs(diff.y))
    for i in range(int(iterations)):
        t = i / iterations
        coord = start_coord.lerp(end_coord, t)
        draw.aacircle(surface, round(coord.x), round(coord.y), width, color)
        draw.filled_circle(surface, round(coord.x), round(coord.y), width, color)

def random_color() -> Color:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return Color(r, g, b)
