from random import randrange
from time import time
from pico2d import *
import Game_world
import result_mode
from Game_data import Game_point
from Order import Order
from framework import change_mode
from pico2d import get_canvas_height, get_canvas_width, load_image


GAME_TIME_LIMIT = 180


#UI총괄 클래스
class UI:
    image = None
    font = None
    Ui = None
    point = None
    def __init__(self):
        #점수, 시간, 주문추가
        self.timer = time()# 게임 시작시간
        self.elapsed_time = GAME_TIME_LIMIT
        self.left_time = randrange(5,15)
        self.order_time = time()
        
        self.itemUI = load_image('image/foodUI.png')

        if UI.point == None:
            UI.point = 0
        if UI.font == None:
            UI.font = load_font('ENCR10B.TTF', 40)
        if UI.image == None:
            UI.image = load_image("image/timer.png")
        if Order.list == None:
            Order.list = []
    def update(self):
        #시간
        self.elapsed_time = GAME_TIME_LIMIT-(time() - self.timer)
        if self.elapsed_time < 0:# 시간이 되면
            Game_point.append(self.point)
            change_mode(result_mode)

        self.left_time -= time() - self.order_time
        self.order_time = time()

        if len(Order.list) <= 0 or self.left_time < 0 and len(Order.list) <= 5:
            order = Order(len(Order.list))
            if Order.list == None:
                Order.list = []
            if not order in Game_world.world:
                Game_world.add_object(order,2)
            if not order in Order.list:
                Order.list.append(order)
            if self.left_time < 0:
                self.left_time = randrange(5,12)

    def draw(self):
        #시간
        
        UI.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '',
                                       (int)(get_canvas_width()/2 * self.elapsed_time / GAME_TIME_LIMIT),get_canvas_height()-10,
                                         (int)(get_canvas_width()* self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머
        #점수
        UI.font.draw(20, get_canvas_height()-40, f'point:{self.point}', (0, 0, 255))
        #아이템칸
        for i in range(1,6):
            self.itemUI.clip_draw(0, 0, self.itemUI.w, self.itemUI.h, get_canvas_width()-50*i, 50, 50, 50)

    def handle_event(self, event):
        pass

    #충돌
    def get_bb(self):
        return {}
    
    def handle_collision(self, group, other):
            pass
    def __getstate__(self):
        state = { "elapsed_time":self.elapsed_time, "left_time":self.left_time}
        return state
    def __setstate__ (self,state):
        self.__init__()
        self.timer = time() - (GAME_TIME_LIMIT - state["elapsed_time"])
        self.__dict__.update(state)