from pico2d import *
#캐릭터 관련 조작 : 4방향키, e
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[0] == SDLK_RIGHT
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[0] == SDLK_LEFT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_LEFT
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[0] == SDLK_UP
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_UP
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[0] == SDLK_DOWN
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_DOWN
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_SPACE
def press_e(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[0] == SDLK_e

def time_out(e):
    return e[0] == 'TIME_OUT'

def start(e):
    return e[0] == 'START'

class Charater:
    def __init__(self):
        self.x, self.y = 400, 300    #위치
        self.w, self.h = 100, 100   #크기
        self.xdir, self.ydir = 0, 0    #이동
        self.frame = 0
        self.action = 7             #동작
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)



        self.image = load_image(f'image\chief.png')

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
        pass
    def start(self):
        pass
    def state(self):
        pass

class Idle:
    
    @staticmethod
    def start(boy,e):
        boy.action = 8
        boy.frame = 0
        boy.dir = 0
        
    @staticmethod
    def enter(boy,e):
        if boy.action < 4:
            boy.action = boy.action + 4
        boy.frame = 0
        boy.dir = 0
        
    @staticmethod
    def exit(boy,e):
        pass

    @staticmethod
    def do(boy):
        print(boy.frame)
        boy.frame = (boy.frame + 1) % 3

    @staticmethod
    def draw(boy):
            boy.image.clip_draw(boy.frame * 120, boy.action * 130, 120, 130, boy.x, boy.y)

class Move:
    pass

class Interrect:
    pass

class StateMachine:
    #상태 처리
    def __init__(self,o):
        self.o = o# 객체
        self.event_que=[] #발생한 이벤트

    def start(self, start_state):
        # 시작 상태
        self.cur_state = start_state # Idle
        self.cur_state.enter(self.o,('START', 0))
   
    def add_event(self,event):
        self.event_que.append(event)#상태머신내에 이벤트
        
    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        # 상태 업데이트
        self.cur_state.do(self.o) 
        #이벤트 발생 시 상태 변환
        if self.event_que:
            e = self.event_que.pop[0]
            for check_event, next_state, in self.transitions(self.cur_state.items()):
                if check_event(e):
                    print(f'exit from{self.cur_state}')
                    self.cur_state.exit(self.o)
                    self.cur_state = next_state
                    print(f'enter to{self.cur_state}')
                    self.cur_state.enter(self.o)

    def draw(self):
        self.cur_state.draw(self.o)
