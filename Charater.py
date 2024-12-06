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
    font=None
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
                Idle: {right_down: MoveRight, left_down: MoveLeft, left_up: MoveRight, right_up: MoveLeft, up_down: MoveUp, down_down: MoveDown, up_up: MoveDown, down_up: MoveUp, press_e:Idle, press_r:Idle, press_f:Idle},
                MoveRight: {right_up: Idle, left_down: Idle, up_down: MoveRightUp, up_up: MoveRightDown, down_down: MoveRightDown, down_up: MoveRightUp, press_e:MoveRight, press_r:MoveRight, press_f:MoveRight},
                MoveRightUp: {up_up: MoveRight, right_up: MoveUp, left_down: MoveUp, down_down: MoveRight, press_e:MoveRightUp, press_r:MoveRightUp, press_f:MoveRightUp},
                MoveUp: {up_up: Idle, left_down: MoveLeftUp, down_down: Idle, right_down: MoveRightUp, left_up: MoveRightUp, right_up: MoveLeftUp, press_e:MoveUp, press_r:MoveUp, press_f:MoveUp},
                MoveLeftUp: {right_down: MoveUp, down_down: MoveLeft, left_up: MoveUp, up_up: MoveLeft, press_e:MoveLeftUp, press_r:MoveLeftUp, press_f:MoveLeftUp},
                MoveLeft: {left_up: Idle, up_down: MoveLeftUp, right_down: Idle, down_down: MoveLeftDown, up_up: MoveLeftDown, down_up: MoveLeftUp, press_e:MoveLeft, press_r:MoveLeft, press_f:MoveLeft},
                MoveLeftDown: {left_up: MoveDown, down_up: MoveLeft, up_down: MoveLeft, right_down: MoveDown, press_e:MoveLeftDown, press_r:MoveLeftDown, press_f:MoveLeftDown},
                MoveDown: {down_up: Idle, left_down: MoveLeftDown, up_down: Idle, right_down: MoveRightDown, left_up: MoveRightDown, right_up: MoveLeftDown, press_e:MoveDown, press_r:MoveDown, press_f:MoveDown},
                MoveRightDown: {right_up: MoveDown, down_up: MoveRight, left_down: MoveDown, up_down: MoveRight, press_e:MoveRightDown, press_r:MoveRightDown, press_f:MoveRightDown}
            }
        )
        self.grab = True
        self.held_item = []#들고 있는 음식
        self.emphatic_food = 0

        self.placeputup = []#접근 가능한 가구
        self.handrangefood = []#접근 가능한 음식
        
        if Charater.font == None:
            Charater.font = load_font("ENCR10B.TTF",16)
    def update(self):
        self.state_machine.update()

        if self.placeputup:
            for o in self.placeputup:
                if not (o.x + o.w > self.w - self.w and o.x - o.w < self.w + self.w  and o.y + o.h > self.y - self.h and o.y - o.h < self.y + self.h):
                    self.placeputup.remove(o)
        self.placeputup.clear()           
        if self.handrangefood:
            for o in self.handrangefood:
                if not (o.x + o.w > self.w - self.w and o.x - o.w < self.w + self.w  and o.y + o.h > self.y - self.h and o.y - o.h < self.y + self.h):
                    self.handrangefood.remove(o)
        self.handrangefood.clear()
    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        image = None
        #선택한 아이템 강조
        if self.emphatic_food >= 0 and len(self.held_item) > 0 and self.emphatic_food < len(self.held_item):
            draw_rectangle(*self.held_item[self.emphatic_food].get_bb())
            image = self.held_item[self.emphatic_food].image
        
        if self.grab:
            Charater.font.draw(self.x-self.w/2, self.y-self.h/2-20,"place")
        else:
            Charater.font.draw(self.x-self.w/2, self.y-self.h/2-20,"pick up")
# 입력
    def handle_event(self, event):
        self.state_machine.add_event(('INPUT', event))
