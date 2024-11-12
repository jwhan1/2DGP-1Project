from pico2d import *
from StateMachine import *

import Game_world
import framework

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Charater:
    image_w=120
    image_h=130
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
            {
                Idle: { right_down or left_down or up_up or down_down: Move }, 
                Move: { right_up or left_up or up_up or down_up: Idle }, 
                #Interrect: { time_out: Idle, right_down or left_down or up_down or down_down: Move } #상호작용
                })
        
    def update(self):
        self.state_machine.update()
    def draw(self):
        self.state_machine.draw()
    def handle_event(self, event):
        #input event
        #state machine event : (이벤트 종류, 큐)
        self.state_machine.add_event(('INPUT', event))
#충돌
    def get_bb(self):
        pass
    def handle_collision(self, group, other):
            pass



class Idle:
    @staticmethod
    def enter(boy,e):
        if start(e):
            boy.action = 3
            boy.face_dir = 1
        elif right_down(e) or left_up(e):
            boy.action = 2
            boy.face_dir = -1
        elif left_down(e) or right_up(e):
            boy.action = 3
            boy.face_dir = 1

        boy.frame = 0
        boy.wait_time = get_time()
  
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME* framework.frame_time) % 8

    @staticmethod
    def draw(boy):
            boy.image.clip_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, 120, 130, boy.x, boy.y)

class Move:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            boy.dir, boy.face_dir, boy.action = -1, -1, 0

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()


    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME*game_framework.frame_time) % 8

        boy.x += boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 120, boy.action * 130, 120, 130, boy.x, boy.y)



class Interrect:
    pass

