from pico2d import *
from StateMachine import *

import Game_world
import framework

# Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Action Speed
TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Charater:
    image_w = 120
    image_h = 130
    def __init__(self):
        self.x, self.y = 400, 300    #위치
        self.w, self.h = 100, 100   #크기
        self.xdir, self.ydir = 0, 0    #이동
        self.frame = 0
        self.action = 7             #동작
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

        self.image = load_image(f'image/chief.png')

        self.state_machine.set_transitions(
            {Idle: {right_down : Move, left_down : Move, up_down : Move, down_down: Move }, 
            Move: { right_up: Idle, left_up : Idle, up_up : Idle, down_up: Idle}}
            )
        self.onhand = None
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
#충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    def handle_collision(self, group, other):
            if group == 'charater:food' and self.onhand == None:
                    self.onhand = other



class Idle:
    @staticmethod
    def enter(boy,e):
        if right_up(e):
            boy.action = 4
        elif up_up(e):
            boy.action = 5
        elif left_up(e):
            boy.action = 6
        elif down_up(e) or start(e):
            boy.action = 7

        boy.frame = 0
        boy.wait_time = get_time()
  
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        if boy.action != 5:
            boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME* framework.frame_time) % 3
        else:
            boy.frame = 0
    @staticmethod
    def draw(boy):
            boy.image.clip_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, 120, 130, boy.x, boy.y)

class Move:
    @staticmethod
    def enter(boy, e):
        if right_down(e):
            boy.xdir, boy.ydir, boy.action = 1, 0, 0
        elif up_down(e):
            boy.xdir, boy.ydir, boy.action = 0, 1, 1
        elif left_down(e):
            boy.xdir, boy.ydir, boy.action = -1, 0, 2
        elif down_down(e):
            boy.xdir, boy.ydir, boy.action = 0, -1, 3
    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8

        boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 120, boy.action * 130, 120, 130, boy.x, boy.y)
