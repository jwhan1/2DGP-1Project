from pico2d import load_image, load_wav, get_canvas_width,get_canvas_height


class Background:
    def __init__(self):
        self.image = load_image('image/background.png')
        self.x = get_canvas_width()/2
        self.y = get_canvas_height()/2
        self.w = get_canvas_width()
        self.h = get_canvas_height()
        self.bgm = load_wav("sound/background_music.mp3")
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.image.w, self.image.w, self.x, self.y, self.w, self.h)
        
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
