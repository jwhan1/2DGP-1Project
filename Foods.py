from pico2d import load_image, draw_rectangle


class Foods:
    def __init__(self, what, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50

        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
#충돌
    def get_bb(self):
       return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            if group == 'charater:food' and  (other.onhand == None or other.onhand == self):
                    self.x, self.y = 750, 50

