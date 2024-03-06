import pygame as pg
import datetime as dt
import os

FILE_DIR = os.path.dirname(__file__)

def load_image(src):
    return pg.image.load(os.path.join(FILE_DIR, src))

def draw_rotated(screen, image, angle, offset):
    rect = image.get_rect()
    rotated_image = pg.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=rect.center)
    rotated_rect.x += offset[0]
    rotated_rect.y += offset[1]
    screen.blit(rotated_image, rotated_rect)

class Scene:
    def __init__(self):
        clock = load_image("images/mainclock.png")
        left_arm = load_image("images/leftarm.png")
        right_arm = load_image("images/rightarm.png")
        
        self.clock = pg.transform.scale_by(clock, 0.5)
        self.left_arm = pg.transform.scale_by(left_arm, 0.5)
        self.right_arm = pg.transform.scale_by(right_arm, 0.5)
        self.right_arm = pg.transform.rotate(self.right_arm, -45)

    def render(self, screen):
        time = dt.datetime.now()
        
        screen.blit(self.clock, (0, 0))
        draw_rotated(screen, self.left_arm, -time.second * 6, (335, 0))
        draw_rotated(screen, self.right_arm, -time.minute * 6, (-80, -170))

class App:
    def __init__(self, width, height, *, fps=60):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = fps
        self.scene = Scene()

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
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

