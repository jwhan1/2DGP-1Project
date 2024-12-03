from pico2d import load_image,get_canvas_width,get_canvas_height


class Background:
    def __init__(self):
        self.background = GameObject('image/background.png',get_canvas_width()/2,get_canvas_height()/2,get_canvas_width(),get_canvas_height())

        self.itemUI = load_image('image/foodUI.png')
    def update(self):
        pass

    def draw(self):
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.w, self.background.x, self.background.y, self.background.w, self.background.h)
        
        
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

class GameObject:
    def __init__(self, image_path, x, y, w=0, h=0):
        self.image = load_image(image_path)
        self.x = x
        self.y = y
        self.w = w
        self.h = h