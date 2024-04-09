import os, sys
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
import engine

import pygame
import utils
import tools
import canvas

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CANVAS_WIDTH = SCREEN_WIDTH
CANVAS_HEIGHT = int(0.8 * SCREEN_HEIGHT)

class MainScene(engine.Scene):
    def _on_load(self):
        self.canvas = canvas.Canvas(pygame.Rect(0, SCREEN_HEIGHT - CANVAS_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT))
        self.tool = tools.EraserTool(self.canvas)

    def _on_event(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.tool.on_mouse_down(event.button, event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.tool.on_mouse_up(event.button, event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.canvas.tool_color = utils.random_color()
            elif event.key == pygame.K_u:
                self.canvas.undo()
            elif event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:
                self.canvas.redo()

    def _on_update(self):
        self.tool.update()
        self.canvas.update(self.app.screen)

def main():
    app = engine.Application((SCREEN_WIDTH, SCREEN_HEIGHT), 'Paint')
    app.scene_manager.add_scene(MainScene())
    app.scene_manager.switch_to(0)
    app.run()

main()
