import pygame as pg
import pygame.mixer_music as music
import os

FILE_DIR = os.path.dirname(__file__)

class Player:
    def __init__(self):
        self.playlist = [
            "music/Darude – Sandstorm Radio Edit.mp3",
            "music/Rick Astley - Never Gonna Give You Up.mp3"
        ]
        self.current_track = 0
        music.set_volume(0.6)
        self.play_track(self.current_track)

    def play_track(self, index):
        music.load(os.path.join(FILE_DIR, self.playlist[index]))
        music.play()

    def toggle(self):
        if music.get_busy():
            music.pause()
        else:
            music.unpause()

    def play_next(self):
        if self.current_track + 1 < len(self.playlist):
            self.current_track += 1
            self.play_track(self.current_track)

    def play_prev(self):
        if self.current_track > 0:
            self.current_track -= 1
            self.play_track(self.current_track) 

    def render(self, screen):
        screen.fill("blue")

class App:
    def __init__(self, width, height, *, fps=60):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        self.clock = pg.time.Clock()
        self.fps = fps
        self.player = Player()

    def run(self):
        self.running = True
        while self.running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE or event.key == pg.K_k:
                        self.player.toggle()
                    elif event.key == pg.K_j:
                        self.player.play_prev()
                    elif event.key == pg.K_l:
                        self.player.play_next()
                if event.type == pg.QUIT:
                    self.running = False
           
            self.player.render(self.screen)
            pg.display.flip()
            self.clock.tick(self.fps)

    def __del__(self):
        pg.quit()

def main():
    app = App(700, 525)
    app.run()

main()