# 충돌
    def get_bb(self):
        return self.x-self.w/2,self.y-self.h/2,self.x+self.w/2,self.y+self.h/2

    def handle_collision(self, group, other):
            match  group:
                case 'charater:food':# 반경에 들어온 음식 
                    food = other
                    self.handrangefood.append(food)#접근 가능한 음식
                case 'charater:counter':
                    place = other
                    self.placeputup.append(place) #접근 가능한 장소
                case 'charater:cookware':
                    place = other
                    self.placeputup.append(place) #접근 가능한 장소
                case 'charater:wall':#벽 부딪힘
                    xdis, ydis = other.x - self.x, other.y - self.y
                    xR , yR = (self.w + other.w) / 2, (self.h + other.h) / 2
                    xrange, yrange = abs(abs(xdis) - xR), abs(abs(ydis) - yR)


                    # x축 충돌 검사
                    
                    if -xR < xdis < xR and xrange > yrange:  # 위아래에 있음
                        if 0 <= ydis <= yR and self.ydir > 0:  # 위 막힘
                                self.ydir = 0
                        elif -yR <= ydis <= 0 and self.ydir < 0:  # 아래 막힘
                                self.ydir = 0

                    elif -yR < ydis < yR and xrange < yrange:  # 양 옆에 있음
                        if 0 <= xdis <= xR and self.xdir > 0:  # 아래 막힘
                            self.xdir = 0
                        elif -xR <= xdis <= 0 and self.xdir < 0:  # 위 막힘
                            self.xdir = 0

    def add_food(self, food):
        food.held_by = self
        if not food in self.held_item:self.held_item.append(food)
        food.w = 50
        food.h = 50
        food.x = get_canvas_width() - 50 * (self.held_item.index(food) + 1)
        food.y = 50
    def remove_food(self,food):
        if food in self.held_item: self.held_item.remove(food)
        
        if self.emphatic_food>=len(self.held_item):
            self.emphatic_food=len(self.held_item)-1
    def __getstate__(self):
        state = {'x':self.x, 'y':self.y, 'held_item':self.held_item, 'emphatic_food':self.emphatic_food}
        return state
    def __setstate__(self, state):
        self.__init__()
        self.__dict__.update(state)

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
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        if o.max_capacity > len(o.held_item):
                            place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
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
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        
        if boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    
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
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveRight:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = 1, 0, 0
    @staticmethod
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        
     
    
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
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if  boy.x + boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time <  get_canvas_width():
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time:
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
    
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveDown:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = 0, -1, 3
    @staticmethod
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time:
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
   
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
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time:
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if 0 < boy.y - boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time:
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)

class MoveLeft:
    @staticmethod
    def enter(boy, e):
        boy.xdir, boy.ydir, boy.action = -1, 0, 2
    @staticmethod
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time:
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        
     
   
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
    def exit(boy,e):
        if press_e(e) :
            if  boy.grab and len(boy.held_item) > 0 and boy.placeputup: # 조리대, 매대에 음식을 올린다.
                place = None
                for o in boy.placeputup:
                    if  place == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (place.x-boy.x)**2 + (place.y-boy.y)**2:#더 가까우면
                        place = o

                if place != None:
                    boy.held_item[boy.emphatic_food].move_to(place)
                    #음식들의 위치를 잡는다
                    index=0
                    for held_food in boy.held_item:
                        held_food.x, held_food.y = get_canvas_width() - 50 * (index + 1), 50
                        index = index + 1
                        

                else: print('놓을 곳이 없다.')

            elif not boy.grab and len(boy.held_item) < 5 and boy.handrangefood: # 주변의 가까운 음식을 집는다.
                target = None # 집을 음식
                #잡을 음식 고르기
                for o in boy.handrangefood:
                    if  target == None or (o.x-boy.x)**2 + (o.y-boy.y)**2 < (target.x-boy.x)**2 + (target.y-boy.y)**2:#더 가까우면
                        target = o
                #음식 가져오기
                if target != None and not target in boy.held_item:# 잡기
                    target.move_to(boy)
                else: print('주변에 음식이 없음')
        elif press_r(e):
            boy.grab = not boy.grab
        elif press_f(e):
            if len(boy.held_item) > 0: boy.emphatic_food = (boy.emphatic_food + 1) % len(boy.held_item)
    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        # boy.x += boy.dir * 5

        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * framework.frame_time) % 8
        if 0 < boy.x - boy.w / 2 + boy.xdir * RUN_SPEED_PPS * framework.frame_time:
            boy.x += boy.xdir * RUN_SPEED_PPS * framework.frame_time
        if boy.y + boy.h/2 + boy.ydir * RUN_SPEED_PPS * framework.frame_time < get_canvas_height():
            boy.y += boy.ydir * RUN_SPEED_PPS * framework.frame_time
        
     
    
    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(int(boy.frame) * Charater.image_w, boy.action * Charater.image_h, Charater.image_w, Charater.image_h, 0, '', boy.x, boy.y, boy.w, boy.h)
