import pygame as pg

class Scene:
    def __init__(self, screen):
        self.speed = 20
        self.rad = 25
        self.max_x = screen.get_width()
        self.max_y = screen.get_height()
        self.pos = pg.math.Vector2(self.max_x / 2, self.max_y / 2)

    def update(self, dir_x, dir_y):
        next_pos_x = self.pos.x + dir_x * self.speed 
        next_pos_y = self.pos.y + dir_y * self.speed
        if next_pos_x >= self.rad and next_pos_x + self.rad <= self.max_x:
            self.pos.x = next_pos_x
        if next_pos_y >= self.rad and next_pos_y + self.rad <= self.max_y:
            self.pos.y = next_pos_y

    def render(self, screen):
        screen.fill("white")
        pg.draw.circle(screen, "red", self.pos, self.rad)

class App:
    def __init__(self, width, height, *, fps=60):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = fps
        self.scene = Scene(self.screen)

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.scene.update(0, -1)
                    elif event.key == pg.K_LEFT:
                        self.scene.update(-1, 0)
                    elif event.key == pg.K_RIGHT:
                        self.scene.update(1, 0)
                    elif event.key == pg.K_DOWN:
                        self.scene.update(0, 1)
                if event.type == pg.QUIT:
                    self.running = False
           
            self.scene.render(self.screen)
            pg.display.flip()
            self.clock.tick(self.fps)

    def __del__(self):
        pg.quit()

def main():
    app = App(700, 525)
    app.run()

main()
