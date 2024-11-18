from pico2d import load_image


class Background:
    def __init__(self):
        self.background = GameObject('image/background.png',400,300,800,600)

        self.itemUI = GameObject('image/itemUI.png',750,50,60,60)
    def update(self):
        pass

    def draw(self):
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.w, self.background.x, self.background.y, self.background.w, self.background.h)
        #self.floor.image.clip_draw(0, 0, self.floor.image.w, self.floor.image.h, self.floor.x, self.floor.y, self.floor.w, self.floor.h)
        #self.itemUI.image.clip_draw(0, 0, self.itemUI.image.w, self.itemUI.image.h, self.itemUI.x, self.itemUI.y, self.itemUI.w, self.itemUI.h)


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