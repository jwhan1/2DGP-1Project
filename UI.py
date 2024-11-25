from pico2d import *
import framework
import time


GAME_TIME_LIMIT = 180



class UI:
    
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 40)
        self.stack=[]#
        self.cooking=[]#
        self.result=[]#
        self.timer = time.time()# 남은 게임 제한시간
        self.elapsed_time = GAME_TIME_LIMIT
        self.point = 0# 게임 포인트
        self.image = load_image("image/timer.png")
    def update(self):
        self.elapsed_time = GAME_TIME_LIMIT-(time.time() - self.timer)
        if self.elapsed_time < 0:# 시간이 되면
            pass#게임 결과창으로 넘어간다
        
    def draw(self):
        #타이머, 점수 표시
        print(f'time = {int(self.elapsed_time)}   /{self.point = }')
        self.image.clip_composite_draw(0, 0, self.image.w , self.image.h, 0, '', 
                                       (int)(360 * self.elapsed_time / GAME_TIME_LIMIT),590,
                                         (int)(720 * self.elapsed_time / GAME_TIME_LIMIT), 20)# 타이머
        self.font.draw(20, 560, f'point:{self.point}', (0, 0, 255))
    def handle_event(self, event):
        pass

    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    
    def handle_collision(self, group, other):
            pass

