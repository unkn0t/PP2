import pygame
import sys
import os
import random
import psycopg2
import config
from collections import deque
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import engine

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GrassCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (75, 245, 66)

class Board:
    def __init__(self, x, y, width, height, cell_size):
        self.pos = (x, y)
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.cells = []
        self.dirty_cells = []

        for x in range(width):
            self.cells.append([])
            for y in range(height):
                self.cells[-1].append(GrassCell(x, y))
                self.dirty_cells.append(GrassCell(x, y))

    def update_cells(self, cells):
        for cell in cells:
            self.cells[cell.x][cell.y] = cell
        self.dirty_cells.extend(cells)

    def redraw(self, screen):
        for cell in self.dirty_cells:
            x = self.pos[0] + cell.x * self.cell_size 
            y = self.pos[1] + cell.y * self.cell_size
            pygame.draw.rect(screen, cell.color, pygame.Rect(x, y, self.cell_size, self.cell_size))
        self.dirty_cells.clear()

class SnakeCell(Cell):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (66, 105, 245)

SNAKE_EAT = pygame.event.custom_type()
SNAKE_COLLIDE = pygame.event.custom_type()
LEVEL_INCREASED = pygame.event.custom_type()

SNAKE_LEVEL_ACC = 1.1

class Snake:
    def __init__(self, x, y, length, dir, speed):
        self.speed = speed
        self.acc_time = 0
        self.dir = dir
        self.cells = deque([])

        for _ in range(length):
            self.cells.append(SnakeCell(x, y))
            x -= dir[0]
            y -= dir[1]
        
        self.dirty_cells = list(self.cells)
    
    def set_horizontal_dir(self, dir_x):
        if self.dir[0] == 0: 
            self.dir = (dir_x, 0) 
    
    def set_vertical_dir(self, dir_y):
        if self.dir[1] == 0: 
            self.dir = (0, dir_y) 

    def eat(self, board: Board) -> bool:
        cell = board.cells[self.cells[0].x][self.cells[0].y]
        if isinstance(cell, Food):
            pygame.event.post(pygame.event.Event(SNAKE_EAT, {'score': cell.score}))
            return True
        return False

    def collide(self, head_x, head_y, board: Board) -> bool:
        for cell in self.cells:
            if cell.x == head_x and cell.y == head_y:
                pygame.event.post(pygame.event.Event(SNAKE_COLLIDE))
                return True
                
        if head_x < 0 or head_y < 0 or head_x >= board.width or head_y >= board.height:
            pygame.event.post(pygame.event.Event(SNAKE_COLLIDE))
            return True

        return False 
    
    def move(self, board: Board, dt: float):
        if self.acc_time < 1.0 / self.speed:
            self.acc_time += dt
            return

        self.acc_time = 0.0

        new_head_x = self.cells[0].x + self.dir[0]
        new_head_y = self.cells[0].y + self.dir[1]
        if self.collide(new_head_x, new_head_y, board):
            return

        self.cells.appendleft(SnakeCell(new_head_x, new_head_y))
        self.dirty_cells.append(self.cells[0])
        if not self.eat(board):
            tail = self.cells.pop()
            self.dirty_cells.append(GrassCell(tail.x, tail.y))

    def redraw(self, board: Board):
        board.update_cells(self.dirty_cells)
        self.dirty_cells.clear()

class Food:
    def __init__(self):
        self.score = 0 

