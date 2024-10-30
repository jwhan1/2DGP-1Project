from pico2d import load_image


class Charater:
    def __init__(self, what):
        self.x = 50
        self.y = 550
        self.w = 100
        self.h = 100
        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass