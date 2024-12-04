import framework
import play_mode
import levelchoose_mode

from pico2d import load_image, draw_rectangle,load_wav,get_canvas_height,get_canvas_width


class button:
    sound=None
    def __init__(self,what,x,y):
        self.x, self.y = x, y
        self.what = what
        self.image = load_image(f'title/{what}_button.png')
        self.imgW, self.imgH = self.image.w, self.image.h

        if button.sound==None:
            button.sound = load_wav('title\Level Ready.mp3')
            button.sound.set_volume(32)
        match what:
            case 'start':
                self.w,self.h=100,100
            case 'level_1':
                self.w,self.h=100,50
            case 'level_2':
                self.w,self.h=100,50
            case 'level_3':
                self.w,self.h=100,50

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        left, bottom, right, top = self.get_bb()
        bottom, top = get_canvas_height() - top, get_canvas_height() - bottom
        if left < event.x and event.x < right and bottom < event.y and event.y < top:
            
            match self.what:
                case 'start':
                    button.sound.play()
                    framework.change_mode(levelchoose_mode)
                case 'level_1':
                    button.sound.play()
                    framework.change_mode(play_mode)
                case 'level_2':
                    button.sound.play()
                    framework.change_mode(play_mode)
                case 'level_3':
                    button.sound.play()
                    framework.change_mode(play_mode)
    
    def get_bb(self):
        return self.x - self.w/2, self.y - self.h/2, self.x + self.w/2, self.y + self.h/2
    def handle_collision(self, group, other):
        pass
    def add_food(self, food):
        pass
    def remove_food(self,food):
        pass
