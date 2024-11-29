from pico2d import *
import framework
import time


GAME_TIME_LIMIT = 180


#UI총괄 클래스
class UI:
    
    def __init__(self):
        self.stack=[]#
        self.result=[]#

        self.timer = Timer()
        self.Point = Point()
        self.slot = Item_Slot()
        self.order = Order()
    def update(self):
        self.timer.do()
        self.Point.do()
        self.slot.do()
        self.order.do()
    def draw(self):
        self.timer.draw()
        self.Point.draw()
        self.slot.draw()
        self.order.draw()
    def handle_event(self, event):
        pass

    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    
    def handle_collision(self, group, other):
            pass
    def add_point(self,name):
        #주문 목록에 있을 경우 점수 상승
        self.Point.point==100

class Timer:
    
    def __init__(self):
        self.timer = time.time()# 남은 게임 제한시간
        self.elapsed_time = GAME_TIME_LIMIT
        self.image = load_image("image/timer.png")

    def do(self):
        self.elapsed_time = GAME_TIME_LIMIT-(time.time() - self.timer)
        if self.elapsed_time < 0:# 시간이 되면
            pass#게임 결과창으로 넘어간다

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '', 
                                       (int)(360 * self.elapsed_time / GAME_TIME_LIMIT),590,
                                         (int)(720 * self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머


class Point:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.point = 0# 게임 포인트
        

    def do(self):
        pass
    def draw(self): 
     self.font.draw(20, 560, f'point:{self.point}', (0, 0, 255))

class Item_Slot:
    def __init__(self):
        
        self.chosen_item = 0 #아이템 선택
        self.itemUI = load_image('image\itemUI.png')
        self.imgw=self.itemUI.w
        self.imgh=self.itemUI.h
    def do(self):
         pass
    def draw(self): 
        self.itemUI.clip_draw(0,0,self.imgw,self.imgh,100,100)


class Order:
    def __init__(self):
        pass
    def do(self):
         pass
    def draw(self): 
     pass