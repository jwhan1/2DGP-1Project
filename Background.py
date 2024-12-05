from pico2d import load_image,get_canvas_width,get_canvas_height


class Background:
    def __init__(self):
        self.image = load_image('image/background.png')
        self.x = get_canvas_width()/2
        self.y = get_canvas_height()/2
        self.w = get_canvas_width()
        self.h = get_canvas_height()

        self.itemUI = load_image('image/foodUI.png')
    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.w, self.x, self.y, self.w, self.h)
        
        
        self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-250, 50, 50, 50)
        self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-200, 50, 50, 50)
        self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-150, 50, 50, 50)
        self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-100, 50, 50, 50)
        self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-50, 50, 50, 50)

    def handle_event(self, event):
        pass
 
    def get_bb(self):
        pass

    def handle_collision(self, group, other):
            pass
    def __getstate__(self):
        return {}
    def __setstate__(self, state):
        self.__init__()
