from pico2d import load_image, draw_rectangle, load_font
from StateMachine import *

whatfood = {'apple_green','apple_red','apple_yellow','abocado_whole',
            'banana','beet','blueberries',
            'cantaloupe_whole','carrot','cheese','cherries',
            'tomato',
            'watermelon',
            'strawberry'}

class Foods:
    
    def __init__(self, what, x, y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.name = what#음식

        
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
    def draw(self):
        self.image.clip_draw(0, 0, self.imgW, self.imgH, self.x, self.y, self.w, self.h)
