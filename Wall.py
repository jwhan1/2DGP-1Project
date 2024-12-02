from pico2d import draw_rectangle


class Wall:
    def __init__(self, left, bottom, right, top):
        self.x=(left + right) / 2
        self.y=(top + bottom) / 2
        self.w = right - left
        self.h = top - bottom
    def update(self):
        pass
    def handle_event(self):
        pass
    def move_to(self):
        pass
    def draw(self):
        draw_rectangle(*self.get_bb())
#충돌
    def get_bb(self):
       return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2
    def handle_collision(self, group, other):
        pass
