from pico2d import load_image, draw_rectangle, load_font
from StateMachine import *

class Foods:
    
    def __init__(self, what, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.timer = 15
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

        self.state_machine.set_transitions(
            {Idle: {time_out:Idle }
            })

        self.image = load_image(f'image/food/{what}.png')
        self.imgW = self.image.w
        self.imgH = self.image.h
    def update(self):
        pass
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        pass
#충돌
    def get_bb(self):
       return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            if group == 'charater:food' and  (other.onhand == None or other.onhand == self):
                pass
            elif group == 'charater:food':
                pass

class Idle:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy,e):
        pass
    @staticmethod
    def do(boy):
        pass
    @staticmethod
    def draw(food):
        food.image.clip_draw(0, 0, food.imgW, food.imgH, food.x, food.y, food.w, food.h)

class cooking:
    @staticmethod
    def enter(boy,e):
        pass
    @staticmethod
    def exit(boy,e):    
        pass
    @staticmethod
    def do(boy):
        pass
    @staticmethod
    def draw(food):
        food.image.clip_draw(0, 0, food.imgW, food.imgH, food.x, food.y, food.w, food.h)