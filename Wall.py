from pico2d import draw_rectangle, load_image


class Wall:
    image=None
    def __init__(self, left, bottom, right, top):

        self.x=(left + right) / 2
        self.y=(top + bottom) / 2
        self.w = right - left
        self.h = top - bottom
        if Wall.image==None:
            Wall.image = load_image('image\wall.png')
    def update(self):
        pass
    def handle_event(self):
        pass
    def move_to(self):
        pass
    def draw(self):
        Wall.image.clip_draw(0,0,Wall.image.w,Wall.image.h,self.x,self.y,self.w,self.h)
        draw_rectangle(*self.get_bb())
#충돌
    def get_bb(self):
       return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2
    def handle_collision(self, group, other):
        pass
    def __getstate__(self):
        left, bottom, right, top = self.get_bb()
        state = {"left" : left, "bottom" : bottom, "right" : right, "top" : top}
        return state
    def __setstate__(self, state):
        self.__init__(state["left"],state["bottom"],state["right"],state["top"])
