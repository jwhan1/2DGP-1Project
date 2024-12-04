from pico2d import *
from random import choice, randrange
from time import time
from framework import change_mode 
import result_mode
from Game_data import Ingredient, cooked_food, Game_point
GAME_TIME_LIMIT = 180


#UI총괄 클래스
class UI:
    
    def __init__(self):
        self.stack=[]
        self.result=[]
        self.order_list=[Order() for i in range(2)]#주문목록
        self.timer = Timer()
        self.Point = Point()

    def update(self):
        self.timer.do(self)
        self.Point.do()
        for i in range(len(self.order_list)):
            self.order_list[i].do()
    def draw(self):
        self.timer.draw()
        self.Point.draw()
        for i in range(len(self.order_list)):
            self.order_list[i].draw(i)
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
        self.timer = time()# 남은 게임 제한시간
        self.elapsed_time = GAME_TIME_LIMIT
        self.order_time = time() + randrange(5,15)
        self.image = load_image("image/timer.png")

    def do(self, UI):
        self.elapsed_time = GAME_TIME_LIMIT-(time() - self.timer)

        if self.order_time - time() < 0:
            self.order_time += randrange(5,15)
            if len(UI.order_list) < 5:
                UI.order_list.append(Order())

        if self.elapsed_time < 0:# 시간이 되면
            Game_point.append(UI.Point.point)
            change_mode(result_mode)
    def draw(self):
        self.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '', 
                                       (int)(get_canvas_width()/2 * self.elapsed_time / GAME_TIME_LIMIT),get_canvas_height()-10,
                                         (int)(get_canvas_width()* self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머


class Point:
    font = None
    def __init__(self):
        self.point = 0# 게임 포인트
        if Point.font == None:
            Point.font = load_font('ENCR10B.TTF', 40)

    def do(self):
        pass
    def draw(self): 
     Point.font.draw(20, get_canvas_height()-40, f'point:{self.point}', (0, 0, 255))


class Order:
    image = None
    font = None
    def __init__(self):
        self.x,self.y=get_canvas_width()-270, get_canvas_height()-80
        self.w,self.h = 60, 120
        self.food = choice(Ingredient)
        if self.food in cooked_food:
            self.point = randrange(300,500)
        else:
            self.point = randrange(110,150)
        self.image = load_image(f'image/food/{self.food}.png')
        

        if Order.font == None:
            Order.font = load_font('ENCR10B.TTF', 20)
        if Order.image == None:
            Order.image = load_image('image/order_paper.png')
    def do(self):
        pass
    def draw(self,count): 
        Order.image.clip_draw(0, 0, Order.image.w, Order.image.h, self.x + 60 * count, self.y, self.w, self.h)

        Order.font.draw(self.x + 60 * count - 25, self.y-30,f"{self.point}P")
        self.image.clip_draw(0, 0, self.image.w, self.image.h, self.x + 60 * count, self.y + 15, 50, 50)