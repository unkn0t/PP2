import pygame
import random
import json
import os
import pygame_gui

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from engine.app import Application
from engine.scene import Scene

DIRNAME = os.path.dirname(__file__)
SNAKE_ATE_APPLE = pygame.event.custom_type()

class Grid:
    def __init__(self, size, cell_size):
        self.cell_size = cell_size
        self.size = size
        self.cells = [[pygame.Color(0,0,0) for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.used_cells = []
    
    def _rect_from_coord(self, x: int, y: int):
        return pygame.Rect((x * self.cell_size[0], y * self.cell_size[1]), self.cell_size)
    
    def get_cell(self, x: int, y: int) -> pygame.Color:
        return self.cells[y][x]
    
    def get_free_cells(self):
        free_cells = []
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if not (x, y) in self.used_cells:
                    free_cells.append((x, y))
        return free_cells

    def set_cell(self, x: int, y: int, color: pygame.Color):
        self.cells[y][x] = color
        self.used_cells.append((x, y))

    def set_permanent_cell(self, x: int, y: int, color: pygame.Color):
        self.cells[y][x] = color

    def is_valid_cell(self, x: int, y: int):
        return x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]
        
    def clear(self):
        for x, y in self.used_cells:
            self.cells[y][x] = pygame.Color(0,0,0)
        self.used_cells.clear() 
            
    def draw(self, screen: pygame.Surface):
        for y in range(self.size[1]):
            for x in range(self.size[0]): 
                pygame.draw.rect(screen, self.cells[y][x], self._rect_from_coord(x,y))

    def debug_draw(self, screen: pygame.Surface):
        width, height = screen.get_size()
        for x in range(self.size[0]):
            pygame.draw.line(screen, 'white', (self.cell_size[0] * x, 0), (self.cell_size[0] * x, height))
        
        for y in range(self.size[1]):
            pygame.draw.line(screen, 'white', (0, self.cell_size[1] * y), (width, self.cell_size[1] * y))

class FoodSpawner:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.food_color = pygame.Color(255, 0, 0)
        self.spawn()
    
    def _spawn_impl(self, x: int, y: int):
        self.grid.set_permanent_cell(x, y, self.food_color)

    def spawn(self):
        cell = random.choice(self.grid.get_free_cells())
        self._spawn_impl(cell[0], cell[1])

class Snake:
    def __init__(self, head_pos, grid: Grid):
        self.segments = [head_pos]
        self.grid = grid
        self.color = pygame.Color(0, 128, 128)
        self.accumulated_time = 0.0
        self.step_time = 0.15 
        self.alive = True
    
    def _update_cells(self):
        for x, y in self.segments:
            self.grid.set_cell(x, y, self.color)  

    def _increase_tail(self, dir):
        new_tail_x = dir[0] + self.segments[0][0]
        new_tail_y = dir[1] + self.segments[0][1]
        self.segments.insert(0, (new_tail_x, new_tail_y))

    def move(self, dir, dt: float):
        if not self.alive:
            return None

        if self.accumulated_time < self.step_time:
            self.accumulated_time += dt
        else:
            self.accumulated_time -= self.step_time
            
            new_head_x = dir[0] + self.segments[-1][0]
            new_head_y = dir[1] + self.segments[-1][1]
            self.segments.append((new_head_x, new_head_y))
            self.segments.pop(0)
            
            if not self.grid.is_valid_cell(new_head_x, new_head_y):
                self.alive = False
                return None 
            
            if self.segments[-1] in self.segments[0:-1]:
                self.alive = False
                return None

            if self.grid.get_cell(new_head_x, new_head_y) == pygame.Color(255, 0, 0):
                pygame.event.post(pygame.Event(SNAKE_ATE_APPLE))
                self._increase_tail(dir)
        
        self._update_cells()

class GameOverScene(Scene):
    def _on_load(self):
        file = open(DIRNAME + '/data.json')
        data = json.load(file)
        file.close()
        self.score = data['score']
        self.max_score = data['max_score']
        width, height = self.app.screen.get_size()
        self.ui_manager = pygame_gui.UIManager((width, height), DIRNAME + '/theme.json')
        label_width = 200
        label_height = 50
        self.score_ui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(width // 2 - label_width // 2, height // 2 - label_height // 2, label_width, label_height),
            text=f'Score: {self.score}',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(object_id='#game_over_label')
        )
        self.max_score_ui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(width // 2 - label_width // 2, height // 2 + label_height // 2, label_width, label_height),
            text=f'Max score: {self.max_score}',
            manager=self.ui_manager,
            object_id=pygame_gui.core.ObjectID(object_id='#game_over_label')
        )

    def _on_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self.app.is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.manager.switch_to(0)
        else:
            self.ui_manager.process_events(event)

    def _on_update(self):
        self.ui_manager.update(self.app.delta_time)

    def _on_redraw(self):
        self.app.screen.fill('black')
        self.ui_manager.draw_ui(self.app.screen)

class PlayScene(Scene):
    def _on_load(self):
        width, height = self.app.screen.get_size()
        self.grid = Grid((width // 30, height // 30), (30, 30))
        self.snake = Snake((10, 10), self.grid)
        self.snake_dir = (1, 0)
        self.food_spawner = FoodSpawner(self.grid)
        self.level = 0
        self.score = 0
        self.ui_manager = pygame_gui.UIManager((width, height), DIRNAME + '/theme.json')
        self.level_ui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 100, 30),
            text=f'Level: {self.score}',
            manager=self.ui_manager
        )
        self.score_ui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(400, 10, 100, 30),
            text=f'Score: {self.score}',
            manager=self.ui_manager,
        )
       
        if os.path.exists(DIRNAME + '/data.json'):
            file = open(DIRNAME + '/data.json')
            self.max_score = json.load(file)['max_score']
        else:
            self.max_score = 0
        
        self.max_score_ui = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(400, 40, 150, 30),
            text=f'Max score: {self.max_score}',
            manager=self.ui_manager,
        )

    def _on_unload(self):
        self.ui_manager.clear_and_reset()
        file = open(DIRNAME + '/data.json', 'w')
        json.dump({'score': self.score, 'max_score': self.max_score}, file)
        file.close()

    def _on_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.app.is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if self.snake_dir[0] == 0: self.snake_dir = (-1, 0)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if self.snake_dir[0] == 0: self.snake_dir = (1, 0)
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                if self.snake_dir[1] == 0: self.snake_dir = (0, -1)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if self.snake_dir[1] == 0: self.snake_dir = (0, 1)
        elif event.type == SNAKE_ATE_APPLE:
            self.food_spawner.spawn()
            self.score += 1
            self.score_ui.set_text(f'Score: {self.score}')
            if self.score > self.max_score:
                self.max_score = self.score
                self.max_score_ui.set_text(f'Max score: {self.max_score}')
            if (self.score + 1) % 4 == 0:
                self.level += 1
                self.snake.step_time *= 0.9
                self.level_ui.set_text(f'Level: {self.level}')
        else:
            self.ui_manager.process_events(event)

    def _on_update(self):
        self.grid.clear()
        self.snake.move(self.snake_dir, self.app.delta_time)
        self.ui_manager.update(self.app.delta_time)

        if not self.snake.alive:
            self.manager.switch_to(1)

    def _on_redraw(self):
        self.app.screen.fill('black')
        self.grid.draw(self.app.screen)
        self.ui_manager.draw_ui(self.app.screen)

def main():
    app = Application((720, 720), 'Snake')
    app.scene_manager.add_scene(PlayScene())
    app.scene_manager.add_scene(GameOverScene())
    app.scene_manager.switch_to(0)
    app.run()

if __name__ == "__main__":
    main()
