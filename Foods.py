from pico2d import load_image


class Foods:
    def __init__(self, what, x, y):
        self.x = x
        self.y = 100 + y
        self.w = 50
        self.h = 50

        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass