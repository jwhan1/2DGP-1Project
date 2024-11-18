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
        self.w, self.h = 50, 50   #크기
        self.xdir, self.ydir = 0, 0    #이동
        self.frame = 0
        self.action = 7             #동작
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)

        self.image = load_image(f'image/chief.png')

        self.state_machine.set_transitions(
            {Idle: {right_down : Move, left_down : Move, up_down : Move, down_down: Move, press_e:Idle }, 
            Move: { right_up: Idle, left_up : Idle, up_up : Idle, down_up: Idle, press_e:Move}}
            )
        self.onhand = None#들고 있는 음식
        self.placeputup = []#접근 가능한 가구
        self.handrangefood = []#접근 가능한 음식
        
    def update(self):
        self.state_machine.update()

        if self.placeputup:
            for o in self.placeputup:
                if not (o.x + o.w > self.w - self.w and o.x - o.w < self.w + self.w  and o.y + o.h > self.y - self.h and o.y - o.h < self.y + self.h):
                    self.placeputup.remove(o)
                    
        if self.handrangefood:
            for o in self.handrangefood:
                if not (o.x + o.w > self.w - self.w and o.x - o.w < self.w + self.w  and o.y + o.h > self.y - self.h and o.y - o.h < self.y + self.h):
                    self.handrangefood.remove(o)


    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
#충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2
    
    def handle_collision(self, group, other):
            if group == 'charater:food':# 반경에 들어온 음식 
                food = other
                self.handrangefood.append(food)#접근 가능한 음식
            elif group == 'charater:counter' or group == 'charater:cookware':
                place = other
                self.placeputup.append(place) #접근 가능한 장소
                
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
        if press_e(e) :
            if boy.onhand == None and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o

                if target != None:# 잡기
                    boy.onhand = target
                    boy.onhand.x = 750
                    boy.onhand.y = 50
            elif boy.onhand != None and boy.placeputup != None: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.onhand.x = place.x
                    boy.onhand.y = place.y
                    boy.onhand = None

    @staticmethod
    def do(boy):
        if boy.action != 5:
            boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME* framework.frame_time) % 3
        else:
            boy.frame = 0
    @staticmethod
    def draw(boy):
            boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h )

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
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time < 650:
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 100 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < 600:
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(onhand)의 위치를 업데이트
        if boy.onhand is not None:
            boy.onhand.x = boy.x
            boy.onhand.y = boy.y
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)
