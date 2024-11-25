from pico2d import load_image, draw_rectangle,load_font
import framework
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

class Cookware:

    def __init__(self, what, x, y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.stack=[]#조리 대기열
        self.cooking=[]#조리중인 요리
        self.result=[]#조리된 요리
        
        self.timer = framework.frame_time # 요리 시작시간


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


    def build_behavior_tree(self):
       pass