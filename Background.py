from pico2d import load_image


class Background:
    def __init__(self, what):
        if what == 'background':
            self.x = 400
            self.y = 300
            self.image = load_image(f'image/{what}.png')
            self.w = self.image.w
            self.h = self.image.h
            self.imgW = self.image.w
            self.imgH = self.image.h
        elif what == 'floor':
            self.x = 400
            self.y = 50
            self.w = 800
            self.h = 100
            self.image = load_image(f'image/{what}.png')
            self.imgW = self.image.w
            self.imgH = self.image.h

    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
    def handle_event(self, event):
        pass