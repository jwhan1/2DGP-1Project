from pico2d import load_image, draw_rectangle
import play_mode
import Game_world
class Furniture:
    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.image = load_image(f'image/furniture/{what}.png')
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
            pass
    def add_food(self, food):
        #점수를 주고 음식을 제거
        print('on')
        play_mode.Ui.point+=100
        Game_world.remove_collision_object(food)
        Game_world.remove_object(food)
        del food
        pass
