from pico2d import *
import framework
import time

import result_mode
import Game_data
GAME_TIME_LIMIT = 10


#UI총괄 클래스
class UI:
    
    def __init__(self):
        self.stack=[]#
        self.result=[]#

        self.timer = Timer()
        self.Point = Point()
        self.order = Order()
    def update(self):
        self.timer.do(self)
        self.Point.do(self)
        self.order.do(self)
    def draw(self):
        self.timer.draw()
        self.Point.draw()
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

    def do(self,U):
        self.elapsed_time = GAME_TIME_LIMIT-(time.time() - self.timer)
        if self.elapsed_time < 0:# 시간이 되면
            Game_data.Game_point.append(U.Point.point)
            framework.change_mode(result_mode)
            
            

    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '', 
                                       (int)(get_canvas_width()/2 * self.elapsed_time / GAME_TIME_LIMIT),get_canvas_height()-10,
                                         (int)(get_canvas_width()* self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머


class Point:
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.point = 0# 게임 포인트
        

    def do(self,U):
        pass
    def draw(self): 
     self.font.draw(20, get_canvas_height()-40, f'point:{self.point}', (0, 0, 255))


class Order:
    def __init__(self):
        pass
    def do(self,U):
         pass
    def draw(self): 
     pass