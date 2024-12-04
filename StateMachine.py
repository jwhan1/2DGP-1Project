from pico2d import *
#조작 : 4방향키
def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT
def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT
def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT
def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP
def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP
def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN
# 조작 : 문자
def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
def press_e(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_e
def press_r(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_r

# 상태 변화
def time_out(e):
    return e[0] == 'TIME_OUT'

def start(e):
    return e[0] == 'START'





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
        self.event_que.append(event)#상태머신내에 이벤트 추가

    def set_transitions(self, transitions):
        self.transitions = transitions

    def update(self):
        self.cur_state.do(self.o)
        if self.event_que:
            event = self.event_que.pop(0)
            self.handle_event(event)

    def draw(self):
        self.cur_state.draw(self.o)

    def handle_event(self, e):
        #이벤트 상태 변환
        
        for event, next_state in self.transitions[self.cur_state].items():
            if event(e):
                #print(f'exit from{self.cur_state}')
                self.cur_state.exit(self.o, e)
                self.cur_state = next_state
                #print(f'enter to{self.cur_state}')
                self.cur_state.enter(self.o, e)
                return