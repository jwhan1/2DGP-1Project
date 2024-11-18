from pico2d import load_font,os
import framework
import time


GAME_TIME_LIMIT = 180


class UI:
    try:
        font = load_font('ENCR10B.TTF', 16)
    except Exception as e:
        print(f"문제가 발생했습니다: {type(e).__name__} - {e}")
    def __init__(self):
        
        self.stack=[]#
        self.cooking=[]#
        self.result=[]#
        self.timer = time.time()# 전체 게임 제한시간
        self.point = 0# 게임 포인트

    def update(self):
        if time.time() - self.timer > GAME_TIME_LIMIT:# 시간이 되면
            pass
        
    def draw(self):
        #타이머, 점수 표시
        print(f'time = {int(GAME_TIME_LIMIT-(time.time() - self.timer))}   /{self.point = }')

    def handle_event(self, event):
        pass

    #충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    
    def handle_collision(self, group, other):
            pass

