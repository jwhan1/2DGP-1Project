from random import randrange
from time import time
from pico2d import *

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
    def update(self):
        #시간
        self.elapsed_time = GAME_TIME_LIMIT-(time() - self.timer)

        if self.order_time - time() < 0:
            self.order_time += randrange(5,15)
            if len(play_mode.orders) < 5:
                play_mode.orders.append(Order(len(play_mode.orders)))

        if self.elapsed_time < 0:# 시간이 되면
            Game_point.append(UI.Point.point)
            change_mode(result_mode)
    def draw(self):
        #시간
        UI.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '',
                                       (int)(get_canvas_width()/2 * self.elapsed_time / GAME_TIME_LIMIT),get_canvas_height()-10,
                                         (int)(get_canvas_width()* self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머

        UI.font.draw(20, get_canvas_height()-40, f'point:{self.point}', (0, 0, 255))
    def handle_event(self, event):
        pass

    #충돌
    def get_bb(self):
        return {}
    
    def handle_collision(self, group, other):
            pass
    def __getstate__(self):
        state = { 'result':self.result}
        return state

