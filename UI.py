from random import randrange
from time import time
from pico2d import *
import Game_world
import play_mode
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
    def __init__(self):
        #점수
        self.point = 0
        if UI.font == None:
            UI.font = load_font('ENCR10B.TTF', 40)
        #시간
        self.timer = time()# 남은 게임 제한시간
        self.elapsed_time = GAME_TIME_LIMIT
        self.order_time = time() + randrange(5,15)
        if UI.image == None:
            UI.image= load_image("image/timer.png")

        
        self.itemUI = load_image('image/foodUI.png')

        
    def update(self):
        #시간
        self.elapsed_time = GAME_TIME_LIMIT-(time() - self.timer)
        if len(play_mode.orders) <= 0 or self.order_time - time() < 0 :
            if len(play_mode.orders) < 5:
                order=Order(len(play_mode.orders))
                play_mode.orders.append(order)
                Game_world.add_object(order,2)
            if self.order_time - time() < 0:
                self.order_time += randrange(5,12)
        
        if self.elapsed_time < 0:# 시간이 되면
            Game_point.append(UI.Point.point)
            change_mode(result_mode)
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
        state = { "elapsed_time":self.elapsed_time}
        return state
    def __setstate__ (self,state):
        self.__init__()
        self.update(state)