class AppleCell(Cell, Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (217, 2, 27)
        self.score = 1

class GoldenAppleCell(Cell, Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255,191,0)
        self.score = 2

DESTROY_FAST_FOOD = pygame.event.custom_type()

class FastFoodCell(Cell, Food):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (84, 10, 209)
        self.score = 2
        pygame.time.set_timer(pygame.event.Event(DESTROY_FAST_FOOD, {'x': self.x, 'y': self.y}), 3000, 1)

class FoodSpawner:
    def __init__(self):
        self.dirty_cells = []
    
    def spawn(self, board: Board):
        while True:
            x = random.randint(0, board.width - 1)
            y = random.randint(0, board.height - 1)
            if isinstance(board.cells[x][y], GrassCell):
                ty = random.randint(1, 20)
                if ty == 7:
                    self.dirty_cells.append(GoldenAppleCell(x, y))
                elif ty == 13 or ty == 17:
                    self.dirty_cells.append(FastFoodCell(x, y))
                else:
                    self.dirty_cells.append(AppleCell(x, y))
                break
        
    def redraw(self, board: Board):
        board.update_cells(self.dirty_cells)
        self.dirty_cells.clear()

class Score:
    def __init__(self, max_score: int):
        self.score = 0
        self.level = 0
        self.level_threshold = 3
        self.max_score = max_score
        self.score_text = TextUI('SCORE', 20, 'white', True)
        self.level_text = TextUI('LEVEL', 20, 'white', True)
        self.max_score_text = TextUI('MAX SCORE', 20, 'white', True)
        self.score_number_text = TextUI(str(self.score), 30, 'grey', True)
        self.level_number_text = TextUI(str(self.level), 30, 'grey', True)
        self.max_score_number_text = TextUI(str(self.max_score), 30, 'grey', True)

    def add(self, value: int):
        self.score += value
        if self.score >= round((self.level + 1) * self.level_threshold):
            self.level += 1
            self.level_threshold *= 1.1
            pygame.event.post(pygame.event.Event(LEVEL_INCREASED))
        self.max_score = max(self.max_score, self.score)
        self.score_number_text = TextUI(str(self.score), 30, 'grey', True)
        self.level_number_text = TextUI(str(self.level), 30, 'grey', True)
        self.max_score_number_text = TextUI(str(self.max_score), 30, 'grey', True)

    def draw(self, screen: pygame.Surface):
        screen.fill((41, 40, 38), pygame.Rect(0, 0, screen.get_width(), 80))
        self.score_text.draw(screen, (60, 20))
        self.level_text.draw(screen, (720-60, 20))
        self.max_score_text.draw(screen, (360, 20))
        self.score_number_text.draw(screen, (60, 50))
        self.level_number_text.draw(screen, (720-60, 50))
        self.max_score_number_text.draw(screen, (360, 50))
        pygame.display.update(0, 0, screen.get_width(), 80)

class GamePlayScene(engine.Scene):
    def _on_load(self):
        self.board = Board(0, 80, 20, 20, 36)
        self.snake = Snake(10, 10, 4, (1, 0), speed=6.0)
        self.food_spawner = FoodSpawner()
        
        if len(sys.argv) < 2:
            print("Provide username as argument")
            exit(1)

        self.username = sys.argv[1]
        max_score = 0
        GET_MAXSCORE_SQL = """
            SELECT max_score FROM users WHERE username = %s
        """
        CREATE_NEW_USER_SQL = """
            INSERT INTO users (username, max_score) VALUES (%s, 0) 
        """

        cfg = config.load()
        with psycopg2.connect(**cfg) as db:
            with db.cursor() as curs:
                curs.execute(GET_MAXSCORE_SQL, (self.username,))
                row = curs.fetchone()
                if row:
                    max_score = row[0]
                else:
                    curs.execute(CREATE_NEW_USER_SQL, (self.username,))

        self.score = Score(max_score)
        self.food_spawner.spawn(self.board)
    
    def _on_unload(self):
        SAVE_MAXSCORE_SQL = """
            UPDATE users SET max_score = %s WHERE username = %s
        """
        
        cfg = config.load()
        with psycopg2.connect(**cfg) as db:
            with db.cursor() as curs:
                curs.execute(SAVE_MAXSCORE_SQL, (self.score.max_score, self.username))
            
    def _on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.snake.set_vertical_dir(-1)
            elif event.key == pygame.K_s:
                self.snake.set_vertical_dir(1)
            elif event.key == pygame.K_a:
                self.snake.set_horizontal_dir(-1)
            elif event.key == pygame.K_d:
                self.snake.set_horizontal_dir(1)
        elif event.type == SNAKE_COLLIDE:
            self.app.scene_manager.switch_to(1)
        elif event.type == SNAKE_EAT:
            self.score.add(event.score)
            self.food_spawner.spawn(self.board)
        elif event.type == LEVEL_INCREASED:
            self.snake.speed *= SNAKE_LEVEL_ACC
        elif event.type == DESTROY_FAST_FOOD:
            if type(self.board.cells[event.x][event.y]) is FastFoodCell:
                self.board.update_cells([AppleCell(event.x, event.y)])

    def _on_update(self):
        self.snake.move(self.board, self.app.delta_time)
        self.food_spawner.redraw(self.board)
        self.snake.redraw(self.board)
        self.board.redraw(self.app.screen)
        self.score.draw(self.app.screen)

class TextUI:
    def __init__(self, text: str, size: int, color, bold=False):
        self.font = pygame.font.SysFont('Iosevka', size, bold)
        self.text = self.font.render(text, True, color)
        self.center = pygame.Vector2(self.text.get_rect().center)

    def draw(self, screen: pygame.Surface, center):
        pos = pygame.Vector2(center) - self.center
        screen.blit(self.text, pos)

class GameOverScene(engine.Scene):
    def _on_load(self):
        self.game_over_text = TextUI('GAME OVER', 50, 'white', True) 
        self.restart_text = TextUI('Press SPACE to restart', 25, 'grey', True)
        screen_center = self.app.screen.get_rect().center

        self.app.screen.fill('black')
        self.game_over_text.draw(self.app.screen, screen_center)
        self.restart_text.draw(self.app.screen, (screen_center[0], 
                                                 screen_center[1] + 2 * self.game_over_text.center[1]))

    def _on_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.app.scene_manager.switch_to(0)

def main():
    app = engine.Application((720, 800), 'Snake')
    app.scene_manager.add_scene(GamePlayScene())
    app.scene_manager.add_scene(GameOverScene())
    app.scene_manager.switch_to(0)
    app.run(fps=144)

if __name__ == "__main__":
    main()
