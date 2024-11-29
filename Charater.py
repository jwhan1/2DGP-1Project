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
            {
                Idle: {right_down: MoveRight, left_down: MoveLeft, left_up: MoveRight, right_up: MoveLeft, up_down: MoveUp, down_down: MoveDown, up_up: MoveDown, down_up: MoveUp, press_e:Idle},
                MoveRight: {right_up: Idle, left_down: Idle, up_down: MoveRightUp, up_up: MoveRightDown, down_down: MoveRightDown, down_up: MoveRightUp, press_e:MoveRight},
                MoveRightUp: {up_up: MoveRight, right_up: MoveUp, left_down: MoveUp, down_down: MoveRight, press_e:MoveRightUp},
                MoveUp: {up_up: Idle, left_down: MoveLeftUp, down_down: Idle, right_down: MoveRightUp, left_up: MoveRightUp, right_up: MoveLeftUp, press_e:MoveUp},
                MoveLeftUp: {right_down: MoveUp, down_down: MoveLeft, left_up: MoveUp, up_up: MoveLeft, press_e:MoveLeftUp},
                MoveLeft: {left_up: Idle, up_down: MoveLeftUp, right_down: Idle, down_down: MoveLeftDown, up_up: MoveLeftDown, down_up: MoveLeftUp, press_e:MoveLeft},
                MoveLeftDown: {left_up: MoveDown, down_up: MoveLeft, up_down: MoveLeft, right_down: MoveDown, press_e:MoveLeftDown},
                MoveDown: {down_up: Idle, left_down: MoveLeftDown, up_down: Idle, right_down: MoveRightDown, left_up: MoveRightDown, right_up: MoveLeftDown, press_e:MoveDown},
                MoveRightDown: {right_up: MoveDown, down_up: MoveRight, left_down: MoveDown, up_down: MoveRight, press_e:MoveRightDown}
            }
        )
        self.held_item = []#들고 있는 음식
        self.emphatic_food = 0

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
        #선택한 아이템 강조
        if self.emphatic_food < len(self.held_item):
            draw_rectangle(*self.held_item[self.emphatic_food].get_bb())

# 입력
    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
# 충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2

    def handle_collision(self, group, other):
            if group == 'charater:food':# 반경에 들어온 음식 
                food = other
                self.handrangefood.append(food)#접근 가능한 음식
            elif group == 'charater:counter' or group == 'charater:cookware':
                place = other
                self.placeputup.append(place) #접근 가능한 장소
    def add_food(self, food):
        food.held_by = self
        self.held_item.append(food)
        food.w /= 5
        food.h /= 5
        food.x = self.x + food.w * self.held_item.index(food)
        food.y = self.y - self.h / 2 - food.h
    def remove_food(self,food):
        self.held_item.remove(food)





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
            if len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[0].move_to(place)
                else: print('놓을 곳이 없다.')

            elif len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                print('a')
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
    @staticmethod
    def do(boy):
        if boy.action != 5:
            boy.frame = (boy.frame + FRAMES_PER_ACTION*ACTION_PER_TIME* framework.frame_time) % 3
        else:
            boy.frame = 0
    @staticmethod
    def draw(boy):
            boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h )



class MoveUp:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = 0, 1, 1
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveRightUp:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir=1,1
        if right_down(e):
            boy.action =  0
        elif up_down(e):
             boy.action = 1
        
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveRight:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = 1, 0, 0
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveRightDown:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir=1,-1
        if right_down(e):
            boy.action = 0
        elif down_down(e):
            boy.action = 3
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveDown:
    @staticmethod
    def enter(boy, e):
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
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveLeftDown:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir=-1,-1
        if left_down(e):
            boy.action = 2
        elif down_down(e):
            boy.action = 3
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveLeft:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = -1, 0, 2
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveLeftUp:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir=-1,1
        if up_down(e):
             boy.action = 1
        elif left_down(e):
             boy.action = 2
    @staticmethod
    def exit(boy, e):
        if press_e(e):
            pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time and boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time and boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    # 들고 있는 객체(held_item)의 위치를 업데이트
        for o in boy.held_item:
            o.x = boy.x + o.w * boy.held_item.index(o)
            o.y = boy.y - boy.h / 2 - o.w / 2
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)
